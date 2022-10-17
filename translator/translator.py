import data_base.sqlite_db
from aiogram import types, Dispatcher
from start_config import dp, bot
from keyboards import client_kb
from googletrans import Translator

translator = Translator()


# отправка переведенного текста
async def translate_text(ID, lg, text=None):
    translate = translator.translate(text, dest=lg)
    await dp.bot.send_message(chat_id=ID, text=translate.text)


# получение текста
@dp.message_handler()
async def translate_message(message: types.Message):
    username = message.from_user.username
    get_from_user = await data_base.sqlite_db.sql_read_to_user(username)

    if get_from_user.fetchone() is None:
        # Дклаем когда человека нет в own базе
        id = await data_base.sqlite_db.sql_read_own_user(username)
        id2 = id.fetchall()[0][1]
        await bot.send_message(chat_id=id2, text='You are not affiliated with anyone yet.',
                               reply_markup=client_kb.kb_client_connect)

    else:
        try:
            # Делем когда есть человек в own базе
            get_to_user = await data_base.sqlite_db.sql_read_to_user(username)
            to_user = get_to_user.fetchall()
            lg = to_user[0][2]
            get_id = await  data_base.sqlite_db.sql_read_own_user(to_user[0][1])
            id = get_id.fetchall()
            id2 = int(id[0][1])
            await translate_text(id2, lg, message.text)
        except:
            pass


def regiser_translate_client(dp: Dispatcher):
    dp.register_message_handler(translate_message)
