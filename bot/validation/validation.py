import re
from db.db import maintain_db, File
from validation.banks import *

def validate_nip(nip: str) -> bool:
    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    nip = nip.replace('-', '').replace(' ', '')
    if not nip.isnumeric() or len(nip) != 10:
        return False
    check_sum = sum(int(nip[i]) * weights[i] for i in range(9)) % 11
    if check_sum == 10:
        check_sum = 0
    return check_sum == int(nip[9])

def validate_amount(payment_amount: str) -> bool:
    if not payment_amount or not isinstance(payment_amount, str):
        return False
    pattern = r'^\d+(\.\d{1,2})?$'
    if not re.match(pattern, payment_amount):
        return False
    return True

def validate_account_number(account_number):
    number = account_number.replace(' ', '')
    account_number = account_number.replace(' ', '')
    if len(account_number) != 26:
        return False
    if not account_number[:2].isdigit():
        return False
    account_number = f"PL{account_number}"
    account_number = account_number[4:] + account_number[:4]
    account_number = ''.join(str(ord(char) - 55) if char.isalpha() else char for char in account_number)
    remainder = int(account_number) % 97
    if remainder != 1:
        return False
    return True, get_bank_name_by_number(number)

def get_bank_name_by_number(account_number):
    account_number = str(account_number).replace(' ', '')
    bank_code = account_number[2:6]
    bank_name = banks.get(bank_code)
    return bank_name

def validate_address(address):
    pattern = r'^Ul\.\s[\w\s]+\s\d+[A-Z]?,\s\d{2}-\d{3}\s\w+$'

    if re.match(pattern, address, re.IGNORECASE):
        return True
    else:
        return False

def check_user_exists(id):
    with File(maintain_db, 'users.db') as db:
       try:
         nip = db.get_user_nip_by_id(id)
         if nip != None:
             return True
         else:
             return False
       except:
         raise Exception("Error") 

def format_address(address):
    if address.startswith("ul."):
        return address
    else:
        parts = address.split(", ")
        street = parts[0].split(" ")
        city = parts[1].split(" ")
        number = street[1]
        street = street[0].title()
        index = city[0]
        city = city[1].title()
        formatted_address = f"ul. {street} {number}, {index} {city}"
        return formatted_address

def format_name(name):
        parts = name.split(" ")
        formatted_name = str('')
        for part in parts:
            if len(part) >1:
              part = part.title()
            else:
                part = part.lower()
            formatted_name = str(formatted_name) + str(part) + " "
        return formatted_name