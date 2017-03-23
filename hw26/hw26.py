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


def input_handle(input_string):
    param_lst = input_string.split()
    default_params = ['Source', '*.jpg']
    if not param_lst:
        return default_params[0], default_params[1]
    elif len(param_lst) == 1:
        return param_lst[0], default_params[1]
    elif len(param_lst) == 2:
        return param_lst[0], param_lst[1]
    else:
        return param_lst[0], param_lst[1:]

def create_photos_lst(path, extensions):
    photos = []
    print(path)
    print(extensions)
    if os.path.exists(path):
        for extension in extensions:
            photos_path = os.path.join(path, extension)
            photos.append(glob.glob(path))
    else:
        print('заданный путь не существут')
        exit(1)


def main_func():
    # define, where photos
    print('введите путь до папки с фотографиями и расширения, с которыми предполагается работать, чрез пробел:')
    inp_lst = input('input path to photos and extensions (default: "Source jpg": ')
    input_path, extension = input_handle(inp_lst)
    path_to_photo = os.path.join(os.path.curdir, input_path)

    # меняем рабочую папку на папку с файлом
    realpath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(realpath)
    # каталог для результатов
    result_path = os.path.join(realpath, 'Result')

    photos_lst = create_photos_lst(path_to_photo, extension)
    print(input_path)
    print(extension)

    print(photos_lst)
    # создаём папку Result/, если её нет
    # try:
    #     os.mkdir(result_path)
    # except FileExistsError:
    #     pass
    if not os.path.exists(result_path):
        os.mkdir(result_path)


    resize_photo(photos_lst, result_path)

main_func()
