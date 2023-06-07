from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter, Text, Command
from aiogram.fsm.context import FSMContext
from validation.validation import validate_nip, validate_account_number, validate_address
from aiogram.fsm.state import default_state
from FSMstate.fsm import *
from parser_folder.parser_code import get_user_data, get_gabinet_data
from keyboard.keyboard import *
from db.db import *
import time

router: Router = Router()

# command
@router.message(Command(commands='logon'))
async def process_logon_command(message: Message, state: FSMContext):    
    with File(maintain_db, 'users.db') as db:
       try:
         nip = db.get_user_nip_by_id(message.from_user.id)
       except:
         await state.clear()
         await message.answer('Что-то пошло не так...')
         return   
    if nip is None:
      await message.answer('Введите NIP:')
      await state.set_state(FSMFillForm.user_nip)
    else:
      await message.answer('Вы уже зарегистрированны!')

# confirm data user
@router.callback_query(Text(text=['yes']), StateFilter(FSMFillForm.user_nip))
async def process_yes_button(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    with File(maintain_db) as db: 
      try:
        db.add_record_users(user_id=data['user_id'] ,nip=data['nip'], regon=data['regon'], address=data['address'], city=data['city'], name=data['name'], date=data['date'])
      except:
        await callback_query.message.answer("Не удалось зарегистрировать юзера, что-то пошло не так...")
        return
        
    await callback_query.message.delete()
    await callback_query.message.answer("Ваш юзер был успешно добавлен!")
    await callback_query.message.answer("Введите номер банковского счета (нужен для создания фактур):")
    await state.set_state(FSMFillForm.account_number)

@router.callback_query(Text(text=['no']), StateFilter(FSMFillForm.user_nip))
async def process_no_button(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(text = 'Данные выше получены из официальной базы данных B2B. Если данные неправильны, попробуйте поменять их в базе и зарегистрироваться позже.')

# confirm data gabinet
@router.callback_query(Text(text=['yes']), StateFilter(FSMFillForm.gabinet_added))
async def process_yes_button_gabinet(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    with File(maintain_db) as db:
     try:
       db.add_record_gabinets(nip=data['gabinet_nip'], user_nip=data['nip'], name=data['name'], address=data['address'])
     except:
       await callback_query.message.answer("Не удалось добавить кабинет, что-то пошло не так...")
       return
    await callback_query.message.delete() 
    await callback_query.message.answer(text = 'Добавить еще один кабинет?', reply_markup= get_yesno_keyboard(yes="yes_add", no="no_add"))
    await state.set_state(FSMFillForm.user_nip)

@router.callback_query(Text(text=['no']), StateFilter(FSMFillForm.gabinet_added))
async def process_no_button_gabinet(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(text = 'Данные выше получены из официальной базы данных. Если данные неправильны, проверьте NIP кабинета.')
    await state.clear()

@router.callback_query(Text(text=['no_add']), StateFilter(FSMFillForm.user_nip))
async def process_no_add(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer('Кабинет был успешно добавлен')
    await state.clear()

@router.callback_query(Text(text=['yes_add']), StateFilter(FSMFillForm.user_nip))
async def process_no_add(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer('Введите NIP кабинета:')
    await state.set_state(FSMFillForm.gabinet_nip)

# process NIPs
@router.message(StateFilter(FSMFillForm.user_nip))
async def process_nip(message: Message, state: FSMContext):
    if not validate_nip(message.text):
        await message.answer('Неправильный номер NIP.')
        await message.answer('Введите NIP:')
    else :
        #try:
          user_data = get_user_data(message.text)
          await state.update_data(nip=message.text)
          await state.update_data(name=user_data['Name'])
          await state.update_data(address=user_data['Address'])
          await state.update_data(city=user_data['City'])
          await state.update_data(regon=user_data['REGON'])
          await state.update_data(date=user_data['Date'])
          await state.update_data(user_id=message.from_user.id)

          await message.answer(text = 'Ваши данные:', reply_markup= get_markup_data(user_data))

          time.sleep(2)
          await message.answer(text = 'Данные корректны?', reply_markup= get_yesno_keyboard())
        #except Exception as err:
        #  await message.answer(text = 'Не могу найти данные по номеру NIP')
    
@router.message(StateFilter(FSMFillForm.gabinet_nip))
async def process_gabinet_nip(message: Message, state: FSMContext):
    await state.update_data(gabinet_nip=message.text)
    if not validate_nip(message.text):
        await message.answer('Неправильный номер NIP.')
        await message.answer('Введите NIP:')
    else :
        try:
          data = get_gabinet_data(message.text)
          await message.answer(text = 'Данные компании:', reply_markup= get_markup_data(data))

          await state.update_data(name=data['Name'])
          await state.update_data(address=data['Address'])
          await state.update_data(regon=data['REGON'])

          await message.answer(text = 'Данные корректны?', reply_markup= get_yesno_keyboard())
          await state.set_state(FSMFillForm.gabinet_added)
        except Exception as err:
          await message.answer(text = 'Не могу найти данные по номеру NIP. Хотите добавить кабинет в ручную?', reply_markup= get_yesno_keyboard())
          await state.set_state(FSMFillForm.add_gabinet_manually)

# add gabinet manually
@router.callback_query(Text(text=['yes']), StateFilter(FSMFillForm.add_gabinet_manually))
async def process_yes_button_gabinet_manually(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete() 
    await callback_query.message.answer(text = 'Введите название кабинета (в формате: Ul. Jerzego Bajana 31D, 54-129 Wrocław):')

@router.callback_query(Text(text=['no']), StateFilter(FSMFillForm.add_gabinet_manually))
async def process_no_button_gabinet_manually(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await callback_query.message.answer(text = 'Чем еще могу помочь?')
    await state.clear()

@router.message(StateFilter(FSMFillForm.add_gabinet_manually))
async def process_address(message: Message, state: FSMContext):
   if validate_address(message.text):
      await state.update_data(address=message.text)
      await message.answer('Введите название кабинета:')
      await state.set_state(FSMFillForm.add_manually_name)
   else:
      await message.answer('Неправильный формат. Введите название кабинета (в формате: Ul. Jerzego Bajana 31D, 54-129 Wrocław):')

@router.message(StateFilter(FSMFillForm.add_manually_name))
async def process_name(message: Message, state: FSMContext):
    data = await state.get_data()
    with File(maintain_db) as db:
     try:
       db.add_record_gabinets(nip=data['gabinet_nip'], user_nip=data['nip'], name=message.text, address=data['address'])
     except:
       await message.answer("Не удалось добавить кабинет, что-то пошло не так...")
       return
    await message.delete() 
    await message.answer(text = 'Добавить еще один кабинет?', reply_markup= get_yesno_keyboard(yes="yes", no="no_add"))
    await state.set_state(FSMFillForm.user_nip)

@router.message(StateFilter(FSMFillForm.account_number))
async def process_account_number(message: Message, state: FSMContext):
    result = validate_account_number(message.text)
    if not result[0]:
        await message.answer('Неправильный номер счета.')
        await message.answer("Введите номер банковского счета (нужен для создания фактур):")
    else :
        data = await state.get_data()
        with File(maintain_db) as db:
           try:
              db.add_account_number(user_nip=data['nip'], account_number=message.text)
           except:
              await message.answer("Не удалось добавить номер счета, что-то пошло не так...")
              return
        await message.answer(f"Ваш номер счета в банке {result[1]} успешно добавлен!")
        await message.answer("Введите NIP кабинета:")
        await state.set_state(FSMFillForm.gabinet_nip)
