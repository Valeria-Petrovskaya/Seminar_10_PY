import random
from aiogram import Bot, Dispatcher 
from aiogram.types import Message
from aiogram.utils import executor

bot = Bot('5826927112:AAFm8jUdxpBP9VyVri_hckRk4EYtEhGKbDs')
dp = Dispatcher(bot)

async def start_bot(_):
    print('Бот запущен')

executor.start_polling(dp, skip_updates=True, on_startup=start_bot)

dp.message_handler(commands=['start', 'начать'])
async def mes_start(message: Message):
    await message.answer(text=f'{message.from_user.first_name}, привет! Сегодня мы с тобой поиграем в интересную игру')

dp.message_handler(commands=['new'])
async def mes_new_game(message: Message):
    total = 150
    await message.answer(text=f'И так, на столе {total} конфет. Кидаем жребий, кто берёт первым')
    coin = random.randint(0, 1)
    if coin:
        await message.answer(text=f'{message.from_user.first_name}, поздравляю! Выпал орёл. Ты ходишь первым. Бери от 1 до 28 конфет')
    else:
        await message.answer(text=f'{message.from_user.first_name}, не расстраивайся, первый ход делает бот')
    await bot_turn(message)

dp.message_handler()
async def all_catch(message: Message):
    if message.text.isdigit():
        if 0 < int(message.text) < 29:
            await player_turn(message)
        else:
            await message.answer(text=f'{message.from_user.first_name}, Конфет надо взять от 1 до 28. Попробуй ещё раз')
    else:
            await message.answer(text='Введи цифрами количество конфет')

async def player_turn(message: Message):
    take_amount = int(message.text)
    total -= take_amount
    name = message.from_user.first_name
    await message.answer(text=f'{name} взял {take_amount} конфет и на столе осталось {total}')
    if await check_victory(message, name):
        return
    await message.answer(text=f'Теперь ходит бот')
    await bot_turn(message)

async def bot_turn(message: Message):
    take_amount = 0
    if total <= 28:
        take_amount = total
    else:
        take_amount = total%29 if total%29 ==0 else 1
    total -= take_amount
    name = message.from_user.first_name
    await message.answer(text=f'Бот взял {take_amount} конфет и на столе осталось {total}')
    if await check_victory(message, 'Бот'):
        return
    await message.answer(text=f'{name} теперь твой черед! Бери конфеты')
    
async def check_victory(message: Message, name: str):
    if total <=0:
        await message.answer(text=f'Победил {name}! Это была славная игра')
        return True
    return False