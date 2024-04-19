import requests
import json
from tqdm import tqdm
import re
import aiohttp
import asyncio
import httpx
import asyncio
import urllib.parse
import execjs
import datetime
import os
from multiprocessing import Process


class DyApiDownloader:
    def __init__(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        main_path = dirname.replace("\\", '/')
        self.DouYinCookies = "ttwid=1%7C3UtF-qneFEBjIHPIIyqSkXqZX2ck8oxwacwbxFPtXeo%7C1711063795%7C2754df694da7a7bbdf125168d5945218a9b8ff284b558cfa19117dc4dce3fdc3; IsDouyinActive=true; home_can_add_dy_2_desktop=%220%22; dy_swidth=1835; dy_sheight=1147; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1835%2C%5C%22screen_height%5C%22%3A1147%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A16%2C%5C%22device_memory%5C%22%3A0%2C%5C%22downlink%5C%22%3A%5C%22%5C%22%2C%5C%22effective_type%5C%22%3A%5C%22%5C%22%2C%5C%22round_trip_time%5C%22%3A0%7D%22; strategyABtestKey=%221712719612.217%22; msToken=oxHVRRQWlfcMd0qxo8wiAj1tJIHFabhq1XOh9DVvQ58oxBwbCGnBwQHxp-haC4mw5OQJi91v2pox0jKbbE8vgm6iZvymn0ztfGaThiXDglsowW_CG6Uss2phY377eSE=; passport_csrf_token=25b422fb8a1a9bc347f618c90b956abb; passport_csrf_token_default=25b422fb8a1a9bc347f618c90b956abb; bd_ticket_guard_client_web_domain=2; GlobalGuideTimes=%221712569923%7C0%22; odin_tt=d485a667b6241f02ca1d683ea28a86c2ca1b0fdb39b31dd30bf81ff75f33c5a578f022fb719c6429ba8464ab5cbc7537dcddaaf3defda4b26c9e3b37a54272f0ebb24a5021285f8b886ba9825d97af05; n_mh=13KNPUKNEzoW3A4J-OLRxfal2zj1GbF-vJUFPs3WSIY; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=66d53989a3f243291aa66d25c9c09cd6; LOGIN_STATUS=1; __security_server_data_status=1; store-region=us; store-region-src=uid; d_ticket=47f85db73b2c2b14359c189c1813a59f8c466; my_rd=2; stream_player_status_params=%22%7B%5C%22is_auto_play%5C%22%3A0%2C%5C%22is_full_screen%5C%22%3A0%2C%5C%22is_full_webscreen%5C%22%3A0%2C%5C%22is_mute%5C%22%3A1%2C%5C%22is_speed%5C%22%3A1%2C%5C%22is_visible%5C%22%3A0%7D%22; __live_version__=%221.1.1.9068%22; live_use_vvc=%22false%22; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%2C%22isForcePopClose%22%3A1%7D; xgplayer_user_id=145124503600; s_v_web_id=verify_luop8tbv_378419a4_20c9_f688_db00_a0edb906bd3d; download_guide=%223%2F20240407%2F1%22; SEARCH_RESULT_LIST_TYPE=%22single%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCTFFUdWdBbEg4Q1NxRENRdE9QdnN6K1pSOVBjdnBCOWg5dlp1VDhSRU1qSFFVNEVia2dOYnRHR0pBZFZ3c1hiak5EV01WTjBXd05CWEtSbTBWNDI4eHc9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoxfQ%3D%3D; tt_scid=yOPz66EFkYWVxEZdzlp2oXz8-93ZXFI3QBoGe-QiJy5FRMrzYTEobhpvfx4a.X9N3954; msToken=6HzG-uXu_cIXQcSmsAlfdTG0FB7nv8rH_rlt7_J_wnxrmkKqUNpkaW_PdESzG56g1WWbwhpACRAA03qYKXm2ghww8R2zNchjHKEQ3P6WIJvfaSkpzgLYEQMcrjKLkIA=; __ac_nonce=0661606fc0043e518c105; __ac_signature=_02B4Z6wo00f01ijouYwAAIDDa9gg7RRXqrYo2b0AAOw6LEFj2PgR7B-bsW-.G1T6BExjYP5wGiFF27ouN.9EpEhOXNiYVANCKknwXm-8Sh1xYqGlQipz2XfVtBsxRgPyLtOatlJjFvKY0n7vda"

        self.api_download = 'http://localhost:8000/download/'
        self.douyin_video_data = 'http://localhost:8000/douyin_video_data/'
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }
        self.proxies = None
        self.douyin_api_headers = {
            'accept-encoding': 'gzip, deflate, br',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'Referer': 'https://www.douyin.com/',
            # 如果抖音接口不返回数据，可能是因为cookie过期，需要更新cookie/If the Douyin interface does not return data, it may be because the cookie has expired and needs to be updated
            'cookie': self.DouYinCookies
        }
        self.url_type_code_dict = {
            # 抖音/Douyin
            2: 'image',
            4: 'video',
            68: 'image',
            # TikTok
            0: 'video',
            51: 'video',
            55: 'video',
            58: 'video',
            61: 'video',
            150: 'image'
        }
        self.filename_length = 30
        self.douyin_download_dir_path = f'{main_path}/downloads/douyin/'
        self.douyin_download_user_dir_path = f'{main_path}/downloads/douyin/user/'
        self.douyin_download_video_dir_path = f'{main_path}/downloads/douyin/video/'
        self.douyin_download_image_dir_path = f'{main_path}/downloads/douyin/image/'
        if not os.path.exists(self.douyin_download_dir_path):
            os.makedirs(self.douyin_download_dir_path)
        if not os.path.exists(self.douyin_download_user_dir_path):
            os.makedirs(self.douyin_download_user_dir_path)
        if not os.path.exists(self.douyin_download_video_dir_path):
            os.makedirs(self.douyin_download_video_dir_path)
        if not os.path.exists(self.douyin_download_image_dir_path):
            os.makedirs(self.douyin_download_image_dir_path)

        self.douyin_url_file = f'{main_path}/抖音下载链接.txt'
        self.post_url_file = '抖音用户所有视频.txt'

    def get_url(self, text: str):
        try:
            # 从输入文字中提取索引链接存入列表/Extract index links from input text and store in list
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            # 判断是否有链接/Check if there is a link
            if len(url) > 0:
                return url[0]
        except Exception as e:
            print('Error in get_url:', e)
            return None

    def generate_x_bogus_url(self, url: str, headers: dict):
        query = urllib.parse.urlparse(url).query
        xbogus = execjs.compile(open('./X-Bogus.js').read()).call('sign', query, headers['User-Agent'])
        new_url = url + "&X-Bogus=" + xbogus
        return new_url

    def relpath(self, file):
        """ Always locate to the correct relative path. """
        from sys import _getframe
        from pathlib import Path
        frame = _getframe(1)
        curr_file = Path(frame.f_code.co_filename)
        return str(curr_file.parent.joinpath(file).resolve())

    # 转换链接/convert url
    async def convert_share_urls(self, url: str):
        # 检索字符串中的链接/Retrieve links from string
        url = self.get_url(url)
        # 判断是否有链接/Check if there is a link
        if url is None:
            print('无法检索到链接/Unable to retrieve link')
            return None
            # 判断是否为抖音分享链接/judge if it is a douyin share link
        if 'douyin' in url:
            """
            抖音视频链接类型(不全)：
            1. https://v.douyin.com/MuKhKn3/
            2. https://www.douyin.com/video/7157519152863890719
            3. https://www.iesdouyin.com/share/video/7157519152863890719/?region=CN&mid=7157519152863890719&u_code=ffe6jgjg&titleType=title&timestamp=1600000000&utm_source=copy_link&utm_campaign=client_share&utm_medium=android&app=aweme&iid=123456789&share_id=123456789
            抖音用户链接类型(不全)：
            1. https://www.douyin.com/user/MS4wLjABAAAAbLMPpOhVk441et7z7ECGcmGrK42KtoWOuR0_7pLZCcyFheA9__asY-kGfNAtYqXR?relation=0&vid=7157519152863890719
            2. https://v.douyin.com/MuKoFP4/
            抖音直播链接类型(不全)：
            1. https://live.douyin.com/88815422890
            """
            if 'v.douyin' in url:
                # 转换链接/convert url
                # 例子/Example: https://v.douyin.com/rLyAJgf/8.74
                url = re.compile(r'(https://v.douyin.com/)\w+', re.I).match(url).group()
                print('正在通过抖音分享链接获取原始链接...')
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=self.headers, proxy=self.proxies, allow_redirects=False,
                                               timeout=10) as response:
                            if response.status == 302:
                                url = response.headers['Location'].split('?')[0] if '?' in response.headers[
                                    'Location'] else \
                                    response.headers['Location']
                                print('获取原始链接成功, 原始链接为: {}'.format(url))
                                return url
                except Exception as e:
                    print('获取原始链接失败！')
                    print(e)
                    # return None
                    raise e
            else:
                print('该链接为原始链接,无需转换,原始链接为: {}'.format(url))
                return url

    async def get_douyin_video_id(self, original_url: str):
        """
        获取视频id
        :param original_url: 视频链接
        :return: 视频id
        """
        # 正则匹配出视频ID
        try:
            video_url = await self.convert_share_urls(original_url)
            # 链接类型:
            # 视频页 https://www.douyin.com/video/7086770907674348841
            if '/video/' in video_url:
                key = re.findall('/video/(\d+)?', video_url)[0]
                # print('获取到的抖音视频ID为: {}'.format(key))
                return key
            # 发现页 https://www.douyin.com/discover?modal_id=7086770907674348841
            elif 'discover?' in video_url:
                key = re.findall('modal_id=(\d+)', video_url)[0]
                # print('获取到的抖音视频ID为: {}'.format(key))
                return key
            # 直播页
            elif 'live.douyin' in video_url:
                # https://live.douyin.com/1000000000000000000
                video_url = video_url.split('?')[0] if '?' in video_url else video_url
                key = video_url.replace('https://live.douyin.com/', '')
                # print('获取到的抖音直播ID为: {}'.format(key))
                return key
            # note
            elif 'note' in video_url:
                # https://www.douyin.com/note/7086770907674348841
                key = re.findall('/note/(\d+)?', video_url)[0]
                # print('获取到的抖音笔记ID为: {}'.format(key))
                return key
        except Exception as e:
            print('获取抖音视频ID出错了:{}'.format(e))
            return None

    # 获取单个抖音视频数据/Get single Douyin video data
    # @retry(stop=stop_after_attempt(4), wait=wait_fixed(7))
    async def get_douyin_video_data(self, video_id: str):
        """
        :param video_id: str - 抖音视频id
        :return:dict - 包含信息的字典
        """
        try:
            # 构造访问链接/Construct the access link
            # parameters provided by https://github.com/Johnserf-Seed
            domain = "https://www.douyin.com"
            endpoint = "/aweme/v1/web/aweme/detail/"
            query_body = {
                "aweme_id": video_id,
                "device_platform": "webapp",
                "aid": "6383",
                "channel": "channel_pc_web",
                "pc_client_type": 1,
                "version_code": "170400",
                "version_name": "17.4.0",
                "cookie_enabled": "true",
                "screen_width": 1920,
                "screen_height": 1080,
                "browser_language": "zh-CN",
                "browser_platform": "Win32",
                "browser_name": "Edge",
                "browser_version": "117.0.2045.47",
                "browser_online": "true",
                "engine_name": "Blink",
                "engine_version": "117.0.0.0",
                "os_name": "Windows",
                "os_version": "10",
                "cpu_core_num": 12,
                "device_memory": 8,
                "platform": "PC",
                "downlink": 10,
                "effective_type": "4g",
                "round_trip_time": 100,
                "msToken": "Hello From Evil0ctal!"
            }
            # 将参数编码为 URL 查询字符串
            query_string = urllib.parse.urlencode(query_body, quote_via=urllib.parse.quote)
            api_url = urllib.parse.urljoin(domain, endpoint) + "?" + query_string
            api_url = self.generate_x_bogus_url(url=api_url, headers=self.douyin_api_headers)
            # 访问API/Access API
            print("正在请求抖音视频API: {}".format(api_url))
            # 使用httpx请求
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url, headers=self.douyin_api_headers, timeout=10)
                response = response.json()
                print(response)
                # 获取视频数据/Get video data
                video_data = response["aweme_detail"]
                return video_data
        except Exception as e:
            raise ValueError(f"获取抖音视频数据出错了: {e}")

    """__________________________________________⬇️工具⬇️______________________________________"""

    # 时间戳转日期
    async def timestamp_to_date(self, timestamp):
        # 将时间戳转换为datetime对象
        date_time = datetime.datetime.fromtimestamp(timestamp)
        # 格式化日期
        date = date_time.strftime('%Y-%m-%d_%H-%M-%S')
        return date

    async def create_folder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    async def validateTitle(self, title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

    def photo_downloader(self, url, path):
        print(url)
        r = requests.get(url, stream=True)
        # with open(path, 'wb') as f:
        #     f.write(r.content)
        total = int(r.headers.get('content-length', 0))
        with open(path, 'wb') as file, tqdm(
                desc=path.split('/')[-1],
                total=total,
                unit='iB',
                unit_scale=True,
                unit_divisor=512,
        ) as bar:
            for data in r.iter_content(chunk_size=512):
                size = file.write(data)
                bar.update(size)

    """__________________________________________⬇️API 本地获取视频信息⬇️______________________________________"""

    async def get_douyin_video_download_data_api(self, url):
        # url = await self.convert_share_urls(text)
        douyin_video_url = url
        prefix = "true"
        watermark = "false"
        api_download_url = f'{self.api_download}?url={douyin_video_url}&prefix={prefix}&watermark={watermark}'
        response = requests.get(api_download_url)
        return response

    async def get_douyin_video_data_api(self, url):
        douyin_video_url = url
        api_douyin_video_data = f'{self.douyin_video_data}?douyin_video_url={douyin_video_url}'
        response = requests.get(api_douyin_video_data)
        response = response.json()
        return response

    async def video_wb_downloader(self, video_res, path):
        total = int(video_res.headers.get('content-length', 0))
        with open(path, 'wb') as file, tqdm(
                desc=path.split('/')[-1],
                total=total,
                unit='iter',
                unit_scale=True,
                unit_divisor=512,
        ) as bar:
            for data in video_res.iter_content(chunk_size=512):
                size = file.write(data)
                bar.update(size)

    async def douyin_url_to_video(self, text):
        # downloads_path = self.douyin_download_video_dir_path
        length = self.filename_length
        original_url = await self.convert_share_urls(text)
        video_data = await self.get_douyin_video_data_api(original_url)
        url_type_code = video_data["aweme_list"][0]['aweme_type']
        url_type = self.url_type_code_dict.get(url_type_code)
        if url_type == 'video':
            print('url的类型为【视频】')
            print("正在处理抖音视频数据...")
            downloads_path = self.douyin_download_video_dir_path
            create_time = video_data["aweme_list"][0]["create_time"]
            create_time = await self.timestamp_to_date(create_time)
            nickname = video_data["aweme_list"][0]["author"]["nickname"]
            desc = video_data["aweme_list"][0]["desc"]
            if len(desc) >= length:
                desc = await self.validateTitle(desc[:length])
            video_name = f'【{nickname}】_{create_time}_{desc}'
            video_path = f'{downloads_path}{video_name}.mp4'
            print(video_path)
            video_res = await self.get_douyin_video_download_data_api(original_url)
            await self.video_wb_downloader(video_res, video_path)
        if url_type == 'image':
            print('url的类型为【图文】')
            print("正在处理抖音图片数据...")
            downloads_path = self.douyin_download_image_dir_path

            no_watermark_image_list = []
            watermark_image_list = []

            data = video_data["aweme_list"][0]
            for i in data['images']:
                no_watermark_image_list.append(i['url_list'][0])
                watermark_image_list.append(i['download_url_list'][0])
            create_time = video_data["aweme_list"][0]["create_time"]
            create_time = await self.timestamp_to_date(create_time)
            nickname = video_data["aweme_list"][0]["author"]["nickname"]
            desc = video_data["aweme_list"][0]["desc"]
            if len(desc) >= length:
                desc = await self.validateTitle(desc[:length])
            image_name = f'【{nickname}】_{create_time}_{desc}'
            # print(image_name)
            image_path = f'{self.douyin_download_image_dir_path}{image_name}/'
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            # print(image_path)
            image_url_list = enumerate(no_watermark_image_list)
            for image in image_url_list:
                index = image[0]
                url = image[1]
                path = f'{image_path}{desc}_{index}.webp'
                if not os.path.exists(path):
                    self.photo_downloader(url, path)
                else:
                    print(f'{path}【已存在】')

        else:
            print('url的类型为未知，无法处理')
    async def douyin_url_to_video_user(self, text):
        # downloads_path = self.douyin_download_video_dir_path
        length = self.filename_length
        original_url = await self.convert_share_urls(text)
        video_data = await self.get_douyin_video_data_api(original_url)
        url_type_code = video_data["aweme_list"][0]['aweme_type']
        url_type = self.url_type_code_dict.get(url_type_code)
        if url_type == 'video':
            print('url的类型为【视频】')
            print("正在处理抖音视频数据...")
            nickname = video_data["aweme_list"][0]["author"]["nickname"]
            downloads_path = f'{self.douyin_download_user_dir_path}{nickname}/'
            create_time = video_data["aweme_list"][0]["create_time"]
            create_time = await self.timestamp_to_date(create_time)
            desc = video_data["aweme_list"][0]["desc"]
            if len(desc) >= length:
                desc = await self.validateTitle(desc[:length])
            video_name = f'【{nickname}】_{create_time}_{desc}'
            video_path = f'{downloads_path}{video_name}.mp4'.replace("\n", '')
            print(video_path)
            if not os.path.exists(downloads_path):
                os.makedirs(downloads_path)
            if not os.path.exists(video_path):
                # print(video_path)
                video_res = await self.get_douyin_video_download_data_api(original_url)
                await self.video_wb_downloader(video_res, video_path)
            else:
                print(f'{video_name}【已存在】')
        if url_type == 'image':
            print('url的类型为【图文】')
            print("正在处理抖音图片数据...")
            nickname = video_data["aweme_list"][0]["author"]["nickname"]
            downloads_path = f'{self.douyin_download_user_dir_path}{nickname}/'

            no_watermark_image_list = []
            watermark_image_list = []

            data = video_data["aweme_list"][0]
            for i in data['images']:
                no_watermark_image_list.append(i['url_list'][0])
                watermark_image_list.append(i['download_url_list'][0])
            create_time = video_data["aweme_list"][0]["create_time"]
            create_time = await self.timestamp_to_date(create_time)
            desc = video_data["aweme_list"][0]["desc"]
            if len(desc) >= length:
                desc = await self.validateTitle(desc[:length])
            image_name = f'【{nickname}】_{create_time}_{desc}'
            image_path = f'{downloads_path}{image_name}'.replace("\n", '')
            print(image_path)
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            # print(image_path)
            image_url_list = enumerate(no_watermark_image_list)
            for image in image_url_list:
                index = image[0]
                url = image[1]
                path = f'{image_path}/{desc}_{index}.webp'.replace("\n", '')
                if not os.path.exists(path):
                    self.photo_downloader(url, path)
                else:
                    print(f'{path}【已存在】')

        else:
            print('url的类型为未知，无法处理')

    async def douyin_download_from_urlfile(self):
        process_list = []
        with open(self.douyin_url_file, 'r', encoding='utf-8') as f:
            url_list = f.readlines()
        for text in url_list:
            await self.douyin_url_to_video(text)

    async def douyin_download_user_post(self):
        process_list = []
        with open(self.post_url_file, 'r', encoding='utf-8') as f:
            url_list = f.readlines()
        for text in url_list:
            test = text.replace('\n', '')
            url = f'https://www.douyin.com/video/{text.split("/")[-1]}'
            print(url)
            await self.douyin_url_to_video_user(url)


async def main():
    text = "https://v.douyin.com/iYXcDrn6/"
    api = DyApiDownloader()
    await api.douyin_download_from_urlfile()
async def user_main():
    api = DyApiDownloader()
    await api.douyin_download_user_post()

if __name__ == '__main__':
    # asyncio.run(main())
    asyncio.run(user_main())
