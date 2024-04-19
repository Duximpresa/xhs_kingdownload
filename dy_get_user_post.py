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

"""
xpath to get the user post links:
//div[@data-e2e='user-post-list']/ul/li/div//a/@href

"""
import asyncio


class DouYinUserPost:
    def __init__(self):
        dirname, filename = os.path.split(os.path.abspath(__file__))
        main_path = dirname.replace("\\", '/')
        self.post_url_file = '抖音用户所有视频.txt'
        self.douyin_download_user_dir_path = f'{main_path}/downloads/douyin/user/'
        if not os.path.exists(self.douyin_download_user_dir_path):
            os.makedirs(self.douyin_download_user_dir_path)

    async def douyin_download_user_post(self):
        process_list = []
        with open(self.post_url_file, 'r', encoding='utf-8') as f:
            url_list = f.readlines()
        for text in url_list:
            print(text)


async def main():
    api = DouYinUserPost()
    await api.douyin_download_user_post()


if __name__ == '__main__':
    asyncio.run(main())
