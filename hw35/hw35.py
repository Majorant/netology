from urllib.parse import urlencode, urlparse, urljoin
from pprint import pprint
import requests

TOKEN = 'AQAAAAABnnujAAQLkvvGNGEutExkpOhmUpcHsSA'  # token here

class YandexMetrika(object):
    _METRIKA_STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/'
    _METRIKA_MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'
    token = None

    def __init__(self, token):
        self.token = token

    def get_header(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token),
            'User-Agent': 'bb'
        }


class YandexMetrika_management(YandexMetrika):

    @property
    def counter_list(self):
        url = urljoin(self._METRIKA_MANAGEMENT_URL, 'counters')
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        # pprint(response.json())
        counter_list = [c['id'] for c in response.json()['counters']]
        return counter_list


class YandexMetrika_stat(YandexMetrika):

    def __init__(self, token, counter_id):
        self.token = token
        self.counter_id = counter_id

    def get_visits_count(self, counter_id):
        """возвращает количество визитов"""
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:visits'
        }

        response = requests.get(url, params, headers=headers)
        # print(response.headers['Content-Type'])
        # pprint(response.json())
        visits_count = response.json()['data'][0]['metrics'][0]
        return visits_count

    def get_pageviews_count(self, counter_id):
        """возвращает количество просмотров"""
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:pageviews'
        }
        response = requests.get(url, params, headers=headers)
        pageviews_count = response.json()['data'][0]['metrics'][0]
        return pageviews_count

    def get_users_count(self, counter_id):
        """возвращает количество уникальных пользователей"""
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:users'
        }
        response = requests.get(url, params, headers=headers)
        users_count = response.json()['data'][0]['metrics'][0]
        return users_count

ids = YandexMetrika_management(TOKEN)
metrika = YandexMetrika_stat(TOKEN, ids)
# print('YandexMetrika')
# pprint(YandexMetrika.__dict__)
# print('metrika')
# pprint(metrika.__dict__)

# print(metrika.counter_list)
#
for counter in ids.counter_list:
# for counter in metrika.counter_list:
    print(metrika.get_visits_count(counter))
    print(metrika.get_pageviews_count(counter))
    print(metrika.get_users_count(counter))
