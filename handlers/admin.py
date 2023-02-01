from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import dp, bot
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None


class FSMAdmin(StatesGroup):
    main_photo = State()
    bedroom_photo = State()
    kitchen_photo = State()
    garden_photo = State()
    name = State()
    description = State()
    price = State()


# Получаем ID Администратора
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_change_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, "Вы являетесь администратором",
                           reply_markup=admin_kb.button_case_admin)
    await message.delete()


# начало диалога загрузки нового пункта меню
# @dp.message_handler(commands=['Загрузить'], state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.main_photo.set()
        await message.reply('Загрузите основное фото')


# выход из состояний
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('ОК')


# ловим ответ пользователя
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_main_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['main_photo'] = message.photo[0].file_id
        await FSMAdmin.bedroom_photo.set()
        await message.reply('Теперь фото спальни')


async def load_bedroom_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['bedroom_photo'] = message.photo[1].file_id
        await FSMAdmin.kitchen_photo.set()
        await message.reply('Теперь фото кухни')


async def load_kitchen_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['kitchen_photo'] = message.photo[2].file_id
        await FSMAdmin.garden_photo.set()
        await message.reply('Теперь фото сада')


async def load_garden_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['garden_photo'] = message.photo[3].file_id
        await FSMAdmin.next()
        await message.reply('Теперь необходимо ввести название')


# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь введите описание')


# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь введите цену')


# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)
        # передача данных в БД
        await sqlite_db.sql_add_command(state)
        # сохранить до этого момента
        await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(call: types.CallbackQuery):
    await sqlite_db.sql_delete_command(call.data.replace('del', ''))
    await call.answer(text=f'{call.data.replace("del", "")} удалена', show_alert=True)


@dp.message_handler(commands='удалить')
async def delete_item(message: types.Message):
    # if message.from_user.id == ID:
    read = await sqlite_db.sql_read2()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[4]}\nОписание: {ret[5]}\nЦена {ret[-1]}')
        await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(f'Удалить {ret[4]}', callback_data=f'del {ret[4]}')))


# Регистрируем хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_change_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_main_photo, content_types=['photo'], state=FSMAdmin.main_photo)
    dp.register_message_handler(load_bedroom_photo, content_types=['photo'], state=FSMAdmin.bedroom_photo)
    dp.register_message_handler(load_kitchen_photo, content_types=['photo'], state=FSMAdmin.kitchen_photo)
    dp.register_message_handler(load_garden_photo, content_types=['photo'], state=FSMAdmin.garden_photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    #dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    #dp.register_message_handler(delete_item, commands=['удалить'])
