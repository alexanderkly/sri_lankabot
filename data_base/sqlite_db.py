import sqlite3 as sq

from aiogram.types import InputMediaPhoto

from create_bot import dp, bot


def sql_start():
    global base, cur
    base = sq.connect('rent1_sri.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute(
        'CREATE TABLE IF NOT EXISTS house_for_rent(main_photo TEXT, bedroom_photo TEXT, kitchen_photo TEXT,\
         garden_photo TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO house_for_rent VALUES(?, ?, ?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM house_for_rent').fetchall():
        media_list = []
        for file_id in ret[0:4]:
            media_list.append(InputMediaPhoto(media=file_id))
        await bot.send_media_group(message.from_user.id, media=media_list)
        await bot.send_message(message.from_user.id, f'{ret[4]}\nОписание: {ret[-2]}\nЦена {ret[-1]}')
    # for ret in cur.execute('SELECT * FROM house_for_rent').fetchall():
    #     media_list = [InputMediaPhoto(file_id=file_id) for file_id in ret[0:3]]
    #     await bot.send_media_group(message.from_user.id, media=media_list)
    # await bot.send_photo(message.from_user.id, ret[3], f'{ret[4]}\nОписание: {ret[-2]}\nЦена {ret[-1]}')


async def sql_read2():
    return cur.execute('SELECT * FROM house_for_rent').fetchall()


async def sql_delete_command(data):
    cur.execute('DELETE FROM house_for_rent WHERE name == ?', (data,))
    base.commit()
