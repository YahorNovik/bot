from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter, Text, Command
from aiogram import Router
from bot.FSMstate.fsm import *

router: Router = Router()

@router.callback_query(Text(text=['payment_exit']), StateFilter(FSMFillForm.add_payment))
@router.callback_query(Text(text=['payment_exit']), StateFilter(FSMFillForm.gabinet_opened))
async def process_exit(callback_query: CallbackQuery, state: FSMContext):
   await callback_query.message.delete()
   await callback_query.message.answer("Чем еще могу помочь?")
   await state.set_state(FSMFillForm.default_state)

@router.message(Command(commands='restart'))
async def process_exit(message: Message, state: FSMContext):
   await message.delete()
   await message.answer("Чем еще могу помочь?")
   await state.set_state(FSMFillForm.default_state)