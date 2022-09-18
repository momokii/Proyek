import requests
import datetime
API_KEY = '9ZNITM0FYYRAIMUF'
URL_VANTAGE = 'https://www.alphavantage.co/query'
MINGGU = 6
SABTU = 5


LASTDAY = datetime.datetime.today().date() - datetime.timedelta(days= 1)
if LASTDAY.weekday() == MINGGU:
    LASTDAY = LASTDAY - datetime.timedelta(days=2)
elif LASTDAY.weekday() == SABTU:
    LASTDAY = LASTDAY - datetime.timedelta(days=1)

PARAMS = {
        'function': 'FX_DAILY',
        'from_symbol': 'USD',
        'to_symbol': 'IDR',
        'apikey': API_KEY
    }

class KonversiRupiah:
    def __init__(self):
        self.LASTDAY = datetime.datetime.today().date() - datetime.timedelta(days= 1)


    def check_weekend_detected(self):
        if self.LASTDAY.weekday() == MINGGU:
            self.LASTDAY = self.LASTDAY - datetime.timedelta(days=2)
        elif self.LASTDAY.weekday() == SABTU:
            self.LASTDAY = self.LASTDAY - datetime.timedelta(days=1)

        return self.LASTDAY

    # dapatkan tanggal "hari" sebelumnya
    def get_day_konversion(self):
        self.LASTDAY = self.check_weekend_detected()

        return self.LASTDAY

    # cari nilai tukar konversi pada hari "sebelumnya"
    def get_last_day_konversi_rate(self):
        self.response = requests.get(url= URL_VANTAGE, params = PARAMS).json()

        try:
            kemarin = float(self.response['Time Series FX (Daily)'][str(LASTDAY)]['4. close'])
            # 'kemungkinan' ada jika hari sudah ganti, tapi nilai hari sebelumnya belum keluar, maka hal di atas bisa error, kemudian masuk ke except
        except:
            try:
                kemarin = float(self.response['Time Series FX (Daily)'][str(LASTDAY - datetime.timedelta(days=1))]['4. close'])
                '''
                di sini pasang try-catch lagi karena ada kemungkinan terjadi pada hari selasa pada try awal gagal karena nilai hari senin belum keluar, otomatis jika masuk ke sini dan jalankan try ini maka akan cari hari minggu karena senin - 1 -> minggu, dan itu sudah pasti gagal, karena tidak ada transaksi di hari minggu
                Maka perlu ada nested try-catch disini untuk check weekend jika bagian ini gagal 
                '''
            except:
                self.LASTDAY = LASTDAY - datetime.timedelta(days=1) # kurangi LASTDAY dengan -1, agar menyamai input lastday pada TRY bagian ini
                kemarin = float( self.response['Time Series FX (Daily)'][self.check_weekend_detected()]['4. close'])

        return kemarin


    def harga_hasil_konversi(self, harga_usd):

        return round((self.get_last_day_konversi_rate() * harga_usd), 2)








