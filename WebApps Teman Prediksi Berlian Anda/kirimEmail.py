from mailjet_rest import Client
from konversi_rupiah import KonversiRupiah
MAIJET_API_KEY = 'fb3bf8be913d33916f010f98a2d19df6'
MAIJET_SECRET_KEY = '16dfdcd00644e87cbdab87da54c55ee0'
# https://github.com/mailjet/mailjet-apiv3-python
kr = KonversiRupiah()
USERNAME = 'artshutter922@gmail.com'
PASSWORD = 'HBP2FtVhzMdA8nwm'

class KirimEmail:
    def __init__(self,
                 pesan_kontak = [1,2,3],
                 harga_asli_usd = 0, data_input_prediksi = [1,2,3,4,5,6,7]
                 ):
        self.pesan_kontak = f"Email Pengirim : {pesan_kontak[0]} \n" \
                           f"Nama Pengirim : {pesan_kontak[1]} \n" \
                           f"Pesan : {pesan_kontak[2]}"
        self.pesan_detailPrediksi = f"Halo, Berikut adalah info detail hasil prediksi berlian berdasarkan model kami \n" \
                     f"Dari hasil input yang telah dilakukan yaitu: \n\n" \
                     f"Carat : {data_input_prediksi[0]} \n" \
                     f"Depth : {data_input_prediksi[4]} \n" \
                     f"Table : {data_input_prediksi[5]} \n" \
                     f"Volume : {data_input_prediksi[6]} \n" \
                     f"Pilihan Potongan  : {data_input_prediksi[1]} \n" \
                     f"Pilihan Warna   : {data_input_prediksi[2]} \n" \
                     f"Pilihan Clarity : {data_input_prediksi[3]} \n\n" \
                     f"Berdasarkan Hasil perhitungan model dengan input di atas dihasilkan prediksi sebagai berikut :\n" \
                     f"Harga prediksi USD : ${harga_asli_usd}\n" \
                     f"Harga prediksi IDR : {kr.harga_hasil_konversi(harga_asli_usd)}\n\n" \
                     f"Catatan Nilai Kurs Rupiah Terhadap Dollar \n" \
                     f"Tanggal {kr.get_day_konversion()} \n" \
                     f"Nilai Rupiah terhadap Dollar USD : {kr.get_last_day_konversi_rate()}" \
 \

    def kirim_email_mailjet(self, user_address_tujuan):

        try:
            mailjet = Client(auth=(MAIJET_API_KEY, MAIJET_SECRET_KEY), version='v3.1')
            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": "artshutter922@gmail.com",
                            "Name": "Feedback User!"
                        },
                        "To": [
                            {
                                "Email": user_address_tujuan,
                                "Name": "You"
                            }
                        ],
                        "Subject": "Pesan Feedback!",
                        "TextPart": self.pesan_kontak
                    }
                ]
            }
            mailjet.send.create(data=data)
        except:
            return False
        else:
            return True

    def kirim_email_detailPrediksi(self, user_address_tujuan):

        try:
            mailjet = Client(auth=(MAIJET_API_KEY, MAIJET_SECRET_KEY), version='v3.1')
            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": "artshutter922@gmail.com",
                            "Name": "Teman Prediksi Berlian Anda!"
                        },
                        "To": [
                            {
                                "Email": user_address_tujuan,
                                "Name": "You"
                            }
                        ],
                        "Subject": "Hasil dan Detail Info Hasil Prediksi Berlian",
                        "TextPart": self.pesan_detailPrediksi
                    }
                ]
            }
            mailjet.send.create(data=data)
        except:
            return False
        else:
            return True
