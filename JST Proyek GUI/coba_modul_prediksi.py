import tkinter
THEME_COLOR = "#375362"
from infovar_ui import InfoVar_UI
import smtplib
my_email = 'artshutter922@gmail.com'
password = 'Kelana.helyandika66'

MAIJET_API_KEY = 'fb3bf8be913d33916f010f98a2d19df6'
MAIJET_SECRET_KEY = '16dfdcd00644e87cbdab87da54c55ee0'

'''
import prediksi
import requests
import datetime







TODAY = datetime.datetime.today().date()
FILE_MODEL = 'model'
API_KEY = '9ZNITM0FYYRAIMUF'
URL_VANTAGE = 'https://www.alphavantage.co/query'


model = prediksi.Prediksi(FILE_MODEL)

carat = input('carat :')
potongan = input('potongan : ')
warna = input('warna :')
clarity = input('clarity : ')
depth = input('depth : ')
table = input('table : ')
volume = input('volumne : ')

inputan_user = [carat, potongan, warna, clarity, depth, table, volume]

params = {
    'function' : 'FX_DAILY',
    'from_symbol' : 'USD',
    'to_symbol' : 'IDR',
    'apikey' : API_KEY
}

response = requests.get(url= URL_VANTAGE, params= params)
kurs_hari_ini = int(float(response.json()['Time Series FX (Daily)'][str(TODAY)]['4. close']))
harga_prediksi = int(model.prediksi(inputan_user))
harga_rupiah = kurs_hari_ini * harga_prediksi

pesan_kirim = f'Berikut adalah laporan hasil prediksi Berlian dengan keterangan : \n' \
              f'Carat : {carat} \nWarna : {warna} \nJenis Potongan : {potongan} \n' \
              f'Tipe Clarity : {clarity} \n' \
              f'Besaran Depth : {depth} \nBesaran Table : {table} \nVolume Berlian : {volume}\n\n' \
              f'Prediksi harga berlian adalah : ${harga_prediksi}\n' \
              f'Harga Prediksi : ${harga_prediksi}\n' \
              f'Harga Rupiah : {harga_rupiah} dengan kurs tanggal {TODAY} adalah {kurs_hari_ini}'

print(pesan_kirim)
'''


def kirim_email_mailjet(user_address_tujuan):
  from mailjet_rest import Client
  MAIJET_API_KEY = 'fb3bf8be913d33916f010f98a2d19df6'
  MAIJET_SECRET_KEY = '16dfdcd00644e87cbdab87da54c55ee0'
  mailjet = Client(auth=(MAIJET_API_KEY, MAIJET_SECRET_KEY), version='v3.1')
  data = {
    'Messages': [
      {
        "From": {
          "Email": "artshutter922@gmail.com",
          "Name": "Me"
        },
        "To": [
          {
            "Email": user_address_tujuan,
            "Name": "You"
          }
        ],
        "Subject": "My first Mailjet Email!",
        "TextPart": 'cekk'
      }
    ]
  }
  result = mailjet.send.create(data=data)
  print(result.status_code)

kirim_email_mailjet('kelanachandra7@gmail.com')



'''
# --------------------------------------
import psycopg2

conn = psycopg2.connect(host = 'localhost',
                        database = 'Employees',
                        user = 'postgres',
                        password = 'postgres')
cur = conn.cursor()

cur.execute('select * from titles;')

rows = cur.fetchall()

l = 0
for r in rows:
    print(f"{r[0]} {r[1]}")
    l = l + 1
    if l == 10:
        break



conn.close()
# --------------------------------------

def cari_info():
    infoVar = InfoVar_UI()

wd = tkinter.Tk()
wd.config(bg = THEME_COLOR, pady= 20, padx=20)

button_info = tkinter.Button(text= 'Info Variabel', command= cari_info)
button_info.grid(row=8, column=1,  pady= 10)


wd.mainloop()

'''

