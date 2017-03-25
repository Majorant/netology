#
# convert input.jpg -resize 200 output.jpg

import glob
import os
import subprocess
import threading
import queue


def one_thread(que):
    """один поток для обработки одной фотографии"""
    while True:
        # берём параметры из очереди
        params = que.get()
        # условие завершения потока
        if params is None:
            return
        subprocess.run(params)
        que.task_done()


def resize_photo(photos, path, size = 200):
    '''функция вызывает внешнюю программу imsgemagick и передаёт параметры
    subprocess.run() работает только в версиях 3,5 и выше'''
    '''функция вызывает внешнюю программу imagemagick и передаёт параметры
    subprocess.run() работает только в версиях 3,5 и выше'''
    # количество потоков
    num_worker_threads = 4
    # очередь
    que = queue.Queue()
    # список потоков
    threads = []
    for i in range(num_worker_threads):
        # создаём поток
        thread = threading.Thread(target=one_thread, args=(que,))
        # запускаем
        thread.start()
        # добавляем в список
        threads.append(thread)
    for photo in photos:
        # os.path.basename(photo) возвращает имя каждго файла
        output = os.path.join(path, os.path.basename(photo))
        # добавляем список команд, которые будет вызывать run() в очередь
        que.put(['convert', photo, '-resize', str(size), output])
    # block until all tasks are done
    # ждём, пока все потоки не завершаться - one_thread
    que.join()
    # пишем в очередь None, каждый поток, когда получит None - завершится.
    for i in range(num_worker_threads):
        que.put(None)
    # нам нет причин ждать завершения всех потоков
    # for thread in threads:
    #     thread.join()
    #     # print(thread.name, 'stopped')


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
