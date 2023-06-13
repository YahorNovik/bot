from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter, Text, Command
from aiogram import Router
from FSMstate.fsm import *

router: Router = Router()

@router.message()
async def process_dummy_message(message: Message, state: FSMContext):
    await message.answer('не очень вас понимаю( Попробуйте следовать инструкциям в меню')