import requests
from lxml import etree
import re
import os
import time
from tqdm import tqdm
from xhs_tool import get_photo_or_video_url, get_one_note_info

# url = 'https://www.xiaohongshu.com/explore/6319ef23000000001103e270'
dirname, filename = os.path.split(os.path.abspath(__file__))
dirname = dirname.replace("\\", '/')

main_path = dirname + '/' + 'downloads/'

if not os.path.exists(main_path):
    os.makedirs(main_path)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Cookie": "abRequestId=6ef85dc1-1c40-589d-8504-063d4f54bc5e; a1=18a4b5eddaduelccwwn0j6a3ryi2x40s6tjegdr7q50000282515; webId=b7ee7530bf9643b128745c721b0d167c; gid=yY04D2ddDWKdyY04D2dff9fF0f7d1SSEEI8VVWAK0qFv3d28JC48Mk888JYJ2y28Df8WJDiJ; web_session=040069b28284056f69aec6682f374b4cc19a6e; webBuild=3.10.6; unread={%22ub%22:%2264f55296000000001f038e5b%22%2C%22ue%22:%226519655a000000001c015f9e%22%2C%22uc%22:29}; galaxy_creator_session_id=wV6ul0OjeIzGyKLpYrWfmu171shxwZXMgs8t; galaxy.creator.beaker.session.id=1696351267132030252659; xsecappid=xhs-pc-web; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=d06487ef-1b57-4e45-b63f-f019711495a9",
    "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}


def get_page_source(url, headers):
    resp = requests.get(url=url, headers=headers)
    return resp.text


def find_images(page_source):
    # page_source = get_page_source(url=url, headers=headers)

    # obj_face_images = re.compile('"imageScene":"CRD_WM_WEBP","url":.*?"}')
    obj_face_images = re.compile('"imageScene":"WB_DFT","url":.*?"}')
    obj_images = re.compile('"imageScene":"CRD_PRV_WEBP","url":.*?"}')
    face_images = obj_face_images.findall(page_source)
    images = obj_images.findall(page_source)

    list = []

    for j in face_images:
        keyword = r'u002F'
        newword = ''
        j = j.replace(keyword, newword)
        j = j.replace('"imageScene":"WB_DFT","url":"', "")
        j = j.replace('"}', "")
        list.append(j)

    return list


def get_name(url):
    page_source = get_page_source(url=url, headers=headers)
    tree = etree.HTML(page_source)
    title = tree.xpath('//title/text()')[0]

    return title


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


def download_photo(image_url, image_path, title):
    r = requests.get(image_url)
    filename = image_path + '/' + title + '.webp'
    print(filename)
    with open(filename, 'wb') as f:
        f.write(r.content)


def xhs_images_downloader(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Cookie": "abRequestId=6ef85dc1-1c40-589d-8504-063d4f54bc5e; a1=18a4b5eddaduelccwwn0j6a3ryi2x40s6tjegdr7q50000282515; webId=b7ee7530bf9643b128745c721b0d167c; gid=yY04D2ddDWKdyY04D2dff9fF0f7d1SSEEI8VVWAK0qFv3d28JC48Mk888JYJ2y28Df8WJDiJ; web_session=040069b28284056f69aec6682f374b4cc19a6e; webBuild=3.10.6; unread={%22ub%22:%2264f55296000000001f038e5b%22%2C%22ue%22:%226519655a000000001c015f9e%22%2C%22uc%22:29}; galaxy_creator_session_id=wV6ul0OjeIzGyKLpYrWfmu171shxwZXMgs8t; galaxy.creator.beaker.session.id=1696351267132030252659; xsecappid=xhs-pc-web; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=d06487ef-1b57-4e45-b63f-f019711495a9",
        "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }

    # if not os.path.exists('downloads/'):
    #     os.makedirs('downloads/')

    # page_source = get_page_source(url=url, headers=headers)
    images_list = []
    for i in range(5):
        page_source = get_page_source(url=url, headers=headers)
        image_list = find_images(page_source)
        for j in image_list:
            if j not in images_list:
                images_list.append(j)

    # for u in images_list:
    #     print(u)

    title = get_name(url)
    title = validateTitle(title)
    print(title)

    path = main_path + "photo" + "/" + title + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    count = 0
    for image_url in images_list:
        count += 1
        image_path = path + title + f"_{count}.webp"
        image_url = image_url.replace('http', 'https')
        image_url = image_url.replace("\\", '/')
        photo_downloader(image_url, image_path)
        print(image_path)

def xhs_images_downloader_api(img_list, note):
    title = validateTitle(note.title)
    nickname = validateTitle(note.nickname)

    path = f"{main_path}photo/{nickname}_{title}/"
    if not os.path.exists(path):
        os.makedirs(path)

    for img in img_list:
        # print(img[0], img[1]['info_list'][1]['url'])
        image_url = img[1]['info_list'][1]['url']
        image_path = path + title + f"_{img[0]}.webp"
        if not os.path.exists(image_path):
            photo_downloader(image_url, image_path)
        else:
            print(f'图片【{nickname}_{title}】已存在')


def xhs_bulk_download():
    url_list_file = dirname + '/下载链接.txt'
    with open(url_list_file, 'r') as f:
        line = f.readlines()
    for url in line:
        xhs_url = url.strip()
        if detection_photo_video(xhs_url):
            xhs_videos_downloader(url=xhs_url)
        else:
            xhs_images_downloader(url=xhs_url)

def xhs_bulk_download_api():
    url_list_file = dirname + '/下载链接.txt'
    with open(url_list_file, 'r') as f:
        line = f.readlines()
    for url in line:
        url = url.replace("\n", "")
        note = get_one_note_info(url)
        note_type = note.note_type
        if note_type == 'normal':
            print(f'【笔记类型】：图文')
            img_list = []
            imgs = enumerate(note.image_list)
            for img in imgs:
                img_list.append(img)
            xhs_images_downloader_api(img_list, note)
            print(f'【所有图片下载完毕】', '-' * 50)
        elif note_type == 'video':
            print(f'【笔记类型】：视频')
            video_url = note.video_addr
            xhs_videos_downloader_api(video_url, note)
            print(f'【视频下载完毕】', '-'*50)



def get_video_url(url):
    # url = 'https://www.xiaohongshu.com/explore/651fc922000000002301a724'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Cookie": "abRequestId=6ef85dc1-1c40-589d-8504-063d4f54bc5e; a1=18a4b5eddaduelccwwn0j6a3ryi2x40s6tjegdr7q50000282515; webId=b7ee7530bf9643b128745c721b0d167c; gid=yY04D2ddDWKdyY04D2dff9fF0f7d1SSEEI8VVWAK0qFv3d28JC48Mk888JYJ2y28Df8WJDiJ; web_session=040069b28284056f69aec6682f374b4cc19a6e; webBuild=3.10.6; unread={%22ub%22:%2264f55296000000001f038e5b%22%2C%22ue%22:%226519655a000000001c015f9e%22%2C%22uc%22:29}; galaxy_creator_session_id=wV6ul0OjeIzGyKLpYrWfmu171shxwZXMgs8t; galaxy.creator.beaker.session.id=1696351267132030252659; xsecappid=xhs-pc-web; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=d06487ef-1b57-4e45-b63f-f019711495a9",
        "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "https://www.google.com/",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin"
    }

    page_source = get_page_source(url, headers)
    # print(page_source)
    obj_video_url = re.compile('originVideoKey":"(.*?)"')
    # obj_video_url = re.compile('"backupUrls":.*?",')
    originVideoKey = obj_video_url.findall(page_source)[0]
    originVideoKey = originVideoKey.replace("\\u002F", "/")
    # print(originVideoKey)
    video_url = "http://sns-video-bd.xhscdn.com/" + originVideoKey
    # print(video_url)

    return video_url


def video_downloader(url, path):
    print(path)
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    # with open(path, 'wb') as f:
    #     for chunk in res.iter_content(chunk_size=10240):
    #         f.write(chunk)
    with open(path, 'wb') as file, tqdm(
            desc=path.split('/')[-1],
            total=total,
            unit='iter',
            unit_scale=True,
            unit_divisor=512,
    ) as bar:
        for data in resp.iter_content(chunk_size=512):
            size = file.write(data)
            bar.update(size)

def photo_downloader(url, path):
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

def xhs_videos_downloader(url):
    video_url = get_video_url(url)
    title = get_name(url)
    title = validateTitle(title)
    print(title)
    path = main_path + 'video' + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    video_path = path + title + '.mp4'
    # print(video_path)
    video_downloader(video_url, video_path)

def xhs_videos_downloader_api(video_url, note):
    title = validateTitle(note.title)
    nickname = validateTitle(note.nickname)
    path = f'{main_path}video/'
    if not os.path.exists(path):
        os.makedirs(path)
    video_path = f'{path}{nickname}_{title}.mp4'
    if not os.path.exists(path):
        print(f"【视频开始下载】:{nickname}_{title}")
        video_downloader(video_url, video_path)
    else:
        print(f'视频【{nickname}_{title}】已存在')

def detection_photo_video(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Cookie": "abRequestId=6ef85dc1-1c40-589d-8504-063d4f54bc5e; a1=18a4b5eddaduelccwwn0j6a3ryi2x40s6tjegdr7q50000282515; webId=b7ee7530bf9643b128745c721b0d167c; gid=yY04D2ddDWKdyY04D2dff9fF0f7d1SSEEI8VVWAK0qFv3d28JC48Mk888JYJ2y28Df8WJDiJ; web_session=040069b28284056f69aec6682f374b4cc19a6e; webBuild=3.10.6; unread={%22ub%22:%2264f55296000000001f038e5b%22%2C%22ue%22:%226519655a000000001c015f9e%22%2C%22uc%22:29}; galaxy_creator_session_id=wV6ul0OjeIzGyKLpYrWfmu171shxwZXMgs8t; galaxy.creator.beaker.session.id=1696351267132030252659; xsecappid=xhs-pc-web; websectiga=2845367ec3848418062e761c09db7caf0e8b79d132ccdd1a4f8e64a11d0cac0d; sec_poison_id=d06487ef-1b57-4e45-b63f-f019711495a9",
        "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Referer": "https://www.google.com/",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin"
    }

    page_source = get_page_source(url, headers)
    # print(page_source)
    obj_video_url = re.compile('originVideoKey":"(.*?)"')
    # obj_video_url = re.compile('"backupUrls":.*?",')
    originVideoKey = obj_video_url.findall(page_source)
    if not originVideoKey:
        return False
    else:
        return True


def main():
    xhs_url = 'https://www.xiaohongshu.com/explore/650a5583000000001e020c07'
    xhs_images_downloader(url=xhs_url)


def main2():
    xhs_bulk_download()


def main_test_01():
    url = 'https://www.xiaohongshu.com/explore/652010d5000000001d03b550'
    detection_photo_video(url)

def main3():
    xhs_bulk_download_api()

if __name__ == '__main__':
    main3()
    # main_test_01()

