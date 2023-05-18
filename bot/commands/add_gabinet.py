from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter, Text, Command
from aiogram.fsm.context import FSMContext
from bot.validation.validation import validate_nip, validate_account_number
from bot.FSMstate.fsm import *
from bot.parser.parser import get_user_data, get_gabinet_data
from bot.keyboard.keyboard import *
from bot.db.db import *
import time

router: Router = Router()

# command
@router.message(Command(commands='add_gabinet'))
@router.message(Command(commands='add_gabinet'), StateFilter(FSMFillForm.default_state))
async def process_logon_command(message: Message, state: FSMContext):
    with File(maintain_db, 'users.db') as db:
       try:
         nip = db.get_user_nip_by_id(message.from_user.id)
       except:
         await state.set_state(FSMFillForm.default_state)
         return   
    if nip is not None:
      await state.update_data(nip=nip)
      await message.answer('Введите NIP кабинета:')
      await state.set_state(FSMFillForm.gabinet_nip)
    else:
      await message.answer('Сначала нужно зарегистрироваться.')