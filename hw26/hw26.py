#
# convert input.jpg -resize 200 output.jpg

import glob
import os
import subprocess


def resize_photo(photos, path, size = 200):
    for photo in photos:
        output = os.path.join(path, os.path.basename(photo))
        subprocess.run(['convert', photo, '-resize', str(size), output])
    return


def main_func():
    # define, where photos
    #print('введите путь до папки с фотографиями и расширения, с которыми предполагается работать чрез пробел:')
    #inp_lst = input('input path to photos and extensions (default: Source and *.jpg)')

    realpath = os.path.dirname(os.path.realpath(__file__))
    # меняем рабочую папку на папку с файлом
    os.chdir(realpath)
    # input_path = 'Source'
    # extension = '*.jpg'
    path_to_photo = os.path.join('Source', '*.jpg')
    photos_lst = glob.glob(path_to_photo)
    # создаём папку Result/, если её нет
    result_path = os.path.join('Result')
    # try:
    #     os.mkdir(result_path)
    # except FileExistsError:
    #     pass
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    resize_photo(photos_lst, result_path)

main_func()
