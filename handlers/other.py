from aiogram import types, Dispatcher
import string, json


# @dp.message_handler()
async def cenz_chek(message: types.message):
    # проверка на маты
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('маты запрещены')
        await message.delete()
    if 'Таня' in message.text or 'таня' in message.text:
        await message.reply('Писька')

    # await  message.answer(message.text)
    # await  message.reply(message.text)
    # await  bot.send_message(message.from_user.id, message.text)


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(cenz_chek)
