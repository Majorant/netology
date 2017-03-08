'''
# ДЗ 2.2
# программа по заданным четырём файлам в формате json (xml)
# выводит топ10 чаще всего встречающихся слов
'''


# import urllib.parse
import codecs
import json
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError


def isxml(file_name):
    '''прроверяет является ли файл xml по расширению )'''
    # если подать json формат в файле bb.xml, то упадёт
    if file_name.endswith('.xml'):
        return True
    else:
        return False


def check_encoding(file_name):
    '''возвращает кодировку в файле
    для этого открывает его, проверяет есть ли слово 'новости'' в заголовке
    '''
    # по внутренним ощещениями это жуткий костыль, но ничего интереснее не придумал (
    # решение из группы:
    # import chardet
    # def check_encoding(news_file):
    # rawdata = open(news_file, "rb").read()
    # result = chardet.detect(rawdata)
    # open(news_file).close()
    # return result['encoding']
    codings = [
        'utf-8',
        'koi8-r',
        'iso8859_5',
        'cp1251'
        ]
    for code in codings:
        # if *.xml
        if isxml(file_name):
            try:
                parser = ET.XMLParser(encoding=code)
                tree = ET.parse(file_name, parser=parser)
                root = tree.getroot()
                # если есть ожидаемые слова
                if 'новости' in root[0][0].text.lower().split():
                    return code
                else:
                    continue
            # при попытке парсинга могут попасться символы, которые not allowed:
            # set(['&#x08;', '&#x0E;', '&#x1E;', '&#x1C;', '&#x18;', '&#x04;',
            #'&#x0A;', '&#x0C;', '&#x16;', '&#x14;', '&#x06;', '&#x00;', '&#x10;
            #', '&#x02;', '&#x0D;', '&#x1D;', '&#x0F;', '&#x09;', '&#x1B;',
            #'&#x05;', '&#x15;', '&#x01;', '&#x03;'])
            except ParseError:
                continue
        else:
            # if *.json
            try:
                with codecs.open(file_name, encoding=code) as news:
                    text = json.load(news)
                    if 'новости' in text['rss']['channel']['title'].lower().split():
                        return code
                    else:
                        continue
            # что произойдёт в windows?
            except UnicodeDecodeError:
                continue
    print('не получилось определить кодировку для ', file_name)
    return None


def xml_text_to_list(file_name, encode):
    '''для файлов формата xml возвращает список слов в статьях
    на вход получает имя файла *.xml, кодировку
    возвращает список слов со всех статей в lowercase'''
    words_lst = []
    parser = ET.XMLParser(encoding=encode)
    tree = ET.parse(file_name, parser=parser)
    root = tree.getroot()
    # ходим по корню, ищем description - это статьи
    for new in root.iter('description'):
        temp_lst = remove_waste_chars(new.text)
        words_lst += temp_lst
    return words_lst


def json_text_to_list(file_name, encode):
    '''для файлов формата json возвращает список слов в статьях
    на вход получает имя файла *.json, кодировку
    возвращает список слов со всех статей в lowercase'''
    words_lst = []
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


def text_to_list(file_name):
    '''на вход получает имя файла,
    возвращает список слов со всех статей в lowercase'''
    words_lst = []
    # определяем кодировку файла
    encode = check_encoding(file_name)
    # если не смогли определить кодировку
    if encode is None:
        return None
    # выбираем чем пользоваться в зависимости от файла
    if isxml(file_name):
        return xml_text_to_list(file_name, encode)
    else:
        return json_text_to_list(file_name, encode)


def remove_waste_chars(string):
    '''выбирает слова по регулярному выражению:
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
    '''печатает слова из списка в строку'''
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
        'newsit.json',
        'newsfr.xml',
        'newsafr.xml',
        'newscy.xml',
        'newsit.xml'
    ]
    for js_file in file_list_json:
        print('для файла \"{}\" top-10 слов:'.format(js_file))
        #top10_words = json_handle(js_file)
        words_lst = text_to_list(js_file)
        if words_lst is not None:
            top10_words = top10(words_lst)
            print_top10(top10_words)
        else:
            print('к сожалению, не удалось определить кодировку файла.')
        print()


file_handle()
