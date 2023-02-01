from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup

b1 = KeyboardButton('/цены')
b2 = KeyboardButton('/города')
b3 = KeyboardButton('/наличие')
b4 = KeyboardButton('контакт', request_contact=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)

kb_client.add(b3).row(b1, b2, b4)

inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="арендовать", callback_data="/арендовать"))
