from aiogram import types, Dispatcher
from create_bot import bot, dp
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db


min_price = 300
max_price = 1400


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'На Шри всегда отличная погода ;)', reply_markup=kb_client)
        await message.delete()
    except:
        await message.answer(
            'Не получилось отправить Вам личное сообщение, пожалуйста напишите https://t.me/sri_lankabot')


# @dp.message_handler(commands=['города'])
async def command_town(message: types.message):
    try:
        await bot.send_message(message.from_user.id, 'Мы представлены в таких городах как: Мирисса, Матара и Вилигама', \
                               reply_markup=ReplyKeyboardRemove())
        await message.delete()
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


async def command_Tanya(message: types.message):
    try:
        # await bot.send_message(message.from_user.id, 'ПИИИИИИСЬКА!!!!!')
        await message.answer('ПИИИИИИСЬКА!!!!!')
    except:
        await message.answer(
            'Не получилось отправить Вам личное сообщение, пожалуйста напишите https://t.me/sri_lankabot')

# @dp.message_handler(commands=['наличие'])
async def house_for_rent_command(message : types.Message):
    await sqlite_db.sql_read(message)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_town, commands=['города', 'город', 'место', 'где находитесь', 'локации'])
    dp.register_message_handler(command_price, commands=['цены', 'цена', 'стоимость', 'price', 'сколько стоит'])
    dp.register_message_handler(command_Tanya, commands=['Таня'])
    dp.register_message_handler(house_for_rent_command, commands=['наличие'])