contacts = [
    {'name': 'Geektech', 'phone': '0507052018'},
    {'name': 'Служба спасения', 'phone': '911'},
    {'name': 'Пожарная служба', 'phone': '101'},
]
def create():
    name = input('Введите имя:')
    phone = input('Введите номер:')

    contacts.append({'name':name,'phone': phone})

    print('Контакт добавлен')

print('======================')

def edit():
    for i, contact in contacts:
        print(f'{i} - {contact('name')}: {contact('phone')}')

    try:
        index = int(input('Ввеите индекс:'))

        contacts[index]['name'] = input('Введите новое имя:')
        contacts[index]['phone'] = input('Введите новый номер телефона:')

        print('Контакт изменён')

    except IndexError:
        print('Не правильный индекс')

def delete():
    for i, contact in contacts:
        print(f'{i} - {contact('name')}: {contact('phone')}')

    try:
        index = int(input('Введите индекс:'))

        contacts.index

        print('Контакт удалён')
    except IndexError:
        print('Индекс не найден')

ten = []

for i in range(1, 11):
    ten.append(i)

print(ten)

        



