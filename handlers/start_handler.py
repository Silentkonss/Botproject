from aiogram import F, Router, Bot, types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.enums.content_type import ContentType
from dotenv import load_dotenv
from keyboards.keyboard import start_markup
import os
from handlers.cont_type import get_type
import texts


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
    