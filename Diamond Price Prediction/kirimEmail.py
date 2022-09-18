import smtplib
from mailjet_rest import Client
from konversi_rupiah import KonversiRupiah
MAIJET_API_KEY = 'MAILJET_API_KEY'
MAIJET_SECRET_KEY = 'MAILJET_SECRET'
# https://github.com/mailjet/mailjet-apiv3-python
kr = KonversiRupiah()

class KirimEmail:
    def __init__(self, harga_asli_usd, data_input_prediksi):
        self.pesan = f"Halo, Berikut adalah info detail hasil prediksi berlian berdasarkan model kami \n" \
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


    def kirim_email_mailjet(self, user_address_tujuan):

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
                        "TextPart": self.pesan
                    }
                ]
            }
            mailjet.send.create(data=data)
        except:
            return False
        else:
            return True
