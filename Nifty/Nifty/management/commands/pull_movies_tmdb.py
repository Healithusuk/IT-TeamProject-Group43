import os
import time
import datetime
import requests
import pandas as pd
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from allModels.models import Movies, ArtworkType
from django.conf import settings

class Command(BaseCommand):
    help = '从 TMDB API 获取电影数据并填充数据库'

    def handle(self, *args, **kwargs):
        # 请替换为你自己的 TMDB API Key
        tmdb_api_key = 'cf336e21d837d093d66ae7cc55001b2c'

        # 读取 CSV 文件，示例中假设 CSV 中有一个 "Title" 列
        df = pd.read_csv(r'Nifty\management\commands\imdb-movies-dataset.csv', encoding='latin1')
        movie_titles = df['Title'].tolist()

        for title in movie_titles:
            self.stdout.write(f"正在搜索电影：{title}")
            # 1. 通过 search/movie 接口搜索电影
            search_url = "https://api.themoviedb.org/3/search/movie"
            search_params = {
                'api_key': tmdb_api_key,
                'query': title,
                'language': 'en-US',  # 可根据需要修改语言
                'page': 1,
            }
            try:
                time.sleep(1)  # 简单防止请求过于频繁，可根据需要调整
                search_response = requests.get(search_url, params=search_params)
                search_response.raise_for_status()
                search_data = search_response.json()
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"搜索 {title} 时出错: {e}"))
                continue

            results = search_data.get('results', [])
            if not results:
                self.stdout.write(self.style.WARNING(f"未找到电影：{title}"))
                continue

            # 简单取搜索结果的第一条，若需更精确匹配可根据年份等信息再筛选
            first_result = results[0]
            tmdb_id = first_result['id']

            # 2. 根据 tmdb_id 获取电影详情
            detail_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
            detail_params = {
                'api_key': tmdb_api_key,
                'language': 'en-US',
                'append_to_response': 'external_ids'  # 用于获取 IMDb ID 等信息
            }

            try:
                time.sleep(1)
                detail_response = requests.get(detail_url, params=detail_params)
                detail_response.raise_for_status()
                detail_data = detail_response.json()
            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"获取电影详情 {tmdb_id} 时出错: {e}"))
                continue

            # 3. 从详情数据中解析所需字段
            # 标题
            movie_name = detail_data.get('title', title)
            # 上映日期
            release_date_str = detail_data.get('release_date', '')
            if release_date_str:
                try:
                    movie_release_year = datetime.datetime.strptime(release_date_str, '%Y-%m-%d').date()
                except ValueError:
                    movie_release_year = None
            else:
                movie_release_year = None
            # 类型（Genres）取第一个为例
            genres = detail_data.get('genres', [])
            genre_name = genres[0]['name'] if genres else 'Unknown'

            # 作品类型（此处直接写死为 movie，若你有其他分类逻辑可再做区分）
            type_str = 'movie'
            artwork_type, _ = ArtworkType.objects.get_or_create(artwork_type=type_str)

            # 电影简介
            movie_description = detail_data.get('overview', '')

            # 导演、演员等信息需要进一步调用 /credits 或者你可以仅存储在 description 中
            # 此处示例只展示获取 external_ids 来拿 IMDb ID
            imdb_id = detail_data.get('external_ids', {}).get('imdb_id', '')

            # 片长（runtime，单位是分钟）
            runtime = detail_data.get('runtime', 0)

            # 国家/地区（production_countries）
            countries = detail_data.get('production_countries', [])
            movie_country = countries[0]['name'] if countries else 'Unknown'

            # 4. 通过 /credits 接口获取导演和演员信息
            credits_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits"
            credits_params = {
                'api_key': tmdb_api_key,
                'language': 'en-US'
            }
            try:
                time.sleep(1)
                credits_response = requests.get(credits_url, params=credits_params)
                credits_response.raise_for_status()
                credits_data = credits_response.json()
            except requests.RequestException as e:
                self.stdout.write(self.style.WARNING(f"获取电影 {tmdb_id} 的 credits 时出错: {e}"))
                credits_data = {}

            # 解析导演：取 crew 中 job 为 "Director" 的第一个
            director = ''
            for person in credits_data.get('crew', []):
                if person.get('job') == 'Director':
                    director = person.get('name')
                    break

            # 解析演员：取 cast 前 5 名，拼接为字符串
            cast = credits_data.get('cast', [])
            actors_list = [actor.get('name') for actor in cast[:5]]
            actors_str = ', '.join(actors_list)
            # 如果你的 Movies 模型有 tmdb_id 字段，也可以先判断 tmdb_id
            if imdb_id and Movies.objects.filter(movie_imdb=imdb_id).exists():
                self.stdout.write(self.style.WARNING(f"电影 {imdb_id} 已存在，跳过。"))
                continue

            # 4. 创建电影记录
            movie = Movies.objects.create(
                movie_name=movie_name,
                movie_release_year=movie_release_year,
                movie_genre=genre_name,
                type=artwork_type,
                movie_description=movie_description,
                movie_director=director,  # 若需导演信息，需要调用 /credits 接口进一步获取
                movie_actors=actors_str,    # 同上
                movie_country=movie_country,
                movie_runtime=runtime,
                movie_imdb=imdb_id,  # 这里存 IMDb ID，也可改存 TMDB ID
            )

            # 5. 处理海报图片
            poster_path = detail_data.get('poster_path', '')
            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                try:
                    img_response = requests.get(poster_url)
                    if img_response.status_code == 200:
                        # 为文件名添加后缀，如 .jpg
                        extension = os.path.splitext(poster_path)[1]
                        file_name = f"{imdb_id}{extension}" if imdb_id else f"tmdb_{tmdb_id}{extension}"
                        movie.movie_cover_image.save(file_name, ContentFile(img_response.content), save=True)
                except requests.RequestException as e:
                    self.stdout.write(self.style.ERROR(f"下载海报 {poster_url} 出错: {e}"))

            self.stdout.write(self.style.SUCCESS(f"电影数据添加成功：{movie_name}"))

        self.stdout.write(self.style.SUCCESS("所有电影处理完毕！"))
