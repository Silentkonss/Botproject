from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_button = [
    [InlineKeyboardButton(text='Начать работу', callback_data='start_messages')]
]

sending_button = [
    [InlineKeyboardButton(text='Отправить сообщение', callback_data='send_messages')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel')]
]

start_markup = InlineKeyboardMarkup(inline_keyboard=start_button)
send_markup_1 = InlineKeyboardMarkup(inline_keyboard=sending_button)