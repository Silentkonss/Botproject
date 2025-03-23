from aiogram import F, Router, Bot, types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.enums.content_type import ContentType
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from pydantic import ValidationError
from dotenv import load_dotenv
from keyboards.keyboard import start_markup, send_markup_1
import os
from handlers.cont_type import get_type
import texts
import asyncio
from DB.db_func import db_new_chat, db_delete_chat, db_list_id, db_user_topic, db_user_id
from DB.main_db import conn


router = Router()

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))


class Boto_Func(StatesGroup):
    cancelling = State()
    sending_message = State()
    saving_inf = State()

@router.callback_query(F.data == 'cancel')
async def get_cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()


@router.message(Command('start'))
async def start_bot_handler(mess: Message):
    await mess.answer(texts.greeting_text, reply_markup=start_markup)


@router.callback_query(F.data == 'start_messages')
async def choisen_one(call: CallbackQuery, state: FSMContext):
    await state.clear()
    print('Time for choise')
    await call.message.answer(text='Вы готовы отправить сообщение? Если да - нажмите на кнопку "Отправить"', reply_markup=send_markup_1)

@router.callback_query(F.data == 'send_messages')
async def inputing_message(mess: Message, state: FSMContext):
    await state.update_data(mess.from_user.id)
    list_of_id = db_list_id()
    if mess.from_user.id not in list_of_id:
        try:
            topic = await room_bot.create_forum_topic(int(os.getenv('GROUP_ID')), f'{str(mess.from_user.id)}')
            db_new_chat(mess.from_user.id, 'anonym', topic.message_thread_id)
        except TelegramBadRequest:
            db_delete_chat(mess.chat.id)
            topic = await room_bot.create_forum_topic(int(os.getenv('GROUP_ID')), f'{str('anonym')}')
            db_new_chat(mess.from_user.id, "anonym", topic.message_thread_id)
            topic = db_user_topic(mess.from_user.id)
        await room_bot.send_message(int(os.getenv('GROUP_ID')), f'У Вас новое сообщение\n@{mess.from_user.id}',
                                    message_thread_id=topic.message_thread_id)
    else:
        pass


@router.message()
async def get_talk(mess: Message):
    if mess.chat.id != int(os.getenv('GROUP_ID')):
        topic = db_user_topic(mess.from_user.id)
        try:
            try:
                if mess.sticker is not None:
                    await bot.send_sticker(int(os.getenv('GROUP_ID')), mess.sticker.file_id, message_thread_id=int(topic))
                elif mess.photo is not None:
                    await bot.send_photo(int(os.getenv('GROUP_ID')), mess.photo[0].file_id, caption=mess.caption, message_thread_id=int(topic))
                else:
                    await bot.send_message(int(os.getenv('GROUP_ID')), mess.text, message_thread_id=int(topic))
            except ValidationError:
                await mess.answer('Можно отправлять Стикер, фото и картинки')
        except TelegramBadRequest:
            db_delete_chat(mess.chat.id)
            topic = await bot.create_forum_topic(int(os.getenv('GROUP_ID')), f'{str(mess.from_user.username)}')
            db_new_chat(mess.from_user.id, mess.from_user.username, topic.message_thread_id)
            topic = db_user_topic(mess.from_user.id)
            try:
                if mess.sticker is not None:
                    await bot.send_sticker(int(os.getenv('GROUP_ID')), mess.sticker.file_id, message_thread_id=int(topic))
                elif mess.photo is not None:
                    await bot.send_photo(int(os.getenv('GROUP_ID')), mess.photo[0].file_id, caption=mess.caption, message_thread_id=int(topic))
                else:
                    await bot.send_message(int(os.getenv('GROUP_ID')), mess.text, message_thread_id=int(topic))
            except ValidationError:
                await mess.answer('Можно отправлять Стикер, фото и картинки')

    elif mess.chat.id == int(os.getenv('GROUP_ID')) and mess.from_user.is_bot is False:
        topic = mess.message_thread_id
        user_id = db_user_id(topic)
        try:
            if mess.sticker is not None:
                await bot.send_sticker(int(user_id), mess.sticker.file_id)
            elif mess.photo is not None:
                await bot.send_photo(int(user_id), mess.photo[0].file_id, caption=mess.caption)
            else:
                await bot.send_message(int(user_id), mess.text)
        except TelegramForbiddenError:
            await bot.send_message(int(os.getenv('GROUP_ID')), 'Пользователь заблокировал бота, можно удалить этот чат', message_thread_id=int(topic))
    else:
        pass