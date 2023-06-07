from db import maintain_db
from db import File

import sqlite3


path = '/Users/a1/Desktop/lekarz-dentysta/venv/bot/db/users.db'
path = '/Users/a1/Desktop/bot/venv/dev_bot/spendings.db'

# connect to the database
conn = sqlite3.connect('/home/egornovik2010/bot/bot/users.db')

# create a cursor object
cursor = conn.cursor()

#cursor.execute('ALTER TABLE gabinets DROP COLUMN city')
# cursor.execute('DROP TABLE IF EXISTS users')

cursor.execute('''CREATE TABLE users (
                    user_id INTEGER,
                    nip INTEGER,
                    regon INTEGER,
                    address TEXT,
                    city TEXT,
                    name TEXT,
                    registrationDate TEXT,
                    accountNumber INTEGER,
                    PRIMARY KEY (nip, regon, user_id)
                 )''')
# cursor.execute("DROP TABLE gabinets")
# cursor.execute('''CREATE TABLE gabinets (
#                     NIP INTEGER,
#                     USER_NIP INTEGER,
#                     Address TEXT,
#                     Name TEXT,
#                     PRIMARY KEY (NIP, USER_NIP),
#                     FOREIGN KEY (USER_NIP) REFERENCES users(nip)
#                  )''')

#cursor.execute('DROP TABLE IF EXISTS invoices')

# cursor.execute('''CREATE TABLE invoices (
#                     invoice_number TEXT,
#                     issue_date TEXT,
#                     sale_date TEXT,
#                     due_date TEXT,
#                     note TEXT,
#                     payment_method TEXT,
#                     account_number TEXT,
#                     user_nip INTEGER,
#                     user_name TEXT,
#                     user_business_name TEXT,
#                     user_address TEXT,
#                     user_phone TEXT,
#                     gabinet_nip INTEGER,
#                     gabinet_name TEXT,
#                     gabinet_address TEXT,
#                     service_name TEXT,
#                     service_amount INTEGER,
#                     service_unit TEXT,
#                     service_unit_price INTEGER,
#                     service_netto INTEGER,
#                     service_vat INTEGER,
#                     service_vat_amount INTEGER,
#                     service_brutto INTEGER,
#                     total_netto INTEGER,
#                     total_vat_amount INTEGER,
#                     total_brutto INTEGER,
#                     total_brutto_verbally TEXT,
#                     in_total_netto INTEGER,
#                     in_total_vat INTEGER,
#                     in_total_vat_amount INTEGER,
#                     in_total_brutto INTEGER,
#                     PRIMARY KEY (INVOICE_NUMBER, USER_NIP, GABINET_NIP),
#                     FOREIGN KEY (user_nip) REFERENCES users(nip),
#                     FOREIGN KEY (gabinet_nip) REFERENCES gabinets(nip)
#                  )''')

# cursor.execute('''CREATE TABLE payments (
#                     ID INTEGER PRIMARY KEY,
#                     USER_NIP INTEGER,
#                     GABINET_NIP INTEGER,
#                     AMOUNT DECIMAL,
#                     DATE TEXT,
#                     DESCRIPTION TEXT,
#                     FOREIGN KEY (USER_NIP) REFERENCES users(nip),
#                     FOREIGN KEY (GABINET_NIP) REFERENCES gabinets(nip)
#                  )''')

# close the cursor and connection
cursor.close()
conn.close()

