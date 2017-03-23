#
# convert input.jpg -resize 200 output.jpg

import glob
import os
import subprocess


def resize_photo(photos, path, size = 200):
    '''функция вызывает внешнюю программу imsgemagick и передаёт параметры
    subprocess.run() работает только в версиях 3,5 и выше'''
    for photo in photos:
        # os.path.basename(photo) возвращает имя каждго файла
        output = os.path.join(path, os.path.basename(photo))
        subprocess.run(['convert', photo, '-resize', str(size), output])


def modify_extensions(extensions):
    '''возвращает список расширений вида "*.smth"
    '''
    # exten = extensions.copy()
    # вот тут вопрос
    for i in range(len(extensions)):
        if not extensions[i].startswith('*.'):
            extensions[i] = '*.' + extensions[i]
        else:
            continue
    return extensions


def input_handle(extensions):
    '''функция возвращает список с расширениями, по которым будем искать файлы'''
    default_extension = ['*.jpg']
    if not extensions:
        return default_extension
    else:
        return modify_extensions(extensions)


def create_photos_lst(path, extensions):
    '''функция возвращает список всех файлов, размер которых надо изменить'''
    photos = []
    for extension in extensions:
        photos_path = os.path.join(path, extension)
        photos += glob.glob(photos_path)
    return photos


def main_func():
    '''основная функция'''
    # define, where photos
    inp_lst = input('введите расширения файлов с картинками через пробел: (by default jpg): ').split()
    extension = input_handle(inp_lst)
    # меняем рабочую папку на папку с файлом
    realpath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(realpath)
    # каталог с фотографиями
    path_to_photo = os.path.join(realpath, 'Source')
    # каталог для результатов
    result_path = os.path.join(realpath, 'Result')
    # получаем список всех изображений
    photos_lst = create_photos_lst(path_to_photo, extension)
    # создаём папку Result/, если её нет
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    # меняем размер изображений, складываем в result_path
    resize_photo(photos_lst, result_path)

    
main_func()
