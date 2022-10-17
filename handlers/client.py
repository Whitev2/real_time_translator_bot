import data_base.sqlite_db
from aiogram import types, Dispatcher
from start_config import dp
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import client_kb


class FSMAdmin(StatesGroup):
    from_user = State()
    to_user = State()
    language = State()


# Приветствие
async def commans_start(message: types.Message):
    await message.answer(f"Your username:  <code>{message.from_user.username}</code>\n\n"
                         f"Send it to the interlocutor so that he can contact you",
                         reply_markup=client_kb.kb_client_connect)
    user_data = [message.from_user.username, message.from_user.id]
    await sqlite_db.sql_add_own_user(user_data)


# Начало диалога загрузки

async def cm_start(message: types.Message):
    await FSMAdmin.to_user.set()
    await message.reply('Upload name', reply_markup=client_kb.kb_client_cancel)


# Ловим имя
async def name(message: types.Message, state: FSMContext):
    get_name_in_own_base = await data_base.sqlite_db.sql_read_own_user(message.text)
    username = message.from_user.username
    if get_name_in_own_base.fetchone() is None:
        await message.reply('This person is not logged in to the bot', reply_markup=client_kb.kb_client_connect)
        await state.finish()
    else:
        get_id_in_own_base = await data_base.sqlite_db.sql_read_own_user(message.text)
        user_id = get_id_in_own_base.fetchall()
        id = int(user_id[0][1])
        await dp.bot.send_message(chat_id=id, text=f'User: <code>{username}</code> сonnects to you')
        async with state.proxy() as data:
            data['from_user'] = message.from_user.username
        async with state.proxy() as data:
            data['to_user'] = message.text
        await FSMAdmin.next()

        await message.reply('What language does your interlocutor speak?\nInput example: "En" or "en"', reply_markup=client_kb.kb_client_cancel)


# Отмена фсм
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК', reply_markup=client_kb.kb_client_connect)


# Ловим language
async def set_language(message: types.Message, state: FSMContext):
    if len(message.text) <= 4:
        async with state.proxy() as data:
            data['language'] = message.text.lower()
        await sqlite_db.sql_add_to_user(state)
        await message.reply('Successful connection', reply_markup=client_kb.kb_client_disconnect)

        await state.finish()


# Удаление связи
async def sql_delete(message: types.Message):
    username = message.from_user.username
    # Предупреждение 2 юзера о разрыве связи
    user2 = await sqlite_db.sql_read_to_user(username)
    username2 = user2.fetchall()[0][1]
    id_user_2 = await sqlite_db.sql_read_own_user(username2)
    # id_user = id_user_2.fetchall()[0][1]
    id = int(id_user_2.fetchall()[0][1])
    await dp.bot.send_message(chat_id=id, text=f'Partner: {username} disconnected from you',
                              reply_markup=client_kb.kb_client_connect)

    # Юзер нажимает дисконект
    await data_base.sqlite_db.sql_delete_command(username)
    await message.reply('Successful disconnection', reply_markup=client_kb.kb_client_connect)


def regiser_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commans_start, commands=['start', 'help'])
    dp.register_message_handler(cm_start, Text(equals='Connect to user', ignore_case=True))
    dp.register_message_handler(cancel_handler, Text(equals='Cancel', ignore_case=True), state="*")
    dp.register_message_handler(name, state=FSMAdmin.to_user)
    dp.register_message_handler(set_language, state=FSMAdmin.language)
    dp.register_message_handler(sql_delete, Text(equals='Disconnect', ignore_case=True), state="*")
