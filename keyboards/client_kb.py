from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/цены')
b2 = KeyboardButton('/города')
b3 = KeyboardButton('/Таня')
b4 = KeyboardButton('контакт', request_contact=True)
b5 = KeyboardButton('локация', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b3).row(b1,b2).row(b4,b5)
