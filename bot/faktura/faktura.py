from datetime import datetime
from db.db import *
from validation.validation import *
from faktura.faktura_lex import *
from faktura.banks import *
from num2words import num2words
import calendar
import jinja2
import pdfkit
import weasyprint

class Faktura:
 
 def __init__(self, user_nip, gabinet_nip, amount: int =None, payment_method='Przelew', note=note_text):
   self.user_nip = user_nip
   self.gabinet_nip = gabinet_nip
   self.note = note
   self.payment_method = payment_method
   self.amount = amount

 def get_amount(self):
  return 10000
 def get_vat(self):
  return 0
 
 def get_count(self):
  with File(maintain_db) as db: 
      try:
        invoices = db.get_invoices(self.user_nip, self.gabinet_nip)
        return len(invoices) + 1
      except:
        return
  
 def replace_num_to_word(self, amount):
    string = num2words(amount, lang='pl')
    string = string.replace('przecinek', 'PLN')
    parts = string.split('PLN')
    if len(parts) > 1:
        string = parts[0] + 'PLN ' + parts[1] + ' gr'
    else:
        string = parts[0] + ' PLN'
    return string
 
 def get_invoice_number(self, count=1):
  today = datetime.datetime.now()
  month = today.strftime('%m') 
  year = today.strftime('%Y') 
  self.invoice_number =  f"{count}/{month}/{year[-2:]}"

 def set_payment_method(self, payment_method):
  self.payment_method = payment_method

 def get_account_number(self):
    with File(maintain_db) as db: 
      try:
        account_number = db.get_user_account_by_nip(self.user_nip)
      except:
        return
    self.account_number = account_number
    self.bank = get_bank_name_by_number(account_number)

 def get_dates(self):
    today = datetime.date.today()
    if today.day == calendar.monthrange(today.year, today.month)[1]:
        self.sale_date = today
        self.due_date = str(today + datetime.timedelta(weeks=1))
    else:
        sale_date_temp = today.replace(day=1) - datetime.timedelta(days=1)
        if today > sale_date_temp + datetime.timedelta(weeks=1):
            self.sale_date = today
            self.due_date = str(today + datetime.timedelta(weeks=1))
        else:
            self.sale_date = sale_date_temp
            self.due_date = str(sale_date_temp + datetime.timedelta(weeks=1))

    self.issue_date = str(today)
    self.sale_date_word = month[self.sale_date.strftime("%B")]

 def set_dates(self, issue_date=None, sale_date=None, due_date=None):
  if issue_date is not None:
    self.issue_date = issue_date
  if sale_date is not None:
    self.sale_date = sale_date
  if due_date is not None:
    self.due_date = due_date

 def get_user_data(self):
    with File(maintain_db) as db: 
      try:
        user_data = db.get_user_data_by_nip(self.user_nip)
      except:
        return
    self.user = {'name': user_data[2],
                 'business_name': f"{business_name_text} {user_data[2]}",
                 'address': f"{user_data[0]} {user_data[1]}",
                 'nip': self.user_nip,
                 'bank': get_bank_name_by_number(user_data[3]),
                 'account_number': user_data[3],
                 'phone': ""}
    print(user_data[3])

 def get_gabinet_data(self):
    with File(maintain_db) as db: 
      try:
        gabinet_data = db.get_gabinet_data_by_nip(self.gabinet_nip)
      except:
        return
    self.gabinet = {'business_name': format_name(gabinet_data[1]),
                    'address': format_address(gabinet_data[0]),
                    'nip': self.gabinet_nip}

 def get_service_data(self):
  
  if self.amount is None:
    brutto = self.get_amount()
  else:
    brutto = self.amount
  vat = self.get_vat()
  vat_amount = brutto * self.get_vat()
  netto = brutto - vat
  self.service = {'name': f"{service} - {self.sale_date_word}",
                  'amount': 1,
                  'unit': unit,
                  'unit_price_netto': netto,
                  'price_netto': netto,
                  'vat_perc': vat,
                  'vat_value': vat_amount,
                  'price_brutto': brutto }

  self.in_total = { 'price_netto': netto,
                    'vat_value': vat_amount,
                    'price_brutto': brutto,
                    'price_brutto_verbally': self.replace_num_to_word(brutto)}
  
  self.in_total_details = {'price_netto': netto,
                           'vat_perc': vat,
                           'vat_value': vat_amount,
                           'price_brutto': brutto}
 def set_service_data(self, service, in_total, in_total_details):
    if service is None or in_total is None or in_total_details is None:
     return
    else:
     self.service = service
     self.in_total = in_total
     self.in_total_details = in_total_details

 def get_data(self):
  
  self.get_invoice_number(self.get_count())
  self.get_account_number()
  self.get_dates()
  self.get_user_data()
  self.get_gabinet_data()
  self.get_service_data()

  self.data = {'invoice_number': self.invoice_number,
               'issue_date': self.issue_date,
               'sale_date': self.sale_date,
               'due_date': self.due_date,
               'notes': self.note,
               'payment_method': self.payment_method,
               'account_number': self.account_number,
               'user': self.user,
               'cabinet': self.gabinet,
               'services': [ self.service],
               'in_total': self.in_total ,
               'in_total_details': [self.in_total_details]}
  return self.data
 
#  def get_faktura(self, data):
#    with open('/home/egornovik2010/bot/bot/faktura/invoice-template.html.jinja', 'r', encoding='utf-8') as f:
#     template_str = f.read()
#    print('generating invoice...')
#    template = jinja2.Template(template_str)   
#    rendered_template = template.render(**data)
#    wkhtmltopdf="/home/egornovik2010/bot/bot/faktura/wkhtmltox_0.12.6.1-2.bullseye_amd64.deb" 
#    #/venv/bot/faktura
#    #"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe" 
#    options={"enable-local-file-access": ""}
#    css=['/home/egornovik2010/bot/bot/faktura/css/style2.css', '/home/egornovik2010/bot/bot/faktura/css/reset.css']
#    file = str(f"/home/egornovik2010/bot/bot/faktura/faktury/Faktura.pdf")
#    pdfkit.from_string(rendered_template, file, configuration=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf), options=options, css=css)
#    with File(maintain_db) as db: 
#        try:
#          db.add_invoice(data)
#          return data['invoice_number']
#        except:
#          return
 def get_faktura(self, data):
    template_path = 'bot/faktura/invoice-template.html.jinja'
    css_paths = ['bot/faktura/css/style2.css', 'bot/faktura/css/reset.css']
    output_pdf_path = 'bot/faktura/faktury/Faktura.pdf'

    with open(template_path, 'r', encoding='utf-8') as f:
        template_str = f.read()

    template = jinja2.Template(template_str)
    rendered_template = template.render(**data)

    rendered_html = weasyprint.HTML(string=rendered_template)
    rendered_pdf = rendered_html.write_pdf(stylesheets=css_paths)

    with open(output_pdf_path, 'wb') as pdf_file:
        pdf_file.write(rendered_pdf)

    with File(maintain_db) as db:
        try:
            db.add_invoice(data)
            return data['invoice_number']
        except:
            return
    
  



