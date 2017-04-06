import osa

def temperature(filename):
    url = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'
    client = osa.client.Client(url)
    temperature_lst = []
    with open(filename, 'r', encoding='utf8') as temps:
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
    with open(filename, 'r', encoding='utf8') as travel_list:
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
    with open(filename, 'r', encoding='utf8') as travel_list:
        for line in travel_list.readlines():
            # MOSCOW-LONDON: 1,553.86 mi
            distance = line.split()[1].replace(',','')
            response = client.service.ChangeLengthUnit(fromLengthUnit='Miles',
                                toLengthUnit='Kilometers', LengthValue=distance)
            travel_distance_sum += response
    return round(travel_distance_sum, 2)


def miles_handle(string):
    return

def main():
    avg_temp = temperature('temps.txt')
    print('средняя температура за неделю {:.2f} градусов Цельсия'.format(avg_temp))
    # travel_sum = travel_currencies('currencies.txt')
    print('на путешествие будет затрачено {}руб.'.format(travel_sum))
    travel_distance_sum = travel_distance('travel.txt')
    print('путешествие займёт вас на {} км'.format(travel_distance_sum))



main()
