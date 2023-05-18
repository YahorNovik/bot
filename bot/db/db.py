import sqlite3 as sql
import datetime

class File():
    def __init__(self, object, db_file="users.db"):
        self.object = object
        self.db = db_file
    def __enter__(self):
        self.conn = self.object(self.db)
        return self.conn
    def __exit__(self, *args, **kwargs):
        self.conn.close()

class maintain_db:

    def __init__(self, db_file):
        self.conn = sql.connect(db_file) 
        print('connected to db..')
        self.cursor = self.conn.cursor()
    
    def add_record_users(self, user_id, nip, regon, address, city, name, date):
        print('adding record user..')
        self.cursor.execute("INSERT INTO 'users' ('user_id','nip', 'regon', 'name', 'address', 'city', 'registrationDate') VALUES(?, ?, ?, ?, ?, ?, ?)",
                           (user_id, nip, regon, name, address, city, date))
        return self.conn.commit()
    
    def add_account_number(self, user_nip, account_number):
        print('adding account number for user..')
        self.cursor.execute("UPDATE 'users' SET accountNumber=? WHERE nip=?", (account_number, user_nip))
        return self.conn.commit()
    
    def add_record_gabinets(self, nip, user_nip, name, address):
        print('adding record gabinet..')
        self.cursor.execute("INSERT INTO 'gabinets' ('nip', 'user_nip', 'name', 'address') VALUES(?, ?, ?, ?)",
                           (nip, user_nip, name, address))
        return self.conn.commit()
    
    def add_record_payments(self, user_nip, gabinet_nip, amount, date):
        print('adding record payment..')
        self.cursor.execute("INSERT INTO 'payments' ('user_nip', 'gabinet_nip', 'amount', 'date', 'description') VALUES(?, ?, ?, ?, ?)",
                           (user_nip, gabinet_nip, amount, date, ""))
        payment_id = self.cursor.lastrowid
        self.conn.commit()
        return payment_id
    
    def get_user_nip_by_id(self, user_id):
        print('getting user nip by user id..')
        self.cursor.execute("SELECT nip FROM 'users'WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def get_user_account_by_nip(self, nip):
        print('getting user account number by user nip..')
        self.cursor.execute("SELECT accountNumber FROM users WHERE nip=?", (nip,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    
    def get_user_data_by_nip(self, nip):
        print('getting user data by user nip..')
        self.cursor.execute("SELECT address, city, name FROM users WHERE nip=?", (nip,))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            return None

    def get_gabinet_data_by_nip(self, nip):
        print('getting gabinet data by nip..')
        self.cursor.execute("SELECT address, name FROM gabinets WHERE nip=?", (nip,))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            return None
    
    def get_gabinets_by_user_nip(self, user_nip):
        print('getting gabinets by user nip..')
        self.cursor.execute("SELECT nip, name FROM 'gabinets' WHERE user_nip=?", (user_nip,))
        return self.cursor.fetchall()
    
    def set_description(self, payment_id, description):
        print('setting description for payment..')
        self.cursor.execute("UPDATE 'payments' SET description=? WHERE id=?", (description, payment_id))
        return self.conn.commit()
    
    def get_payments(self, start_date=None, end_date=None):
        print('getting payments within date range..')
        date_format = '%Y-%m-%d' # specify date format
        if start_date is None:
            start_date = datetime.datetime.now() - datetime.timedelta(days=7) # default to last week
        else:
            start_date = datetime.datetime.strptime(start_date, date_format)
        if end_date is None:
            end_date = datetime.datetime.now()
        else:
            end_date = datetime.datetime.strptime(end_date, date_format)
        self.cursor.execute("SELECT * FROM 'payments' WHERE date BETWEEN ? AND ? ORDER BY id DESC", (start_date.strftime(date_format), end_date.strftime(date_format)))
        return self.cursor.fetchall()
    
    def get_payments_by_gabinet_and_date(self, gabinet_nip:int, start_date:str=None, end_date:str=None):
        print('getting payments within gabinet_nip..')
        payments = self.get_payments(start_date, end_date)

        filtered_payments = [p for p in payments if p[2] == gabinet_nip]
        return filtered_payments
    
    def get_gabinet_name(self, gabinet_nip):
        print('getting gabinet name by nip..')
        self.cursor.execute("SELECT name FROM 'gabinets' WHERE nip=?", (gabinet_nip,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    
    def get_last_payment_id(self):
        print('getting last payment..')
        self.cursor.execute("SELECT id FROM 'payments' ORDER BY id DESC LIMIT 1")
        return self.cursor.fetchone()[0]
    
    def edit_payment(self, payment_id, gabinet_nip=None, amount=None):
        print('editing payment..')

        if gabinet_nip is not None:
            self.cursor.execute("UPDATE 'payments' SET gabinet_nip=? WHERE id=?", (gabinet_nip, payment_id))

        if amount is not None:
            self.cursor.execute("UPDATE 'payments' SET amount=? WHERE id=?", (amount, payment_id))

        return self.conn.commit()
    
    def delete_payment(self, payment_id:int != None):
        print('deleting payment..')
        self.cursor.execute("DELETE FROM 'payments' WHERE id=?", (payment_id,))
        return self.conn.commit()
    
    def add_invoice(self, data):
        print('adding invoice...')
        #self.cursor.execute("INSERT INTO 'invoices' (invoice_number, issue_date, sale_date, due_date, note, payment_method, account_number, user_nip, user_name, user_business_name, user_address, user_phone, gabinet_nip, gabinet_name, gabinet_address, service_name, service_amount, service_unit, service_unit_price, service_netto, service_vat, service_vat_amount, service_brutto, total_netto, total_vat_amount, total_brutto, total_brutto_verbally, in_total_netto, in_total_vat, in_total_vat_amount, in_total_brutto) VALUES(?, ?, ?, ?, ?)",
        self.cursor.execute("INSERT INTO 'invoices' (invoice_number, issue_date, sale_date, due_date, note, payment_method, account_number, user_nip, user_name, user_business_name, user_address, user_phone, gabinet_nip, gabinet_name, gabinet_address ) VALUES(?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?)",
                           (data['invoice_number'], data['issue_date'], data['sale_date'], data['due_date'], data['notes'], data['payment_method'], data['account_number'], data['user']['nip'], data['user']['name'], data['user']['business_name'], data['user']['address'], data['user']['phone'], data['cabinet']['nip'], data['cabinet']['business_name'], data['cabinet']['address']))
        self.conn.commit()
    
    def get_invoices(self, user_nip, gabinet_nip):
        print('getting invoices...')
        current_month = datetime.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        query = "SELECT * FROM invoices WHERE user_nip = ? AND gabinet_nip = ? AND issue_date >= ?"
        self.cursor.execute(query, (user_nip, gabinet_nip, current_month))
        result = self.cursor.fetchall()
        return result    
    
    def close(self):
        self.conn.close()
        print('connection was closed..')