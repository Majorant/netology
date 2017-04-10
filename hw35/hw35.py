from urllib.parse import urlencode, urlparse, urljoin
from pprint import pprint
import requests


AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'
APP_ID = 'ea4e1e951785496f89fbf73450961742'  # Your app_id here

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}
# print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

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

    @property
    def counter_list(self):
        url = urljoin(self._METRIKA_MANAGEMENT_URL, 'counters')
        headers = self.get_header()
        response = requests.get(url, headers=headers)
        # pprint(response.json())
        counter_list = [c['id'] for c in response.json()['counters']]
        return counter_list

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
        visits_count = response.json()['data'][0]['metrics'][0]
        return visits_count

    def get_users_count(self, counter_id):
        """возвращает количество уникальных пользователей"""
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self.get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:users'
        }
        response = requests.get(url, params, headers=headers)
        visits_count = response.json()['data'][0]['metrics'][0]
        return visits_count


metrika = YandexMetrika(TOKEN)
# print('YandexMetrika')
# pprint(YandexMetrika.__dict__)
# print('metrika')
# pprint(metrika.__dict__)

# print(metrika.counter_list)
#
for counter in metrika.counter_list:
    print(metrika.get_visits_count(counter))
    print(metrika.get_pageviews_count(counter))
    print(metrika.get_users_count(counter))
