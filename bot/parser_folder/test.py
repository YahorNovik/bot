import requests
import datetime

def get_gabinet_data(nip):

  today = datetime.date.today()

  date = today.strftime('%Y-%m-%d')
  
  url = f"https://wl-api.mf.gov.pl/api/search/nip/{nip}?date={date}"

  res = requests.get(url)

  if res.status_code == 200:
    data = res.json()
    if data['result']['subject'] == None:
        url_id = f"https://dane.biznes.gov.pl/api/mswf/v1/SearchAdvance?nip={nip}&pageNumber=0&pageSize=20"
        res = requests.get(url_id)

        if res.status_code == 200:
          json_data = res.json()     
          source = json_data['companyList'][0]['source']
          if source == "CEIDG":
            id = json_data['companyList'][0]['id']
            date = json_data['companyList'][0]['registerDate']
            url_data = f"https://dane.biznes.gov.pl/api/mswf/v1/GetCompanyDetails?id={id}"

            res_data = requests.get(url_data)
            if res_data.status_code == 200:
              data = res_data.json()
              user_data = { "Name": data['basicData']['name'],
                            "NIP": nip,
                            "REGON": data['basicData']['regon'],
                            "Address": f"{data['addressData']['correspondenceAddress']['street']} {data['addressData']['correspondenceAddress']['buildingNumber']}, {data['addressData']['correspondenceAddress']['postcode']} {data['addressData']['correspondenceAddress']['city']}",}
              return user_data
          elif source == "KRS":
            url_id = f"https://dane.biznes.gov.pl/api/mswf/v1/SearchAdvance?nip={nip}&pageNumber=0&pageSize=20"
            res = requests.get(url_id)
            if res.status_code == 200:
              krs = json_data['companyList'][0]['krs']
              url_data = f"https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{krs}?rejestr=P&format=json"
              res_data = requests.get(url_data)
              if res_data.status_code == 200:
                data = res_data.json()
                user_data = { "Name": data["odpis"]["dane"]["dzial1"]["danePodmiotu"]["nazwa"],
                              "NIP": nip,
                              "REGON": data['odpis']['dane']['dzial1']['danePodmiotu']['identyfikatory']['regon'],
                              "Address": f"{data['odpis']['dane']['dzial1']['siedzibaIAdres']['adres']['ulica']} {data['odpis']['dane']['dzial1']['siedzibaIAdres']['adres']['nrDomu']}, {data['odpis']['dane']['dzial1']['siedzibaIAdres']['adres']['kodPocztowy']} {data['odpis']['dane']['dzial1']['siedzibaIAdres']['adres']['miejscowosc']}"}
                print(user_data)
                return user_data
        else:
          raise Exception("Error")
    else:
      if type(data['result']['subject']['workingAddress']) != "None":
        address = data['result']['subject']['residenceAddress']
      else:
        address = data['result']['subject']['workingAddress']

      gabinet_data = { "Name": data['result']['subject']['name'],
                       "NIP": nip,
                       "REGON": data['result']['subject']['regon'],
                       "Address": address }
      return gabinet_data
  else:
    raise Exception("Error")

  

get_gabinet_data(8943187795)