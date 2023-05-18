from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import math

def get_yesno_keyboard(yes='yes', no='no'):       
        markup_answer = InlineKeyboardBuilder()
        bt_yes = InlineKeyboardButton(text="Да",
                                      callback_data=yes)
        bt_no = InlineKeyboardButton(text="Нет",
                                     callback_data=no)
        markup_answer.row(bt_yes, bt_no, width=2)
        return markup_answer.as_markup()

def get_markup_data(data):
        markup_data = InlineKeyboardBuilder()
        for key, value in data.items():
                bt_name = InlineKeyboardButton(text=key,
                                               callback_data='dummy')
                bt_data = InlineKeyboardButton(text=value,
                                               callback_data='dummy')
                markup_data.row(bt_name, bt_data, width=2)
        return markup_data.as_markup()

def get_markup_gabinet(gabinets):
     markup = InlineKeyboardBuilder()
     for gabinet in gabinets:
             bt_data = InlineKeyboardButton(text=gabinet[1],
                                            callback_data=gabinet[0])
             markup.row(bt_data, width=1)
     return markup.as_markup()

def get_payment_added_markup(gabinet:str, amount):
    markup = InlineKeyboardBuilder()
    
    bt_gabinet = InlineKeyboardButton(text=gabinet,
                                      callback_data="dummy")
    bt_amount = InlineKeyboardButton(text=amount,
                                     callback_data="dummy")
    markup.row(bt_gabinet, bt_amount)
    return markup.as_markup()

def get_markup_pyament_menu(gabinet:str=None, amount=None, descr=True):
    markup = InlineKeyboardBuilder()
    if gabinet != None and amount != None:
        bt_gabinet = InlineKeyboardButton(text=gabinet,
                                          callback_data="dummy")
        bt_amount = InlineKeyboardButton(text=f"{amount} zl",
                                         callback_data="dummy")
        markup.row(bt_gabinet, bt_amount, width=2)
      
    bt_pay = InlineKeyboardButton(text="Добавить еще транзакцию",
                                  callback_data="add_one_more")
    bt_exit = InlineKeyboardButton(text="Выйти",
                                   callback_data="payment_exit")
    bt_edit = InlineKeyboardButton(text="Изменить",
                                   callback_data="payment_edit")
    if descr == True:
      bt_descr = InlineKeyboardButton(text="Добавить описание",
                                      callback_data="add_descr")
      
      markup.row(bt_pay, bt_descr, width=2)
      markup.row(bt_edit, bt_exit, width=2)
    else:
      markup.row(bt_pay, bt_edit, width=2)
      markup.row(bt_exit, width=1)
    return markup.as_markup()

def get_edit_payment_keyboard():
    markup = InlineKeyboardBuilder()  
    bt_gabinet = InlineKeyboardButton(text="Изменить кабинет",
                                      callback_data="edit_gabinet")
    bt_amount = InlineKeyboardButton(text="Изменить сумму",
                                     callback_data="edit_amount")
    bt_delete = InlineKeyboardButton(text="Удалить транзакцию",
                                     callback_data="delete_payment")
    markup.row(bt_gabinet, bt_amount, bt_delete, width=1)
    return markup.as_markup()

def get_gabinet_keyboard():  
    markup = InlineKeyboardBuilder()    
    bt_pay = InlineKeyboardButton(text="Добавить транзакцию",
                                  callback_data="add_payment_gabinet")
    bt_trs = InlineKeyboardButton(text="Октрыть транзакции",
                                  callback_data="open_payments")
    bt_exit = InlineKeyboardButton(text="Выйти",
                                   callback_data="payment_exit")
    markup.row(bt_pay, bt_trs, bt_exit, width=1)
    return markup.as_markup()

def get_open_payments_keyboard():
    markup = InlineKeyboardBuilder()  
    bt_day = InlineKeyboardButton(text="Сегодня",
                                  callback_data="open_today")
    bt_week = InlineKeyboardButton(text="За неделю",
                                  callback_data="open_week")
    bt_month = InlineKeyboardButton(text="За месяц",
                                   callback_data="open_month")
    markup.row(bt_day, bt_week, bt_month, width=1)
    return markup.as_markup()

def get_payments_by_gabinet_markup(data, name:str, page_num:int=1, page_size:int=10):
    markup_data = InlineKeyboardBuilder()
    start_idx = (page_num - 1) * page_size 
    end_idx = start_idx + page_size 
    total_pages = math.ceil(len(data) / page_size)

    bt_name = InlineKeyboardButton(text=name, callback_data='dummy')

    markup_data.row(bt_name, width=1)

    bt_date = InlineKeyboardButton(text="Date", callback_data='dummy')
    bt_amount = InlineKeyboardButton(text="Amount", callback_data='dummy')

    markup_data.row(bt_date, bt_amount, width=2)

    for dt in data[start_idx:end_idx]:
        bt_date = InlineKeyboardButton(text=dt[5], callback_data='dummy')
        bt_amount = InlineKeyboardButton(text=dt[3], callback_data='dummy') 
        if dt[4] != "":
          bt_descr = InlineKeyboardButton(text=dt[4], callback_data='dummy')
          markup_data.row(bt_date, bt_amount, bt_descr, width=3)  
        else:
          markup_data.row(bt_date, bt_amount, width=2)            

    if total_pages > 1:
        total = len(data)
        if page_num - 1 > 0 and page_num + 1 <= total_pages:
          prev_page_button = InlineKeyboardButton(
            text="<<<",
            callback_data=page_num - 1 )  
          next_page_button = InlineKeyboardButton(
            text=">>>",
            callback_data=page_num + 1 )
          counter = InlineKeyboardButton(
            text=f"{end_idx}/{total}",
            callback_data="dummy" )
          markup_data.row(prev_page_button, counter, next_page_button, width=3)
        elif page_num - 1 == 0 and page_num != total_pages: 
          next_page_button = InlineKeyboardButton(
            text=">>>",
            callback_data=page_num + 1 )
          default_page_button = InlineKeyboardButton(
            text=" ",
            callback_data="dummy" )
          counter = InlineKeyboardButton(
            text=f"{end_idx}/{total}",
            callback_data="dummy" )
          markup_data.row(default_page_button, counter,next_page_button, width=3)
        elif page_num  == total_pages:
          prev_page_button = InlineKeyboardButton(
            text="<<<",
            callback_data=page_num - 1 )
          default_page_button = InlineKeyboardButton(
            text=" ",
            callback_data="dummy" )
          counter = InlineKeyboardButton(
            text=f"{total}/{total}",
            callback_data="dummy" )
          markup_data.row(prev_page_button, counter, default_page_button, width=3)
        
    exit_button = InlineKeyboardButton( text="Выйти",
                                        callback_data="payment_exit" )
    markup_data.row(exit_button, width=1)

    return markup_data.as_markup()
