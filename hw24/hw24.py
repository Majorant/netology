
# ДЗ2.4

# Задание
# мне нужно отыскать файл среди десятков других
# я знаю некоторые части этого файла (на память или из другого источника)
# я ищу только среди .sql файлов
# 1. программа ожидает строку, которую будет искать (input())
# после того, как строка введена, программа ищет её во всех файлах
# выводит список найденных файлов построчно
# выводит количество найденных файлов
# 2. снова ожидает ввод
# поиск происходит только среди найденных на этапе 1
# 3. снова ожидает ввод
# ...
# Выход из программы программировать не нужно.
# Достаточно принудительно остановить, для этого можете нажать Ctrl + C


import glob
import os.path
from chardet.universaldetector import UniversalDetector
import chardet

def output(lst):
	'''вывод на экран найденного'''
	for fi in lst:
		print(fi)
	print('всего: {}'.format(len(lst)))


def search(lst, txt):
	'''посик текста в файлов
	lst - список файлов, в которых ищем текст txt'''
	files = []
	for fi in lst:
		if text_in_file(fi, txt):
			files.append(fi)
	return files


def check_encoding(filename):
	'''определяем кодировку файла'''
	with open(filename, 'rb') as f:
		return chardet.detect(f.read())['encoding']
	# построчно нельзя, можно ошибиться с кодировкой
	# detector = UniversalDetector()
	# detector.reset()
	# with open(filename, 'rb') as f:
	# 	for line in f:
	# 		detector.feed(line)
	# 		if detector.done:
	# 			detector.close()
	# 			return detector.result['encoding']


def text_in_file(filename, txt):
	'''search text in file'''
	encode = check_encoding(filename)
	#encode = 'utf8'
	with open(filename, 'r', encoding=encode) as f:
		for line in f:
			if txt in line:
				return True
	return False


def main_func():
	'''основная функция'''
	work_dir = input('с какой папкой будем работать? (1 - Migrations, 2 - Advanced Migrations): ')
	if work_dir == '1':
		migrations = 'Migrations'
	elif work_dir == '2':
		migrations = 'Advanced Migrations'
	else:
		print('извините, не удалось распознать ваш выбор.')
		return
	# папка с файлом, который запускаем
	local_path = os.path.dirname(os.path.realpath(__file__))
	# путь до файлов
	path = os.path.join(local_path, migrations, "*.sql")
	files = glob.glob(path)
	while True:
		# выход по Ctrl+C
		search_text = input('введите строку для поиска: ')
		files = search(files, search_text)
		output(files)


main_func()
