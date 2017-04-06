import osa
import os
import chardet

def check_encoding(filename):
	"""определяет кодировку файла"""
	with open(filename, 'rb') as f:
		return chardet.detect(f.read())['encoding']


def temperature(filename):
    url = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'
    client = osa.client.Client(url)
    temperature_lst = []
    encode = check_encoding(filename)
    with open(filename, 'r', encoding=encode) as temps:
        for line in temps.readlines():
            temp = line.split()[0]
            response = client.service.ConvertTemp(Temperature=temp,
                        FromUnit='degreeFahrenheit', ToUnit='degreeCelsius')
            temperature_lst.append(float(response))
    if temperature_lst:
        return sum(temperature_lst)/len(temperature_lst)
    else:
        return None


def travel_currencies(filename):
    url = 'http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL'
    client = osa.client.Client(url)
    travel_sum = 0
    encode = check_encoding(filename)
    with open(filename, 'r', encoding=encode) as travel_list:
        for line in travel_list.readlines():
            value = line.split()[1]
            fromCurrency = line.split()[2]
            response = client.service.ConvertToNum(fromCurrency=fromCurrency,
                                toCurrency='RUB', amount=value, rounding=True)
            travel_sum += response
    return round(travel_sum + 0.5)


def travel_distance(filename):
    url = 'http://www.webservicex.net/length.asmx?WSDL'
    client = osa.client.Client(url)
    travel_distance_sum = 0.0
    encode = check_encoding(filename)
    with open(filename, 'r', encoding=encode) as travel_list:
        for line in travel_list.readlines():
            # MOSCOW-LONDON: 1,553.86 mi
            distance = line.split()[1].replace(',','')
            response = client.service.ChangeLengthUnit(fromLengthUnit='Miles',
                                toLengthUnit='Kilometers', LengthValue=distance)
            travel_distance_sum += response
    return round(travel_distance_sum, 2)


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


def take_path():
    input_files_path = input('укажите путь к файлу с данными ')
    input_path = find_path(input_files_path)
    if os.path.isfile(input_path):
        return input_path
    else:
        print('это не файл')
        return None


def main():
    while(True):
        input_test = input('введите, с чем работаем (1 - температура, 2 - курсы валют, '
                           '3 - расстояние, 4 - выход): ')
        if input_test == '1':
            filename = take_path()
            if filename is not None:
                avg_temp = temperature('temps.txt')
                print('средняя температура за неделю {:.2f} градусов Цельсия'.format(avg_temp))
        elif input_test == '2':
            filename = take_path()
            if filename is not None:
                travel_sum = travel_currencies('currencies.txt')
                print('на путешествие будет затрачено {}руб.'.format(travel_sum))

        elif input_test == '3':
            filename = take_path()
            if filename is not None:
                travel_distance_sum = travel_distance('travel.txt')
                print('путешествие займёт вас на {} км'.format(travel_distance_sum))
        elif input_test == '4':
            return
        else:
            print('не удалось распознать запрос, выход - 4')


main()
