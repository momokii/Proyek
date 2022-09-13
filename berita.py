import data_saham as ds
import requests
import math
api_endpoint_news = "https://newsapi.org/v2/everything"
api_keys_news = "f77fe8db23134947aab43cffd6a92f31"


class Berita:
    def __init__(self, nama_perusahaan, data_saham: ds.Saham):
        self.nama_perusahaan = nama_perusahaan
        self.data_saham = data_saham
        params_news = {
            'apiKey': api_keys_news,
            'q': self.nama_perusahaan,
            'language': 'en',
            'from': ds.kemarin_lusa,
            'to': ds.kemarin,
            'sortBy': 'popularity'
        }

        try:
            self.response_news = requests.get(url=api_endpoint_news, params=params_news)
        except:
            print('Terjadi Error saat pengambilan info berita')
        else:
            self.berita = self.response_news.json()


    def format_berita(self):
        if self.berita['totalResults'] == 0:
            return f'Tidak ditemukan berita mengenai {self.nama_perusahaan}'
        else:
            self.news_top3 = self.berita['articles'][:3]

            pesan = f"Info Saham {self.nama_perusahaan} ({self.data_saham.stock_code}) Berubah, {self.data_saham.info_perubahan} sekitar {math.floor(self.data_saham.perc_selisih_harga_akhir)}%\n" \
                   f"Harga tanggal : {ds.kemarin} -> ${self.data_saham.harga_akhir_kemarin}\n" \
                   f"Harga tanggal : {ds.kemarin_lusa} -> ${self.data_saham.harga_akhir_kemarin_lusa}\n" \
                   f"Selisih : ${self.data_saham.selisih_harga_akhir} \nPersentase Perubahan : {self.data_saham.perc_selisih_harga_akhir}% \n\n" \
                   f"Berita {self.nama_perusahaan} ditemukan:\n\n" \
                   f"{self.news_top3[0]['title']} \nSumber : {self.news_top3[0]['url']} \n" \
                   f"Isi : \n{self.news_top3[0]['content'].split(' - ')[1]} \n\n--------\n\n" \
                   f"{self.news_top3[1]['title']} \nSumber : {self.news_top3[1]['url']} \n" \
                   f"Isi : \n{self.news_top3[1]['content'].split(' - ')[1]} \n\n--------\n\n" \
                   f"{self.news_top3[2]['title']} \nSumber : {self.news_top3[2]['url']} \n" \
                   f"Isi : \n{self.news_top3[2]['content'].split(' - ')[1]}"

            return pesan

