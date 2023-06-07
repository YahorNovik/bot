from bot.db.db import maintain_db
from bot.db.db import File

import sqlite3


path = '/Users/a1/Desktop/lekarz-dentysta/venv/bot/db/users.db'
path = '/Users/a1/Desktop/bot/venv/dev_bot/spendings.db'

# connect to the database
conn = sqlite3.connect('users.db')

# create a cursor object
cursor = conn.cursor()

#cursor.execute('ALTER TABLE gabinets DROP COLUMN city')
# cursor.execute('DROP TABLE IF EXISTS users')

# cursor.execute('''CREATE TABLE users (
#                     user_id INTEGER,
#                     nip INTEGER,
#                     regon INTEGER,
#                     address TEXT,
#                     city TEXT,
#                     name TEXT,
#                     registrationDate TEXT,
#                     accountNumber INTEGER,
#                     PRIMARY KEY (nip, regon, user_id)
#                  )''')
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

cursor.execute('DELETE FROM invoices')
conn.commit()
conn.close()

# execute a SELECT statement to get the table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

# fetch all the rows in the result set
rows = cursor.fetchall()

# extract the table names from the rows and print them
table_names = [row[0] for row in rows]
print(table_names)

cursor.execute("SELECT * FROM USERS")
rows = cursor.fetchall()
for row in rows:
   print(row)

cursor.execute("SELECT * FROM gabinets")
rows = cursor.fetchall()
for row in rows:
   print(row)

cursor.execute("SELECT * FROM payments")
rows = cursor.fetchall()
for row in rows:
   print(row)

with File(maintain_db, 'users.db') as db:

    data=db.get_payments_by_gabinet_and_date(gabinet_nip=9662098244)

for row in data:
   print(row)


# close the cursor and connection
cursor.close()
conn.close()

#with File(maintain_db, "users.db") as db:
#   result = db.get_sum_by_category(111115, '2023-01-15')
#   for i in result:
#      print (f'{i[0]} - {db.get_category_name(i[1])[0]}')

