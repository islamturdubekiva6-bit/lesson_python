import random
playr={
    'name':'',
    'hp':100,
    'water':50,
    'food':50,
    'invertory':[]
}
events=[
    {'desc': '💧вы нашли водоем (+20 воды)','type': 'water', 'hp':-5, 'water':20, 'food':-5,'item':"бутылка воды"},
    {'desc': '🎒вы нашли еду (+20 еды)','type':'food','hp':-5,'water':-5, 'food':20,'item':"ягоды"},
    {'desc': '⛺вы отдыхаете (+15 здоровья)','type':'rest', 'hp':15,'water':-5,'food':-5},
    {'desc': '🐾вы попались к хищника (-30 здоровья)','type':'enemy','hp':-30, 'water':-5,'food':-5},
    {'desc': '🍂 вы ничего не нашли (-5 ко всему статов что имеется)','type':'emty','hp':-5,'water':-5,'food':-5},
]
def get_choice(massage):
    while True:
        try:
            choice=int(input(massage))
            if choice in(1,2):
                return choice
            print('ведите 1 или 2')
        except ValueError:
            print('ведите целое число!')
def limit_stat():
    playr['hp'] = min(100, playr['hp'])
    playr['water'] = min(100, playr['water'])
    playr['food'] = min(100, playr['food'])
def show_stat():
    print(f'❤️здоровья{playr["hp"]} |'
          f'🍖еда {playr["food"]} |' 
          f'💧вода {playr["water"]} |' 
          f'🎒инвертарь{playr["invertory"]}')
def item_add(item):
    if item not in playr['invertory']:
        playr['invertory'].append(item)
        print(f'🎒 Вы получили предмет: {item}')
    else:
        print(f'⚠️ У вас уже есть предмет: {item}')
def use_item(item,stat):
    if item in playr['invertory']:
        playr[stat] = min(100, playr[stat] + 20)
        playr['invertory'].remove(item)
        print(f'✅ Вы использовали: {item}')
        return True
    return False
def alive():
    return(
playr['hp']<=0 or
playr['water']<=0 or
playr['food']<=0
)
def water(current_event):
    print('💦1-попить\n💧2-набрать в бутылку')
    if get_choice('ваш выбор: ')==1:
        playr['water'] +=current_event['water']
        playr['hp']+=current_event['hp']
        playr['food']+=current_event['food']
        print('🤤вы выпиваете')
    else:
        playr['hp']+=current_event['hp']
        playr['food']+=current_event['food']
        item_add(current_event['item'])
def food(current_event):
    print('1-сьесть\n2-забрать собой')
    if get_choice('ваш выбор: ')==1:
        playr['water'] +=current_event['water']
        playr['hp']+=current_event['hp']
        playr['food']+=current_event['food']
        print('😋вы кушаете')
    else:
        playr['hp']+=current_event['hp']
        playr['water']+=current_event['water']
        item_add(current_event['item'])
def rest(current_event):
    playr['hp']+=current_event['hp']
    playr['food']+=current_event['food']
    playr['water']+=current_event['water']
    print('💤вы отдыхаете')
    if 'бутылка воды' in playr['invertory']:
        print('🔎Хотите попить из запасов❓')
        print('1 - ✅да (+20💧)')
        print('2 - ❌нет')
        if get_choice('ваш выбор: ')==1:
            use_item('бутылка воды','water')
            print('🤤Вы утолили жажду во время отдыха.')
    if 'ягоды' in playr['invertory']:
        print('🔎Хотите перекусить ягодами❓🍓🍓🍓')
        print('1 - ✅да (+20🍖)')
        print('2 - ❌нет')
        if get_choice('ваш выбор: ')==1:
            use_item('ягоды','food')
            print('😋Вы перекусили на привале.')
def enemy(current_event):
    playr['hp']+=current_event['hp']
    playr['food']+=current_event['food']
    playr['water']+=current_event['water']
    print('⚠️⚠️⚠️вы получили урон от хищника⚠️⚠️⚠️')
def emty(current_event):
    used_water = False
    used_food = False
    if 'бутылка воды' in playr['invertory']:
        print('🔎У вас есть бутылка воды, хотите выпить❓')
        print('1 - ✅да (+20 💧)')
        print('2 - ❌нет')
        if get_choice('ваш выбор: ')==1:
            use_item('бутылка воды','water')
            print('🤤вы выпили воду')
            used_water = True
    if 'ягоды' in playr['invertory']:
        print('🔎У вас есть ягоды, хотите съесть❓🍓🍓🍓')
        print('1 - ✅да (+20🍖)')
        print('2 - ❌нет')
        if get_choice('ваш выбор: ')==1:
            use_item('ягоды','food')
            print('😋вы съели ягоды')
            used_food = True
    if not used_water and not used_food:
        playr['hp']+=current_event['hp']
        playr['food']+=current_event['food']
        playr['water']+=current_event['water']
        print('🍂вы ничего ненаходите')
event_functions={
    'water':water,
    'food':food,
    'rest':rest,
    'enemy':enemy,
    'emty':emty
}
def game():
    print('🌲===ИГРА ВЫЖИВАНИЕ В ЛЕСУУ===🌲')
    try:
        name_input= input('👤ведите имя:').strip()
        playr['name'] = name_input if name_input else 'игрок'
        print(f'\n{playr["name"]},у вас есть 10 дней что бы выжить в лесу❗❗❗')
        for day in range(1,11):
            if alive():
                print('💀вы здохли💀')
                break
            print(f'\n📅 === ДЕНЬ {day}/10 ===')
            show_stat()
            current_event = random.choice(events)
            print(f'🎯 Событие: {current_event["desc"]}')
            event_functions[current_event['type']](current_event)
            limit_stat()
        print('\n=== РЕЗУЛЬТАТ ИГРЫ ===')
        if not alive() and day == 10:
            print('🎉 YOU WIN! 🏆')
        else:
            print('💀 GAME OVER 💀')
        show_stat()
    except (KeyboardInterrupt, EOFError):
        print('\n⚠️ Игра прервана.')
if __name__== '__main__':
    game()