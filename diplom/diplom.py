import requests
from time import sleep
import json
import sys

VERSION = '5.65'
access_token = 'd13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22'
PARAMS = dict(access_token=access_token, v=VERSION)


def user_info(user_ids, par=PARAMS):
    """возвращает реальный id, если был введён никнейм
    или None - если такой никнейм не существует

    """
    params = par.copy()
    params['user_ids'] = user_ids
    response = requests.get('https://api.vk.com/method/users.get', params)
    if response.status_code == 200:
        try:
            return response.json()['response'][0]['id']
        except KeyError:
            return None
    else:
        print('response code error in user_info()', response.status_code)
        return None


def input_test_user():
    """ввод и обработка входных данных, возвращает id пользователя
    или None, если распознать ввод не удалось

    """
    inp = input('введите ник или id для теста: ')
    try:
        return int(inp)
    except ValueError:
        if inp.lower().startswith('id'):
            try:
                return int(inp[2:])
            except ValueError:
                return user_info(inp)
        else:
            return user_info(inp)


def get_friends(user_id=None, par=PARAMS):
    """возвращает список id друзей пользователей"""
    params = par.copy()
    if user_id:
        params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/friends.get', params)
    if response.status_code == 200:
        try:
            return response.json()['response']['items']
        except KeyError:
            try:
                if response.json()['error']['error_msg'] == 'Too many requests per second':
                    sleep(1)
                    return None
                else:
                    print('error in get_friends()', response.json()['error']['error_msg'])
                    return None
            except KeyError:
                print('unknown answer get_friends(): ', response.json())
    else:
        print('response code error in get_friends()', response.status_code)
        return None


def string_groups_request(user_ids):
    """возвращает строку для запроса с помощью метода execute"""
    lst = ['API.groups.get({\"user_id\":' + str(u) + '}),' for u in user_ids]
    string = 'return[' + ''.join(lst) + '];'
    return string


def get_groups(user_ids, par=PARAMS):
    """возвращает id групп, в которых состоит пользователь"""
    groups = []
    params = par.copy()
    # если запрос для одного пользователя
    if isinstance(user_ids, int):
        user_ids = [user_ids]
    params['code'] = string_groups_request(user_ids)
    response = requests.get('https://api.vk.com/method/execute', params)
    if response.status_code == 200:
        try:
            for item in response.json()['response']:
                if item:
                    groups += item['items']
        except KeyError:
            try:
                if response.json()['error']['error_msg'] == 'Too many requests per second':
                    sleep(1)
                else:
                    print('error in get_groups()', response.json()['error']['error_msg'])
            except KeyError:
                print('unknown answer in get_groups(): ', response.json())
    else:
        print('response code error in get_groups()', response.status_code)
    return groups


def write_progress(val):
    """функция для работы с командной строкой, организует вывод"""
    sys.stdout.flush()
    sys.stdout.write(val)


def get_target_groups(test_id):
    """возвращает множество групп, в которых состоит пользователь,
    но в которых не состоит никто из его друзей в виде списка id групп

    """
    print('проверка на совпадение групп у друзей')
    groups = set(get_groups(test_id))
    friends = get_friends(test_id)
    # максимум запросов в методе API execute: 25
    if friends:
        for count in range(len(friends)//25+1):
            write_progress('\rзапрос API для поиска групп друзей {}'.format(count+1))
            sleep(0.35)
            friend_id_groups = set(get_groups(friends[count*25:(count+1)*25]))
            groups -= friend_id_groups
    print()

    return groups


def get_groups_info(groups, par=PARAMS):
    """возвращает информацию о группах, переданных в функцию в виде списка id

    """
    params = par.copy()
    groups_info = []
    groups = list(groups)
    # ограничение VK на количество групп в одном запросе 500
    for count in range(len(groups)//500+1):
        write_progress('\rзапрос API для получения информации о группе {}'.format(count+1))
        sleep(0.35)
        st = ','.join(map(str, groups[count*500:(count+1)*500]))
        code = 'return[API.groups.getById({\"group_ids\": "' + st + '\", \"fields\": \"members_count\"})];'
        params['code'] = code
        response = requests.get('https://api.vk.com/method/execute', params)
        if response.status_code == 200:
            try:
                groups_info += response.json()['response'][0]
            except KeyError:
                try:
                    if response.json()['error']['error_msg'] == 'Too many requests per second':
                        sleep(1)
                    else:
                        print('error in get_groups()', response.json()['error']['error_msg'])
                except KeyError:
                    print('unknown answer get_groups_info(): ', response.json())
        else:
            print('response code error in get_groups_info()', response.status_code)

    return groups_info


def make_output_json_file(groups):
    """функция собирает выходной файл формата json с описанием групп

    """
    lst_of_groups = []
    print('составление описания групп')
    if groups:
        for group in get_groups_info(groups):
            result_dict = {'gid': group['id'],
                           'name': group['name'],
                           'members_count': group['members_count']}
            lst_of_groups.append(result_dict)
        print('\nзапись в файл в формате json')
        with open('groups.json', 'w') as output:
            json.dump(lst_of_groups, output, ensure_ascii=False)
    else:
        print('групп, в которых состоит пользователь, но в которых нет его друзей не найдено')


def main():
    """Основная функция"""
    id_for_test = input_test_user()
    if id_for_test:
        groups = get_target_groups(id_for_test)
        make_output_json_file(groups)
        print('работа завершена')
    else:
        print('не удалось распознать ник или id пользователя')


main()
