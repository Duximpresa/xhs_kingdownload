import os
from PIL import Image
from multiprocessing import Process


def get_all_file(path):
    file_list = []
    walks = os.walk(path)
    for root, dirs, files in walks:
        for filename in files:
            # print(os.path.join(root, filename))
            file_list.append(os.path.join(root, filename))
    return file_list


def get_photo(path, suffix):
    photo_list = []
    file_list = get_all_file(path)
    for file in file_list:
        if file.lower().endswith(f'{suffix}'):
            photo_list.append(file)
            # print(file)
    return photo_list


def convert_images_JPG(photo_file):
    try:
        im = Image.open(photo_file)
        im_rgb = im.convert('RGB')
        photo_name = os.path.splitext(photo_file)[0]
        photo_short_name = photo_name.split('\\')[-1]
        photo_file_name = f'{photo_name}.jpg'
        if not os.path.isfile(photo_file_name):
            im_rgb.save(f'{photo_file_name}.jpg', quality=95)
            print(f'【{photo_short_name}】转换成功')
        else:
            print(f'{photo_short_name} 【已存在】')
    except Exception as e:
        print(f'图片：{photo_file}转换失败: {e}')


def convert_images_in_folder(path, suffix):
    photo_list = get_photo(path, suffix=suffix)
    index = 0
    process_list = []
    for photo_file in photo_list:
        p = Process(target=convert_images_JPG, args=(photo_file,))
        p.start()
        process_list.append(p)
        if index % 100 == 0:
            for process in process_list:
                process.join()
            process_list = []
        index += 1


def main():
    path = r'H:\DuximpresaProject\Pycharm\test2\小红书\downloads\photo'
    suffix = 'webp'
    convert_images_in_folder(path, suffix)


if __name__ == '__main__':
    main()
    # photo_test_main()
