#
# convert input.jpg -resize 200 output.jpg

import glob
import os
import subprocess


def resize_photo(photos, path, size = 200):
    for photo in photos:
        # print(photo)
        output = os.path.join(path, os.path.basename(photo))
        subprocess.run(['convert', photo, '-resize', str(size), output])
    return


def modify_extensions(extensions):
    exten = extensions.copy()
    for i in range(len(exten)):
        if not exten[i].startswith('*.'):
            exten[i] = '*.' + exten[i]
        else:
            continue
    return exten


def input_handle(extensions):
    default_extension = ['*.jpg']
    if not extensions:
        return default_extension
    else:
        return modify_extensions(extensions)


def create_photos_lst(path, extensions):
    photos = []
    for extension in extensions:
        photos_path = os.path.join(path, extension)
        photos += glob.glob(photos_path)
    return photos


def main_func():
    # define, where photos
    print('введите расширения, с которыми предполагается работать, через пробел:')
    inp_lst = input('input extensions (by default jpg): ').split()
    extension = input_handle(inp_lst)

    # меняем рабочую папку на папку с файлом
    realpath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(realpath)
    # каталог с фотографиями
    path_to_photo = os.path.join(realpath, 'Source')
    # каталог для результатов
    result_path = os.path.join(realpath, 'Result')
    photos_lst = create_photos_lst(path_to_photo, extension)
    # создаём папку Result/, если её нет
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    resize_photo(photos_lst, result_path)
main_func()
