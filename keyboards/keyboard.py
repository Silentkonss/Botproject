from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start_button = [
    [InlineKeyboardButton(text='Начать работу', callback_data='sending_messages')]
]


start_markup = InlineKeyboardMarkup(inline_keyboard=start_button)