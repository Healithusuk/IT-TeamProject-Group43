import os
import time
import datetime
import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from allModels.models import Books, ArtworkType
import pandas as pd

class Command(BaseCommand):
    help = '从 Google Books API 获取书籍数据并填充到 Books 模型'

    def handle(self, *args, **options):
        # 设置搜索关键词，也可以从 CSV 或其他数据源读取书名
        # 读取 CSV 文件，示例中假设 CSV 中有一个 "Title" 列，存放连续剧名称
        df = pd.read_csv(r'Nifty\management\commands\Books.csv', encoding='latin1')
        search_queries = df['Book-Title'].tolist()

        for query in search_queries:
            self.stdout.write(f"正在搜索书籍：{query}")
            # 使用 Google Books API 搜索书籍
            url = "https://www.googleapis.com/books/v1/volumes"
            params = {
                "q": query,
                "maxResults": 5,  # 每个查询最多返回 5 条数据，根据需要调整
            }
            try:
                time.sleep(0.1)  # 控制请求频率
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"搜索 {query} 时出错: {e}"))
                continue

            items = data.get("items", [])
            if not items:
                self.stdout.write(self.style.WARNING(f"未找到书籍：{query}"))
                continue

            for item in items:
                volume_info = item.get("volumeInfo", {})
                # 书名
                book_name = volume_info.get("title", "")
                
                # 发行日期（可能为 "YYYY" 或 "YYYY-MM-DD"）
                published_date = volume_info.get("publishedDate", "")
                book_release_year = None
                if published_date:
                    try:
                        book_release_year = datetime.datetime.strptime(published_date, "%Y-%m-%d").date()
                    except Exception:
                        try:
                            book_release_year = datetime.datetime.strptime(published_date, "%Y").date()
                        except Exception:
                            book_release_year = None

                # 书籍类型（取 categories 数组中的第一个，如果存在）
                categories = volume_info.get("categories", [])
                book_genre = categories[0] if categories else "Unknown"

                # ArtworkType，此处假定书籍对应的类型写死为 "book"
                artwork_type, _ = ArtworkType.objects.get_or_create(artwork_type="book")

                # 书籍简介
                book_description = volume_info.get("description", "")

                # 作者列表，拼接为字符串
                authors = volume_info.get("authors", [])
                book_writer = ", ".join(authors) if authors else ""
                # 截断到 255 个字符
                if len(book_writer) > 255:
                    book_writer = book_writer[:255]

                # 国家信息：Google Books API 通常不提供出版国家，这里默认为 Unknown
                book_country = "Unknown"

                # 出版社
                book_publisher = volume_info.get("publisher", "")

                # ISBN，从 industryIdentifiers 中获取 ISBN_13 或 ISBN_10
                book_isbn = ""
                for identifier in volume_info.get("industryIdentifiers", []):
                    if identifier.get("type") in ["ISBN_13", "ISBN_10"]:
                        book_isbn = identifier.get("identifier")
                        break

                # 封面图片：从 imageLinks.thumbnail 获取
                image_links = volume_info.get("imageLinks", {})
                thumbnail_url = image_links.get("thumbnail", "")
                cover_file_name = ""
                cover_content = None
                if thumbnail_url:
                    try:
                        img_response = requests.get(thumbnail_url)
                        if img_response.status_code == 200:
                            cover_content = img_response.content
                            # 尝试从 URL 中提取文件后缀
                            ext = os.path.splitext(thumbnail_url)[1] or '.jpg'
                            cover_file_name = f"{book_isbn}{ext}"
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"下载封面图片出错: {e}"))
                        cover_content = None
                        
                # 检查是否已存在相同书籍（通过 ISBN 或书名判断）
                if (book_isbn and Books.objects.filter(book_isbn=book_isbn).exists()) or Books.objects.filter(book_name=book_name).exists():
                    self.stdout.write(self.style.WARNING(f"书籍 {book_name} (ISBN: {book_isbn}) 已存在，跳过。"))
                    continue


                # 创建书籍记录
                book = Books.objects.create(
                    book_name=book_name,
                    book_release_year=book_release_year,
                    book_genre=book_genre,
                    type=artwork_type,
                    book_description=book_description,
                    book_writer=book_writer,
                    book_country=book_country,
                    book_publisher=book_publisher,
                    book_isbn=book_isbn,
                )

                # 保存封面图片
                if cover_content:
                    book.book_cover_image.save(cover_file_name, ContentFile(cover_content), save=True)

                self.stdout.write(self.style.SUCCESS(f"书籍添加成功：{book_name}"))
        self.stdout.write(self.style.SUCCESS("所有书籍数据处理完毕！"))
