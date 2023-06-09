from aiogram.filters.state import State, StatesGroup

class FSMFillForm(StatesGroup):
    user_nip = State()
    account_number = State()        
    gabinet_nip = State()
    gabinet_added = State()  
    add_payment = State() 
    gabinet_choosed = State() 
    add_description = State() 
    gabinet_opened = State()   
    payments_view = State() 
    edit_payment = State()
    edit_payment_data = State()
    invoice_gabinet = State()
    invoice_amount = State()
    set_amount = State()
    add_gabinet_manually = State()
    add_manually_name = State()