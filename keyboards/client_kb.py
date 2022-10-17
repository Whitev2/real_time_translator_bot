from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


b_connect = KeyboardButton('Connect to user')
b_disconnect = KeyboardButton('Disconnect')
b_cancel = KeyboardButton('Cancel')


kb_client_connect = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_disconnect = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_get_id = ReplyKeyboardMarkup(resize_keyboard=True)


# add_buttons
kb_client_connect.add(b_connect)
kb_client_disconnect.add(b_disconnect)
kb_client_cancel.add(b_cancel)
