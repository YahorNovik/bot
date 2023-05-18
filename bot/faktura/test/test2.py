import datetime
from bot.db.db import *
from bot.faktura.faktura import *
from num2words import num2words

def replace_przecinek(string):
    string = num2words(string, lang='pl')
    words = string.split()
    result = []
    for i, word in enumerate(words):
        if word == "przecinek":
            result.append("PLN")
            if i + 1 < len(words):
                gr = words[i+1].replace("zero", "").replace("jeden", "jedna").replace("dwa", "dwie")
                if gr:
                    result.append(gr + " gr")
            break
        else:
            result.append(word)
    return " ".join(result)

def replace_num_to_word( amount):
    string = num2words(amount, lang='pl')
    string = string.replace('przecinek', 'PLN')
    parts = string.split('PLN')
    if len(parts) > 1:
        string = parts[0] + 'PLN' + parts[1] + ' gr'
    else:
        string = parts[0] + ' PLN'
    return string

print(replace_num_to_word(12300))

# faktura = Faktura('8943186123', '9662098244')

# data=faktura.get_data()

# faktura.get_faktura(data)

# today = datetime.date.today()
# start_date = datetime.date(today.year, today.month, 1)
# end_date = start_date.replace(day=28) + datetime.timedelta(days=4)
# end_date = end_date - datetime.timedelta(days=end_date.day)

# with File(maintain_db, 'users.db') as db:
#     payments = db.get_payments_by_gabinet_and_date(int('9662098244'), str(start_date), str(end_date))

# total = 0
# for item in payments:
#     total += item[3]

# print(total)


# today = datetime.date.today() # get today's date
# last_month = datetime.date.today().replace(day=1) - datetime.timedelta(days=1) # get last month's last day

# print(today)
# print(last_month)
# print(last_month + datetime.timedelta(weeks=1))

# month = {'January': 'styczeń', 
#           'February': 'luty', 
#           'March': 'marzec',
#           'April': 'kwiecień', 
#           'May': 'maj', 
#           'June': 'czerwiec', 
#           'July': 'lipiec', 
#           'August': 'sierpień', 
#           'September': 'wrzesień', 
#           'October': 'październik', 
#           'November': 'listopad', 
#           'December': 'grudzień'}


# month_name_pl = last_month.strftime("%B")
# print(month[month_name_pl])

# from num2words import num2words

# num = 10156
# words = num2words(num, lang='pl')
# print(words)
