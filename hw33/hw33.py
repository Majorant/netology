import requests
import os
import chardet


def translate_it(text, lang=None):
    """
    YANDEX translation plugin
    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param text: <str> text for translation.
    :return: <str> translated text.

    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20170402T082957Z.67a31013eaa770b1.e832ce19af6ad5f53a90387c4be2804f5dff6edc'

    if lang is None:
        lang = 'ru'
    params = {
        'key': key,
        'text': text,
        'lang': lang,
    }
    response = requests.get(url, params=params).json()
    # ' '.join(response.get('text', []))
    return ' '.join(response['text'])


def autodetect_language(text):
    """определяет язык текста"""
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20170402T082957Z.67a31013eaa770b1.e832ce19af6ad5f53a90387c4be2804f5dff6edc'
    hint = ['en', 'fr', 'de', 'es']
    params = {
        'key': key,
        'text': text,
        'hint': hint,
    }
    response = requests.get(url, params=params).json()
    if response['code'] == 200:
        return response['lang']
    else:
        return 'unknown'


def check_encoding(filename):
	"""определяет кодировку файла"""
	with open(filename, 'rb') as f:
		return chardet.detect(f.read())['encoding']


def find_path(string):
    """
    возвращает абсолютный путь к файлам, если он существует.
    иначе возвращает путь к текущей рабочей директории

    """
    path = os.path.join(os.getcwd(), string)
    if os.path.exists(path):
        return path
    else:
        print('указанный путь не существует, используется текущая '
              'папка: {}'.format(os.getcwd()))
        return os.getcwd()


def text_from_file(filename):
    """возвращает текст из файла"""
    encode = check_encoding(filename)
    with open(filename, 'r', encoding=encode) as f:
        return f.read()


def save_to_file(filename, text):
    """сохраняет текст в файл"""
    name = os.path.splitext(filename)[0] + '_translated.txt'
    with open(name, 'w', encoding='utf8') as f:
        f.write(text)


def main():
    """
    основная функция.
    если в качестве входного пути указать файл,
    то переведёт только его,
    если путь, то будет искать там файлы по умолчанию
    ['DE.txt', 'ES.txt', 'FR.txt']

    """
    input_files_path = input('укажите путь к файлам для перевода '
                             '(по умолчанию используется текущая папка): ')
    input_path = find_path(input_files_path)
    if os.path.isfile(input_path):
        lst_texts = []
        input_path, filename = os.path.split(input_path)
        lst_texts.append(filename)
    else:
        lst_texts = ['DE.txt', 'ES.txt', 'FR.txt']

    output_files_path = input('укажите путь, куда сложить переведённый текст '
                              '(по умолчанию используется текущая папка): ')
    output_path = find_path(output_files_path)

    input_lang = input('укажите язык, с которого переводить(en, de, fr), '
                       'по умолчанию переводчик попробует определить текст'
                       'автоматически (рекомендуется): ')
    output_lang = input('укажите язык, на который переводить(en, de, fr), '
                        'по умолчанию \'ru\': ')
    # направление перевода по умолчанию
    if output_lang.lower().strip() == '':
        output_lang = 'ru'
    if input_lang.lower().strip() == '':
        lang = output_lang.lower().strip()
    else:
        lang = input_lang.lower().strip() + '-' + output_lang.lower().strip()

    for txt_file in lst_texts:
        print('работаем с ', txt_file)
        text = text_from_file(os.path.join(input_path, txt_file))
        translated_text = translate_it(text, lang)
        save_to_file(os.path.join(output_path, txt_file), translated_text)


main()
