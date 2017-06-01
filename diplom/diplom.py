import requests
from time import sleep
import json
import sys

VERSION = '5.64'
access_token = 'd13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22'
PARAMS = dict(access_token=access_token, v=VERSION)


def user_info(user_ids, par=PARAMS):
    """возвращает реальный id, если был введён никнейм
    или None - если такой никнейм не существует

    """
    params = par.copy()
    params['user_ids'] = user_ids
    response = requests.get('https://api.vk.com/method/users.get', params)
    try:
        return response.json()['response'][0]['id']
    except KeyError:
        return None


def input_test_user():
    """ввод и обработка входных данных, возвращает id пользователя
    или None, если распознать ввод не удалось

    """
    test_id = None
    inp = input('введите ник или id для теста: ')
    try:
        test_id = int(inp)
    except ValueError:
        if inp.lower().startswith('id'):
            test_id = inp[2:]
        else:
            test_id = user_info(inp)

    return test_id


def get_friends(user_id=None, par=PARAMS):
    """возвращает список id друзей пользователей"""
    params = par.copy()
    if user_id:
        params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/friends.get', params)
    return response.json()


def get_groups(user_id=None, par=PARAMS):
    """возвращает id групп, в которых состоит пользователь"""
    params = par.copy()
    if user_id:
        params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/groups.get', params)
    return response.json()


def write_progress(val):
    """функция для работы с командной строкой, организует вывод"""
    sys.stdout.flush()
    sys.stdout.write(val)


def get_target_groups(test_id):
    """возвращает множество групп, в которых состоит пользователь,
    но в которых не состоит никто из его друзей в виде списка id групп

    """
    print('проверка на совпадение групп у друзей')
    groups = set(get_groups(test_id)['response']['items'])
    friends = get_friends(test_id)
    for count, friend_id in enumerate(friends['response']['items'], 1):
        write_progress('\rпроверено {} из {}'.format(count, friends['response']['count']))
        sleep(0.35)
        response = get_groups(friend_id)
        try:
            friend_id_groups = set(response['response']['items'])
            groups -= friend_id_groups
        except KeyError:
            try:
                if response['error']['error_msg'] == 'Too many requests per second':
                    sleep(1)
            except KeyError:
                print('unknown answer in get_target_groups: ', response)
    print()

    return groups


def get_group_name(g_id, par=PARAMS):
    """возвращает название группы"""
    params = par.copy()
    name = ''
    params['group_id'] = g_id
    response = requests.get('https://api.vk.com/method/groups.getById', params).json()
    try:
        if 'deactivated' not in response:
            name = response['response'][0]['name']
    except KeyError:
        try:
            if response['error']['error_msg'] == 'Too many requests per second':
                sleeep(1)
        except KeyError as e:
            print('unknown answer get_group_name: ', response)

    return name


def get_group_count_members(g_id, par=PARAMS):
    """возвращает количество участников в группе"""
    params = par.copy()
    members_count = 0
    params['group_id'] = g_id
    params['count'] = 1
    response = requests.get('https://api.vk.com/method/groups.getMembers', params).json()
    try:
        members_count = response['response']['count']
    except KeyError:
        try:
            if response['error']['error_msg'] == 'Too many requests per second':
                sleep(1)
        except KeyError:
            print('\nunknown answer in get_group_count_members ', response)

    return members_count


def make_output_json_file(groups):
    """функция осбирает выходной файл формата json с описанием групп

    """
    lst_of_groups = []
    print('составление описания групп')
    for count, group_id in enumerate(groups, 1):
        write_progress('\rгруппы {} из {}'.format(count, len(groups)))
        sleep(0.35)
        result_dict = {}
        name = get_group_name(group_id)
        members_count = get_group_count_members(group_id)
        if name and members_count:
            result_dict['name'], result_dict['members_count'], result_dict['gid'] = name, members_count, group_id
            lst_of_groups.append(result_dict)

    print('\nзапись в файл в формате json')
    with open('groups.json', 'w') as output:
        json.dump(lst_of_groups, output, ensure_ascii=False)


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
