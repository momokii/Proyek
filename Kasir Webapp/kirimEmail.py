from mailjet_rest import Client
MAIJET_API_KEY = 'fb3bf8be913d33916f010f98a2d19df6'
MAIJET_SECRET_KEY = '16dfdcd00644e87cbdab87da54c55ee0'
# https://github.com/mailjet/mailjet-apiv3-python

USERNAME = 'artshutter922@gmail.com'
PASSWORD = 'HBP2FtVhzMdA8nwm'

class KirimEmail:
    def __init__(self,carts, transaksi, member ):
        all_carts = [data for data in carts]
        pesan_carts = ""
        for data in all_carts:
            pesan = f"- {data.nama_makanan} | Harga : {data.harga} | Diskon : {data.diskon}% | Jumlah dipesan : {data.jumlah} \n"
            pesan_carts = pesan_carts + pesan

        self.pesan = f"Halo kak {member.nama_member}, Terima Kasih telah mengunjungi Solim Efac \n" \
                    f"Berikut adalah transaksi terbaru kak {member.nama_member} di kedai kami: \n\n" \
                    f"Detail Pesanan Makanan/Minuman: \n" \
                    f"{pesan_carts} \n" \
                    f"Jumlah Jenis Barang di order : {transaksi.total_jenisBarang} \n" \
                    f"Jumlah Total Barang di order : {transaksi.total_order} \n" \
                    f"Total Harga : {transaksi.total_harga} \n" \
                    f"Total Diskon : {transaksi.total_diskon} \n" \
                    f"Total Harga Akhir : {transaksi.harga_akhir} \n" \
                    f"Total Bayar : {transaksi.total_bayar} \n" \
                    f"Kembalian di Terima : {transaksi.kembalian} \n" \
                    f"Tanggal dan Waktu Order : {transaksi.tanggal_order} | {transaksi.waktu_order} \n\n" \
                    f"Terima kasih atas kunjungannya, selalu kami tunggu kunjungan serta order selanjutnya dan seterusnya dari kak {member.nama_member}" \


    def kirim_email_mailjet(self, user_address_tujuan):

        try:
            mailjet = Client(auth=(MAIJET_API_KEY, MAIJET_SECRET_KEY), version='v3.1')
            data = {
                'Messages': [
                    {
                        "From": {
                            "Email": "artshutter922@gmail.com",
                            "Name": "Detail Transaksi Solim Efac"
                        },
                        "To": [
                            {
                                "Email": user_address_tujuan,
                                "Name": "Member Solim Efac"
                            }
                        ],
                        "Subject": "Total Pembelian Anda!",
                        "TextPart": self.pesan
                    }
                ]
            }
            mailjet.send.create(data=data)
        except:
            return False
        else:
            return True
