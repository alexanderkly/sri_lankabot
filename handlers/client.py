from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from keyboards.client_kb import inkb

min_price = 400
max_price = 1400
starting_phrase = ["Здравствуйте", "Привет", "здравствуйте", "привет", "добрый", "доброго", "прив", ]


# # @dp.message_handler(commands=['start', 'help'])
# async def command_start(message: types.Message):
#     try:
#         await bot.send_message(message.from_user.id, 'На Шри всегда отличная погода ;)', reply_markup=kb_client)
#         await message.delete()
#     except:
#         await message.answer(
#             'Не получилось отправить Вам личное сообщение, пожалуйста напишите https://t.me/sri_lankabot')

# @dp.message_handler((lambda mesage: "Здравствуйте" in mesage.text))
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Здравствуйте ;)', reply_markup=kb_client)
    except:
        await message.answer(
            'Не получилось отправить Вам личное сообщение, пожалуйста напишите https://t.me/sri_lankabot')


# @dp.message_handler(commands=['города'])
async def command_town(message: types.message):
    try:
        await bot.send_message(message.from_user.id, 'Мы представлены в таких городах как: Мирисса, Матара и Велигама')#, reply_markup=ReplyKeyboardRemove())
    except:
        await message.answer(
            'Не получилось отправить Вам личное сообщение, пожалуйста напишите https://t.me/sri_lankabot')


# @dp.message_handler(commands=['цены'])
async def command_price(message: types.message, ):
    try:
        await bot.send_message(message.from_user.id,
                               f'Цены на аренду жилья в данный момент варьируются от  {min_price}$ до {max_price}$')
        await message.delete()
    except:
        await message.answer(
            'Не получилось отправить Вам личное сообщение, пожалуйста напишите https://t.me/sri_lankabot')


# @dp.callback_query_handlers(text='арендовать')
async def house_want_rent(callbeck: types.callback_query):
    # await callbeck.message.answer("")
    await callbeck.answer()
    await bot.send_message(chat_id=1581750481, text='хотят бронь')


# chat_id=1581750481, text=

# @dp.message_handler(commands=['наличие'])
async def house_for_rent_command(message: types.Message):
    await sqlite_db.sql_read(message)
    await bot.send_message(message.from_user.id, 'для связи с https://t.me/AlexanderStrogy нажмите ', reply_markup=inkb)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start,
                                (lambda message: any(starting in message.text for starting in starting_phrase)))
    dp.register_message_handler(command_town, commands=['города', 'город', 'место', 'где находитесь', 'локации'])
    dp.register_message_handler(command_price, commands=['цены', 'цена', 'стоимость', 'price', 'сколько стоит'])
    dp.register_callback_query_handler(house_want_rent, text='/арендовать')
    dp.register_message_handler(house_for_rent_command, commands=['наличие'])
