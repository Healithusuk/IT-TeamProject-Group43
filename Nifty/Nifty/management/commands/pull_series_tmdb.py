import os
import time
import datetime
import requests
import pandas as pd
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from allModels.models import TvShows, ArtworkType

class Command(BaseCommand):
    help = '从 TMDB API 获取连续剧数据并填充数据库'

    def handle(self, *args, **kwargs):
        # 请替换为你自己的 TMDB API Key
        tmdb_api_key = 'cf336e21d837d093d66ae7cc55001b2c'

        # 读取 CSV 文件，示例中假设 CSV 中有一个 "Title" 列，存放连续剧名称
        df = pd.read_csv(r'Nifty\management\commands\series_data.csv', encoding='latin1')
        tv_titles = df['Series_Title'].tolist()

        for title in tv_titles:
            self.stdout.write(f"正在搜索连续剧：{title}")
            # 1. 使用 search/tv 接口搜索连续剧
            search_url = "https://api.themoviedb.org/3/search/tv"
            search_params = {
                'api_key': tmdb_api_key,
                'query': title,
                'language': 'en-US',
                'page': 1,
            }
            try:
                time.sleep(0.1)
                search_response = requests.get(search_url, params=search_params)
                search_response.raise_for_status()
                search_data = search_response.json()
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"搜索 {title} 时出错: {e}"))
                continue

            results = search_data.get('results', [])
            if not results:
                self.stdout.write(self.style.WARNING(f"未找到连续剧：{title}"))
                continue

            # 简单取搜索结果第一条（如需更精确匹配可进一步筛选）
            first_result = results[0]
            tmdb_id = first_result['id']

            # 2. 根据 tmdb_id 获取连续剧详情
            detail_url = f"https://api.themoviedb.org/3/tv/{tmdb_id}"
            detail_params = {
                'api_key': tmdb_api_key,
                'language': 'en-US',
                'append_to_response': 'external_ids'
            }
            try:
                time.sleep(0.1)
                detail_response = requests.get(detail_url, params=detail_params)
                detail_response.raise_for_status()
                detail_data = detail_response.json()
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"获取连续剧详情 {tmdb_id} 时出错: {e}"))
                continue

            # 3. 解析连续剧详情数据
            tv_name = detail_data.get('name', title)
            first_air_date_str = detail_data.get('first_air_date', '')
            if first_air_date_str:
                try:
                    first_air_date = datetime.datetime.strptime(first_air_date_str, '%Y-%m-%d').date()
                except ValueError:
                    first_air_date = None
            else:
                first_air_date = None

            genres = detail_data.get('genres', [])
            tv_genre = genres[0]['name'] if genres else 'Unknown'

            # 此处设置 type 固定为 "tv"，ArtworkType 模型中需有对应记录
            type_str = 'tv'
            artwork_type, _ = ArtworkType.objects.get_or_create(artwork_type=type_str)

            tv_overview = detail_data.get('overview', '')
            # 取连续剧创作者作为编剧信息（可能有多个，拼接成字符串）
            creators = detail_data.get('created_by', [])
            tv_writer = ', '.join([creator.get('name') for creator in creators]) if creators else ''

            countries = detail_data.get('origin_country', [])
            # 注意：TV详情中的 origin_country 返回的是国家代码列表，如 ["US"]
            tv_country = countries[0] if countries else 'Unknown'

            # 取第一家制作公司作为发行商
            production_companies = detail_data.get('production_companies', [])
            tv_publisher = production_companies[0]['name'] if production_companies else 'Unknown'

            imdb_id = detail_data.get('external_ids', {}).get('imdb_id', '')
            vote_count = detail_data.get('vote_count', 0)
            vote_average = detail_data.get('vote_average', 0)
            tv_average_rate = {'vote_average': vote_average}

            # 检查数据库中是否已存在相同 IMDb ID 的连续剧（根据需要也可用 TMDB ID 判断）
            if imdb_id and TvShows.objects.filter(tvshow_imdb=imdb_id).exists():
                self.stdout.write(self.style.WARNING(f"连续剧 {imdb_id} 已存在，跳过。"))
                continue

            # 4. 创建连续剧记录
            tv_show = TvShows.objects.create(
                tvshow_name=tv_name,
                tvshow_release_year=first_air_date,
                tvshow_genre=tv_genre,
                type=artwork_type,
                tvshow_description=tv_overview,
                tvshow_writer=tv_writer,
                tvshow_country=tv_country,
                tvshow_publisher=tv_publisher,
                tvshow_imdb=imdb_id,
            )

            # 5. 处理海报图片
            poster_path = detail_data.get('poster_path', '')
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                try:
                    img_response = requests.get(poster_url)
                    if img_response.status_code == 200:
                        extension = os.path.splitext(poster_path)[1] or '.jpg'
                        file_name = f"{imdb_id}{extension}" if imdb_id else f"tmdb_tv_{tmdb_id}{extension}"
                        tv_show.tvshow_cover_image.save(file_name, ContentFile(img_response.content), save=True)
                except requests.RequestException as e:
                    self.stdout.write(self.style.ERROR(f"下载海报 {poster_url} 出错: {e}"))
            self.stdout.write(self.style.SUCCESS(f"连续剧数据添加成功：{tv_name}"))
        self.stdout.write(self.style.SUCCESS("所有连续剧处理完毕！"))
