'''
# ДЗ 2.3
# программа по заданным четырём файлам в формате json (xml)
# выводит топ10 чаще всего встречающихся слов
'''

'''
file -bi newsit.json
text/plain; charset=unknown-8bit
file -bi newsfr.json
text/html; charset=iso-8859-1
file -bi newscy.json
text/html; charset=iso-8859-1
file -bi newsafr.json
text/html; charset=utf-8

import urllib.parse

url = "https://ru.wikipedia.org/wiki/%D0%9C%D0%B5%D1%82%D0%BE%D0%B4_%D0%BC%D0%BD%D0%BE%D0%B6%D0%B8%D1%82%D0%B5%D0%BB%D0%B5%D0%B9_%D0%9B%D0%B0%D0%B3%D1%80%D0%B0%D0%BD%D0%B6%D0%B0"
print(urllib.parse.unquote(url))
'''
# import urllib.parse
import codecs
import json
import re


# пытаемся понять кодировку файла
def check_coding(file_name):
    '''возвращает кодировку в файле
    для этого открывает его, проверяет есть ли слово 'новости'' в заголовке
    '''
    codings = [
        'utf8',
        'koi8-r',
        'iso8859_5',
        'cp1251'
        ]
    for code in codings:
        try:
            with codecs.open(file_name, encoding=code) as news:
                js = json.load(news)
                if 'новости' in js['rss']['channel']['title'].lower().split():
                    return code
                else:
                    continue
        # что произойдёт в windows?
        except UnicodeDecodeError:
            continue
    print('не получилось определить кодировку для ', file_name)
    return None


def json_text_to_list(file_name):
    '''на вход получает имя файла,
    возвращает список слов со всех статей в lowercase'''
    words_lst = []
    # определяем кодировку файла
    encode = check_coding(file_name)
    # если не смогли определить кодировку
    if encode is None:
        return None
    with codecs.open(file_name, encoding=encode) as news:
        js = json.load(news)
        for article in js['rss']['channel']['item']:
            # получаем список слов в одной статье
            # извращение с if/else возникло, потому что формат json для файлов разный
            # для newsit.json - нет __cdata
            # не смог придумать, как сделать красивее
            if type(article['description']) is dict:
                temp_lst = remove_waste_chars(article['description']['__cdata'])
            elif type(article['description']) is str:
                temp_lst = remove_waste_chars(article['description'])
            #: article data
            words_lst += temp_lst
    return words_lst


def remove_waste_chars(string):
    '''несмотря на название, выбирает слова по регулярному выражению:
    r'[а-яА-Я]{6,}'''
    # регулярное выражение: слова на русском, более 6 символов
    reg = r'[а-яА-Я]{6,}'
    words_lst = re.findall(reg, string, re.IGNORECASE)
    return words_lst


def top10(words_lst):
    '''возвращает список топ10 слов по содержанию входного списка'''
    dict_words = {}
    for word in words_lst:
        if word.lower() in dict_words:
            dict_words[word.lower()] += 1
        else:
            dict_words[word.lower()] = 1
    # https://docs.python.org/3/howto/sorting.html - помни, это крутой туториал )
    # сортируем по кортежам (ключ, значение) ('слово', сколько раз встретилось),
    # key= выбираем параметр, по которому сортировать
    # lambda - def func(x): return x[1]
    sorted_pairs = sorted(dict_words.items(), key=lambda pair: pair[1], reverse=True)[:10]
    top10_words = []
    for i in sorted_pairs:
        top10_words.append(i[0])
    return top10_words

def print_top10(words_lst):
    '''печатает топ10 слов'''
    for i in range(0, len(words_lst)):
        if i != len(words_lst)-1:
            print(words_lst[i], end=', ')
        else:
            print(words_lst[i], end='.\n')



def file_handle():
    '''основная функция
    пробегает по списку файлов, высчитывает и выводит топ10 слов, встречающихся
    в текстах статей'''
    file_list_json = [
        'newsfr.json',
        'newsafr.json',
        'newscy.json',
        'newsit.json'
    ]
    for js_file in file_list_json:
        print('для файла \"{}\" top-10 слов:'.format(js_file))
        #top10_words = json_handle(js_file)
        words_lst = json_text_to_list(js_file)
        if words_lst is not None:
            top10_words = top10(words_lst)
            print_top10(top10_words)
        else:
            print('к сожалению, не удалось определить кодировку файла.')
        print()

file_handle()
