# яичница, 2 шт яиц, 100гр помидоров
# стейк, мясо 300гр, специи 5 гр, масло 10 мл
# салат, помидоры 100гр, огурцы 100 гр, масло 100мл, лук 1 шт

# cook_book = {
#   'яичница': [
#       {'ingridient_name': 'яйца', 'quantity': 2, 'measure': 'шт.'},
#       {'ingridient_name': 'помидоры', 'quantity': 100, 'measure': 'гр'}
#       ],
#   'стейк':[
#       {'ingridient_name': 'говядина', 'quantity': 300, 'measure': 'гр'},
#       {'ingridient_name': 'специи', 'quantity': 5, 'measure': 'гр'},
#       {'ingridient_name': 'масло', 'quantity': 10, 'measure': 'мл'}
#       ],
#   'салат':[
#       {'ingridient_name': 'помидоры', 'quantity': 100, 'measure': 'гр'},
#       {'ingridient_name': 'огурцы', 'quantity': 100, 'measure': 'гр'},
#       {'ingridient_name': 'масло', 'quantity': 100, 'measure': 'мл'},
#       {'ingridient_name': 'лук', 'quantity': 1, 'measure': 'шт'}
#       ]
#   }


# определяем комментарии на полях повареной книги, читаем между строк
def comment(string):
    '''определяет комментарии на полях повареной книги, читаем между строк'''
    if (string.strip()[0] == '#') or string == '':
        return True
    else:
        return False


# определяет, является ли строка названием блюда
def isdish(string):
    '''определяет, является ли строка названием блюда
    исключает пустые строки;
    элементы, которые встречаются в игридиентах (|);
    комментарии'''
    if string != '' and '|' not in string and not comment(string):
        return True
    else:
        return False


# преобразуем ингридиенты из книги в словарь для использования
# ингридиент | сколько | в чём измеряется
def ingridients(string):
    '''
    преобразуем ингридиенты из книги в словарь для использования
    формат ингридиентов в кулинарной книге:
    ингридиент | сколько | в чём измеряется
    '''
    ingr_dic = {}
    splitted_string = string.split(' | ')
    try:
        ingr_dic['ingridient_name'] =  splitted_string[0]
        ingr_dic['quantity'] = int(splitted_string[1])
        ingr_dic['measure'] = splitted_string[2]
    except ValueError:
        return None
    return ingr_dic


# из книги рецептов формируем словарь, который использовали на лекции.
def recipes_from_cookbook(cookbook_file, dishes=[]):
    '''из книги рецептов формируем словарь,
    проверяет есть ли блюдо сегодня в меню'''
    recipes = {}
    with open(cookbook_file, 'r') as f:
        for line in f:
            # везде отрезаем символы конца строки и приводим к нижнему регистру
            line = line.strip().lower()
            # если в функцию не передали название блюд, т.е. список dishes  пустой,
            # будем считыать весь файл с рецептами
            if not dishes:
                indishes = True
            else:
                indishes = line in dishes
            # если это название блюда, не комментарий и
            # в списке блюд на сегодня - это сомнительный момент, пока оставил
            if isdish(line) and not comment(line) and indishes:
                recipes[line] = []
                line_in = f.readline().strip().lower()
                # считаем концом рецепта пустую строку
                # или название другого блюда, вдруг кто ошибся
                while not isdish(line_in) and line_in != '':
                    if not comment(line_in):
                        if ingridients(line_in) is not None:
                            recipes[line].append(ingridients(line_in))
                            line_in = f.readline().strip().lower()
                        else:
                            print('не удалось распознать строку с ингридиентами \"{}\" для блюда \"{}\"'\
                             .format(line_in, line))
                            line_in = f.readline().strip().lower()
                    else:
                        line_in = f.readline().strip().lower()

        return recipes


# определяем, какие блюда не смогли найти в книге
def check_forgotten(recipes, dishes):
    forgotten_dishes = []
    for dish in dishes:
        if dish not in recipes.keys():
            forgotten_dishes.append(dish)
    return forgotten_dishes


# функция для получения списка продуктов для магазина
def get_shop_list_by_dishes (dishes, person_count, cook_book):
  shop_list = {}
  for dish in dishes:
    for ingridient in cook_book[dish]:
      new_shop_list_item = dict(ingridient)
      new_shop_list_item['quantity'] *= person_count
      if new_shop_list_item['ingridient_name'] not in shop_list:
        shop_list[new_shop_list_item['ingridient_name']] = new_shop_list_item
      else:
        shop_list[new_shop_list_item['ingridient_name']]['quantity'] += new_shop_list_item['quantity']
  return  shop_list


#  print('{} {} {}'.format(shopt_list_item['ingridient_name'], shopt_list_item['quantity'], shopt_list_item['measure']))
def print_shop_list(shop_list):
    print('список продуктов:')
    for shopt_list_item in shop_list.values():
        print('{ingridient_name} {quantity} {measure}'.format(**shopt_list_item))

# main function
def create_shop_list():
    try:
        person_count = int(input('введите количество человек: '))
    except ValueError:
        print('вы ввели не число')
        return
    # если блюда в запросе повторяются, то это скорее всего ошибка, исключим их
    dishes = list(set(input('введите блюда в расчёте на одного человека (через запятую): ').lower().split(', ')))
    print()
    # моя самая большая находка: если передать в функцию просто название
    # списка, а потом с ним чего-нибудь эдакое сотворить!
    # в общем, передаётся, как и в случае с присваиванием
    # только указатель на список. такие дела.
    cookbook_file = 'cookbook.txt'
    cook_book = recipes_from_cookbook(cookbook_file, dishes)
    # вычёркиваем блюда, которые не нашли в повареной книге
    forgotten_recipes = check_forgotten(cook_book, dishes)
    if forgotten_recipes:
        print('рецепты, которые не найдены в повареной книге:')
        for dish in forgotten_recipes:
            print(dish)
    # оставляем в списке только те блюда, рецепты, которых были найдены
    dishes = list(set(dishes) - set(forgotten_recipes))
    shop_list = get_shop_list_by_dishes(dishes, person_count, cook_book)
    print_shop_list(shop_list)

create_shop_list()
