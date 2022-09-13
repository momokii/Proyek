import requests
import datetime

# const
hari_sekarang = datetime.datetime.today()
kemarin = (hari_sekarang - datetime.timedelta(days = 1)).date()
kemarin_lusa = (hari_sekarang - datetime.timedelta(days = 2)).date()

api_endpoint_stock = 'https://www.alphavantage.co/query'
api_keys_stock = 'YOUR_API_KEYS'


class Saham:
    def __init__(self, stock_code):
        self.stock_code = stock_code
        params_stock = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': self.stock_code,
            'outputsize': 'compact',
            'datatype': 'json',
            'apikey': api_keys_stock
        }


        self.response_stock = requests.get(url= api_endpoint_stock, params= params_stock)

        self.data_stock_kemarin = self.response_stock.json()['Time Series (Daily)'][str(kemarin)]
        self.data_stock_kemarin_lusa = self.response_stock.json()['Time Series (Daily)'][str(kemarin_lusa)]
        self.harga_akhir_kemarin = float(self.data_stock_kemarin['4. close'])
        self.harga_akhir_kemarin_lusa = float(self.data_stock_kemarin_lusa['4. close'])
        self.selisih_harga_akhir = abs(round(self.harga_akhir_kemarin - self.harga_akhir_kemarin_lusa, 2))
        self.perc_selisih_harga_akhir = round((self.selisih_harga_akhir / self.harga_akhir_kemarin * 100), 2)

        self.info_perubahan = ''

        self.cek_perubahan()

    def cek_perubahan(self):
        if self.harga_akhir_kemarin > self.harga_akhir_kemarin_lusa:
            self.info_perubahan = 'naik'
        else:
            self.info_perubahan = 'turun'














