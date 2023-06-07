from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter, Command, Text
from aiogram.fsm.state import default_state

from db.db import maintain_db, File
from bot.keyboard.keyboard import *
from bot.validation.validation import validate_amount, validate_nip
from bot.parser.parser_code import *
from FSMstate.fsm import *

router: Router = Router()

# command
@router.message(Command(commands='add_payment'), StateFilter(default_state))
async def process_add_payment(message: Message, state: FSMContext):    
      with File(maintain_db, 'users.db') as db:
         try:
           nip = db.get_user_nip_by_id(message.from_user.id)
           if nip != None:
             gabinets = db.get_gabinets_by_user_nip(nip)
         except:
           await message.answer("Не удалось найти кабинеты, что-то пошло не так...")
           await state.clear()
           return
      if nip != None:
        await message.answer(text ='Выберите кабинет:', reply_markup=get_markup_gabinet(gabinets))
        await state.update_data(user_nip=nip)
        await state.set_state(FSMFillForm.gabinet_choosed)
      else:
        await message.answer('Сначала нужно зарегистрироваться.')

# choose gabinet
@router.callback_query(StateFilter(FSMFillForm.gabinet_choosed))
async def process_gabinet_choosed(callback_query: CallbackQuery, state: FSMContext):
      await callback_query.message.delete()    
      await state.update_data(gabinet_nip=callback_query.data)   
      await callback_query.message.answer('Введите сумму транзакции (злотые):')
      await state.set_state(FSMFillForm.add_payment)

# process amount
@router.message(StateFilter(FSMFillForm.add_payment))
@router.message(StateFilter(FSMFillForm.gabinet_opened))
async def process_amount(message: Message, state: FSMContext):
      if not validate_amount(message.text):
        await message.answer('Неправильный значение, введите сумму. Например: 5400')
        await message.answer('Введите сумму транзакции (злотые):')
      else:
        with File(maintain_db, 'users.db') as db:
          try:
              data = await state.get_data()
              user_nip = data['user_nip']
              gabinet_nip = data['gabinet_nip']
              date = datetime.date.today()
              payment_id=db.add_record_payments(user_nip, gabinet_nip, message.text, date)
              gabinet = db.get_gabinet_name(gabinet_nip)
          except:
              await message.answer("Не удалось добавить транзакцию, что-то пошло не так...")
              await state.clear()
              return
        await state.update_data(payment_id=payment_id)
        await message.answer(text = "Транзакция успешно добавлена:", reply_markup=get_markup_pyament_menu(gabinet=gabinet, amount=message.text))

# process add one more payment
@router.callback_query(Text(text=['add_one_more']), StateFilter(FSMFillForm.add_payment))
async def process_add_more_payment(callback: CallbackQuery, state: FSMContext):    
    with File(maintain_db, 'users.db') as db:
       try:
         nip = db.get_user_nip_by_id(callback.from_user.id)
         gabinets = db.get_gabinets_by_user_nip(nip)
       except:
         await callback.message.answer("Не удалось найти кабинеты, что-то пошло не так...")
         await state.clear()
         return

    await callback.message.delete()
    await callback.message.answer(text ='Выберите кабинет:', reply_markup=get_markup_gabinet(gabinets))
    await state.update_data(user_nip=nip)
    await state.set_state(FSMFillForm.gabinet_choosed)

# process add description
@router.callback_query(Text(text=['add_descr']), StateFilter(FSMFillForm.add_payment))
async def process_add_description(callback_query: CallbackQuery, state: FSMContext):
   await callback_query.message.delete()
   await callback_query.message.answer('Введите описание транзакции:')
   await state.set_state(FSMFillForm.add_description)

@router.message(StateFilter(FSMFillForm.add_description))
async def process_add_description(message: Message, state: FSMContext):
   
   if isinstance(message.text, str):
    with File(maintain_db, 'users.db') as db:
      try:
        data = await state.get_data()
        db.set_description(data['payment_id'], message.text)
      except:
        await message.answer("Не удалось добавить описание, что-то пошло не так...")
        await state.clear()
        return
   else:
      await message.answer("Неправильный формат, введите описание:")
    
   await state.set_state(FSMFillForm.add_payment) 
   await message.answer("Описание добавлено!", reply_markup= get_markup_pyament_menu(descr=False))

# process edit payment
@router.callback_query(Text(text=['payment_edit']), StateFilter(FSMFillForm.add_payment))
async def process_edit_payment(callback_query: CallbackQuery, state: FSMContext):
   await callback_query.message.delete()
   await callback_query.message.answer("Изменить:", reply_markup=get_edit_payment_keyboard())
   await state.set_state(FSMFillForm.edit_payment)

@router.callback_query( StateFilter(FSMFillForm.edit_payment))
async def process_edit_choice(callback_query: CallbackQuery, state: FSMContext):
   await callback_query.message.delete()

   if callback_query.data == "edit_gabinet":
    with File(maintain_db, 'users.db') as db:
       try:
         nip = db.get_user_nip_by_id(callback_query.from_user.id)
         gabinets = db.get_gabinets_by_user_nip(nip)
       except:
         await callback_query.message.answer("Не удалось найти кабинеты, что-то пошло не так...")
         await state.clear()
         return
    await callback_query.message.answer("Выберите кабинет:", reply_markup=get_markup_gabinet(gabinets))
    await state.set_state(FSMFillForm.edit_payment_data)
   elif callback_query.data == "edit_amount":
      await callback_query.message.answer("Введите сумму:")
      await state.set_state(FSMFillForm.edit_payment_data)
   elif callback_query.data == "delete_payment":
    with File(maintain_db, 'users.db') as db:
       try:
         payment_id = db.get_last_payment_id()
         db.delete_payment(int(payment_id))
         await state.clear()
         await callback_query.message.answer("Транзакция удалена. Чем еще могу помочь?")
       except:
         await callback_query.message.answer("Не удалось удалить транзакцию, что-то пошло не так...")
         await state.clear()
         return      

@router.callback_query(StateFilter(FSMFillForm.edit_payment_data))
async def process_edit_payment_gabinet(callback_query: CallbackQuery, state: FSMContext):
   if validate_nip(callback_query.data):
    with File(maintain_db, 'users.db') as db:
       print('gabinet...')
       try:
         payment_id = db.get_last_payment_id()
         db.edit_payment(payment_id=payment_id, gabinet_nip=callback_query.data)
         await state.clear()
         await callback_query.message.answer("Транзакция изменена. Чем еще могу помочь?")
       except:
         await callback_query.message.answer("Не удалось изменить кабинет, что-то пошло не так...")
         await state.clear()
         return
   else:
      await callback_query.message.answer("Что-то пошло не так...")
      await state.clear()
      return
   
@router.message(StateFilter(FSMFillForm.edit_payment_data))
async def process_edit_payment_amount(message: Message, state: FSMContext):
   if validate_amount(message.text):
    print('amount..')
    with File(maintain_db, 'users.db') as db:
       try:
         payment_id = db.get_last_payment_id()
         db.edit_payment(payment_id=payment_id, amount=message.text)
         await state.clear()
         await message.answer("Транзакция изменена. Чем еще могу помочь?")
       except:
         await message.answer("Не удалось изменить кабинет, что-то пошло не так...")
         await state.clear()
         return
   else:
      await message.answer("Что-то пошло не так...")
      await state.clear()
      return    