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
    if (string.strip()[0] == '#') or string == '':
        return True
    else:
        return False


# определяем, блюдо перед нами или ингридиенты.
def isdish(string):
    if string != '' and ' | ' not in string:
        return True
    else:
        return False


# преобразуем ингридиенты из книги в словарь для использования
# ингридиент | сколько | в чём измеряется
def ingridients(string):
    ingr_dic = {}
    try:
        ingr_dic['ingridient_name'] =  string.split(' | ')[0]
        ingr_dic['quantity'] = int(string.split(' | ')[1])
        ingr_dic['measure'] = string.split(' | ')[2]
    except Exception:
        return None
    return ingr_dic


# из книги рецептов формируем словарь, который использовали на лекции.
def recipes_from_cookbook(dishes):
    recipes = {}
    with open('cookbook.txt', 'r') as f:
        for line in f:
            # везде отрезаем символы конца строки и приводим к нижнему регистру
            line = line.strip('\r\n').lower()
            # если это название блюда, не комментарий и
            # в списке блюд на сегодня
            if isdish(line) and not comment(line) and line in dishes:
                recipes[line] = []
                line_in = f.readline().strip('\r\n').lower()
                # вычёркиваем элемент, для которого посчитали набор ингридиентов
                dishes.remove(line)
                # считаем концом рецепта пустую строку
                # или название другого блюда, вдруг кто ошибся
                while not isdish(line_in) and line_in != '':
                    if not comment(line_in):
                        if ingridients(line_in) is not None:
                            recipes[line].append(ingridients(line_in))
                            line_in = f.readline().strip('\r\n').lower()
                        else:
                            print('не удалось распознать строку с ингридиентами\
                             {} для блюда {}'\
                             .format(line_in, line))
                    else:
                        line_in = f.readline().strip('\r\n').lower()
        if dishes != []:
            print('не удалось распознать следующие блюда:')
            [print(x) for x in dishes]
            print()
            return recipes, dishes
        else:
            return recipes, []


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
  for shopt_list_item in shop_list.values():
      print('список продуктов:')
      print('{ingridient_name} {quantity} {measure}'.format(**shopt_list_item))

# main function
def create_shop_list():
    person_count = int(input('введите количество человек: '))
    # если блюда в запросе повторяются, то это скорее всего ошибка, исключим их
    dishes = list(set(input('введите блюда в расчёте на одного человека (через запятую): ').lower().split(', ')))
    print()
    # моя самая большая находка: если передать в функцию просто название
    # списка, а потом с ним чего-нибудь эдакое сотворить!
    # в общем, передаётся, как и в случае с присваиванием
    # только указатель на список. такие дела.
    cook_book, forgotten_recipes = recipes_from_cookbook(dishes.copy())
    # вычёркиваем блюда, которые не нашли в повареной книге
    dishes = list(set(dishes) - set(forgotten_recipes))
    shop_list = get_shop_list_by_dishes(dishes, person_count, cook_book)
    print_shop_list(shop_list)

create_shop_list()
