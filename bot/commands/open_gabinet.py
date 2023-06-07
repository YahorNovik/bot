from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter, Command, Text
from aiogram.fsm.state import default_state

from db.db import maintain_db, File
from keyboard.keyboard import *
from FSMstate.fsm import *

import datetime

router: Router = Router()

# command open gabinet
@router.message(Command(commands='open_gabinet'), StateFilter(default_state))
@router.message(Command(commands='open_gabinet'))
async def process_open_gabinet_command(message: Message, state: FSMContext):   
    with File(maintain_db, 'users.db') as db:
       try:
         nip = db.get_user_nip_by_id(message.from_user.id)
         gabinets = db.get_gabinets_by_user_nip(nip)
       except:
         await message.answer("Не удалось найти кабинеты, что-то пошло не так...")
         await state.clear()
         return
    if nip is not None:
      await message.answer(text ='Выберите кабинет:', reply_markup=get_markup_gabinet(gabinets))
      await state.update_data(user_nip=nip)
      await state.set_state(FSMFillForm.gabinet_opened)
    else: 
     await message.answer('Сначала нужно зарегистрироваться.')

# command add gabinet
@router.message(Command(commands='add_gabinet'), StateFilter(default_state))
async def process_add_gabinet_command(message: Message, state: FSMContext):    
    await message.answer('Введите NIP кабинета:')
    await state.set_state(FSMFillForm.gabinet_nip)

# add payment
@router.callback_query(Text(text=['add_payment_gabinet']), StateFilter(FSMFillForm.gabinet_opened))
@router.callback_query(Text(text=['add_payment_gabinet']), StateFilter(FSMFillForm.add_payment))
async def process_add_payment_gabinet(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer("Введите сумму транзакции (злотые):")

@router.callback_query(Text(text=['add_one_more']), StateFilter(FSMFillForm.gabinet_opened))
async def process_add_more_payment_gabinet(callback: CallbackQuery, state: FSMContext):     
   await callback.message.answer(text ='Введите сумму транзакции (злотые):')

# open payments
@router.callback_query(Text(text=['open_payments']), StateFilter(FSMFillForm.gabinet_opened))
async def process_open_payments(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(text="Выберите пeриод:", reply_markup=get_open_payments_keyboard())

@router.callback_query(Text(text=["open_today", "open_week", "open_month"]), StateFilter(FSMFillForm.gabinet_opened))
async def process_open_payments_period(callback_query: CallbackQuery, state: FSMContext):
       
       await callback_query.message.delete()
       
       if callback_query.data == "open_today":
          start_date = datetime.datetime.now().strftime('%Y-%m-%d')
          end_date = datetime.datetime.now().strftime('%Y-%m-%d')
          text = 'день'
       elif  callback_query.data == "open_week":
          today = datetime.datetime.now()
          start_date = (today - datetime.timedelta(days=today.weekday())).date()
          end_date = start_date + datetime.timedelta(days=6)
          text = 'неделю'
       elif callback_query.data == "open_month":
          today = datetime.date.today()
          start_date = datetime.date(today.year, today.month, 1)
          end_date = start_date.replace(day=28) + datetime.timedelta(days=4)
          end_date = end_date - datetime.timedelta(days=end_date.day)
          text = 'месяц'

       data = await state.get_data()
       gabinet_nip = data['gabinet_nip']
       with File(maintain_db, 'users.db') as db:
         try:
           payments = db.get_payments_by_gabinet_and_date(int(gabinet_nip), str(start_date), str(end_date))
           name = db.get_gabinet_name(gabinet_nip)
         except:
           await callback_query.message.answer("Не удалось найти транзакции, что-то пошло не так...")
           await state.clear()
           return
       
       await state.update_data(payments=payments)
       await state.update_data(gabinet_name=name)
       await callback_query.message.answer(text=f"Ваши транзакции за {text}:", reply_markup=get_payments_by_gabinet_markup(payments, name))
       await state.set_state(FSMFillForm.payments_view)

@router.callback_query(Text(text=['add_invoice_gabinet']), StateFilter(FSMFillForm.gabinet_opened))
async def process_gabinet_opened(callback_query: CallbackQuery, state: FSMContext):
      await callback_query.message.delete()    
      data = await state.get_data()
      gabinet_nip = data['gabinet_nip']
      today = datetime.date.today()
      start_date = datetime.date(today.year, today.month, 1)
      end_date = start_date.replace(day=28) + datetime.timedelta(days=4)
      end_date = end_date - datetime.timedelta(days=end_date.day)

      with File(maintain_db, 'users.db') as db:
        payments = db.get_payments_by_gabinet_and_date(int(gabinet_nip), str(start_date), str(end_date))

      total = 0
      for item in payments:
        total += item[3]
      await state.update_data(amount=total)
      await callback_query.message.answer(f'Сумма транзакций за месяц: {total} zl. Сумма корректна?', reply_markup=get_yesno_keyboard())
      await state.set_state(FSMFillForm.invoice_amount)

@router.callback_query(StateFilter(FSMFillForm.gabinet_opened))
async def process_gabinet_opened(callback_query: CallbackQuery, state: FSMContext):
   await callback_query.message.delete()
   await state.update_data(gabinet_nip=callback_query.data)
   await callback_query.message.answer(text="Чем могу помочь?", reply_markup=get_gabinet_keyboard())

@router.callback_query(Text(text=['payment_exit']), StateFilter(FSMFillForm.payments_view))
async def process_exit(callback_query: CallbackQuery, state: FSMContext):
   await callback_query.message.delete()
   await callback_query.message.answer("Чем еще могу помочь?")
   await state.clear()

@router.callback_query(Text(text=['dummy']), StateFilter(FSMFillForm.payments_view))
async def process_dummy(callback_query: CallbackQuery, state: FSMContext):
   return

@router.callback_query(StateFilter(FSMFillForm.payments_view))
async def process_pagination(callback_query: CallbackQuery, state: FSMContext):
   data = await state.get_data()
   markup = get_payments_by_gabinet_markup(data=data['payments'], name=data['gabinet_name'], page_num=int(callback_query.data))
   await callback_query.message.edit_reply_markup(reply_markup=markup)