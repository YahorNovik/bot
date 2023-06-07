import requests
import datetime

url_data = f"https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/0000974614?rejestr=P&format=json"
res_data = requests.get(url_data)
if res_data.status_code == 200:
    data = res_data.json()

nazwa = f"{data['odpis']['dane']['dzial1']['siedzibaIAdres']['adres']['ulica']} {data['odpis']['dane']['dzial1']['siedzibaIAdres']['adres']['nrDomu']}, {data['odpis']['dane']['dzial1']['siedzibaIAdres']['adres']['kodPocztowy']} {data['odpis']['dane']['dzial1']['siedzibaIAdres']['adres']['miejscowosc']}"
print(nazwa)