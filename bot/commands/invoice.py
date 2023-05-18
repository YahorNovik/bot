from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter, Command, Text
from aiogram import Bot

from bot.db.db import maintain_db, File
from bot.keyboard.keyboard import *
from bot.validation.validation import validate_amount
from bot.parser.parser import *
from bot.FSMstate.fsm import *
from bot.faktura.faktura import *
from decimal import Decimal

from aiogram.types import Message, InputMediaDocument
from aiogram.enums import InputMediaType

from aiogram.types import FSInputFile

router: Router = Router()

# command
@router.message(Command(commands='invoice'))
@router.message(Command(commands='invoice'), StateFilter(FSMFillForm.default_state))
async def process_add_invoice(message: Message, state: FSMContext):    
      with File(maintain_db, 'users.db') as db:
         try:
           nip = db.get_user_nip_by_id(message.from_user.id)
           gabinets = db.get_gabinets_by_user_nip(nip)
         except:
           await message.answer("Не удалось найти кабинеты, что-то пошло не так...")
           await state.set_state(FSMFillForm.default_state)
           return
      if nip != None:
        await message.answer(text ='Выберите кабинет:', reply_markup=get_markup_gabinet(gabinets))
        await state.update_data(user_nip=nip)
        await state.set_state(FSMFillForm.invoice_gabinet)
      else:
        await message.answer("Сначала нужно зарегистрироваться.") 

# choose gabinet
@router.callback_query(StateFilter(FSMFillForm.invoice_gabinet))
async def process_gabinet_choosed(callback_query: CallbackQuery, state: FSMContext):
      await callback_query.message.delete()    
      await state.update_data(gabinet_nip=callback_query.data)
      today = datetime.date.today()
      start_date = datetime.date(today.year, today.month, 1)
      end_date = start_date.replace(day=28) + datetime.timedelta(days=4)
      end_date = end_date - datetime.timedelta(days=end_date.day)

      with File(maintain_db, 'users.db') as db:
        payments = db.get_payments_by_gabinet_and_date(int(callback_query.data), str(start_date), str(end_date))

      total = 0
      for item in payments:
        total += item[3]
      await state.update_data(amount=total)
      await callback_query.message.answer(f'Сумма транзакций за месяц: {total} zl. Сумма корректна?', reply_markup=get_yesno_keyboard())
      await state.set_state(FSMFillForm.invoice_amount)

@router.callback_query(Text(text=['yes']), StateFilter(FSMFillForm.invoice_amount))
async def process_yes(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()    
    data = await state.get_data()
    faktura = Faktura(user_nip=data['user_nip'], gabinet_nip=data['gabinet_nip'], amount=int(data['amount']))
    data=faktura.get_data()
    number=faktura.get_faktura(data)

    #pdf = FSInputFile("bot/faktura/faktury/Faktura.pdf")
          
    #media = InputMediaDocument(type=InputMediaType.DOCUMENT, media=pdf)
    await callback_query.message.answer(f'Фактура номер {number} успешно создана!')
    #await callback_query.message.answer_media_group([media])

@router.callback_query(Text(text=['no']), StateFilter(FSMFillForm.invoice_amount))
async def process_no(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()    
    await state.set_state(FSMFillForm.set_amount)
    await callback_query.message.answer(f'Введите сумму brutto (zl):')

# process amount
@router.message(StateFilter(FSMFillForm.set_amount))
async def process_amount(message: Message, state: FSMContext, bot: Bot):
      if not validate_amount(message.text):
        await message.answer('Неправильный значение, введите сумму. Например: 5400')
        await message.answer('Введите сумму транзакции (злотые):')
      else:
          data = await state.get_data()
          faktura = Faktura(user_nip=data['user_nip'], gabinet_nip=data['gabinet_nip'], amount=Decimal(message.text))
          data=faktura.get_data()
          number = faktura.get_faktura(data)

          #pdf = FSInputFile("bot/faktura/faktury/Faktura.pdf")
          
          #media = InputMediaDocument(type=InputMediaType.DOCUMENT, media=pdf)
          await message.answer(f'Фактура номер {number} успешно создана!')
          #await message.answer_media_group([media])


