import tkinter
from tkinter import messagebox
THEME_COLOR = "#375362"


VAR_INFO = {
    'Carat' : 'Carat menunjukkan berat berlian, bukan ukurannya, satu Carat bernilai 0.2 grams \n'
              '\nSumber : tiffany.com/engagement/the-tiffany-guide-to-diamonds/carat/',
    'Table' : 'Table merupakan sisi datar berbentuk persegi pada bagian atas berlian dan berperan penting dalam penampilan berlian. Table akan membiaskan sinar yang mereka lewati dan memantulkannya ke sudut lainnya yang membuat berlian menjadi berkilau \n'
              '\nSumber : \n'
              'brilliance.com/education/diamonds/depth-table',
    'Volume' : 'Volume dari berlian, dihitung dengan \n'
               'Volume = X * Z * Y',
    'Depth' : 'Depth (Kedalaman), bisa disebut juga tinggi merupakan jarak dari Table berlian ke Culet (ujung runcing) berlian \n'
               '\nSumber : \n'
              'brilliance.com/education/diamonds/depth-table',
    'Potongan' : 'Merupakan ukuran yang memberitahukan seberapa baik berlian dipotong dan dipoles, termasuk sebeapa proporsional batu tersebut, kedalamannya (depth), dan simetrinya \n'
                 'Dari list yang diberikan urutan kualitas potongan dari yang terbaik sampai yang biasa adalah \n'
                 'Premium - Very Good - Good - Fair - Ideal \n'
                 '\nSumber : \n'
                 'diamonds.pro/education/cuts/',
    'Warna' : 'Merupakan code warna dari berlian, dalam berlian code warna bisa dibagi menjadi 3 tipe dan tiap tipe memiliki beberapa kode warna yang menujukkan kualitas berlian \n'
              '- Colorless (D, E, F) \n'
              '- Near Colorless (G, H, I, J) \n'
              '- Faint Yellow (K, L, M) \n'
              'Secara kualitas, Colorless merupakan yang terbaik, urutan terbaik ke paling kurang baik diurutkan secara urutan abjad dari D - M \n'
              '\nSumber : \n'
              'brilliance.com/education/diamonds/color',
    'Clarity' : 'Clarity (kejernihan) berlian mengacu pada ada tidaknya inklusi (cacat dalam berlian) dan noda (cacat pada permukaan berlian) yang nantinya dua hal tersebut dapat menentukan penempatan grading dari kualitas clarity berlian \nKemudian list yang tersedia urutan secara runut dari kualitas Clarity terbaik ke paling biasa adalah \nIF - VVS1 - VVS2 - VS1 - VS2 - SI1 - SI2 - I1 \n'
                '\nSumber : \n4cs.gia.edu/en-us/diamond-clarity/',
}


class InfoVar_UI:
    def __init__(self):
        self.jendela_info = tkinter.Tk()
        self.jendela_info.title('Info Variabel')
        self.frame = tkinter.Frame(self.jendela_info, bg= THEME_COLOR)
        self.frame.pack()

        self.label_judul = tkinter.Label(self.frame, text='Info Variabel, klik di bawah!', font=('Courier', 12))
        self.label_judul.grid(row=1, column=0)
        self.label_judul.config(bg=THEME_COLOR, fg='white', pady=15, padx= 15)

        self.button_carat = tkinter.Button(self.frame, text='Info Carat',
                                           command= lambda: self.info_variabel_numerik('Carat', 0, 2))
        self.button_carat.grid(row=2, column=0, pady=10)

        self.button_warna = tkinter.Button(self.frame, text='Info Warna',
                                           command= lambda: self.info_variabel_kategorikal('Warna'))
        self.button_warna.grid(row=3, column=0, pady=10)

        self.button_potongan = tkinter.Button(self.frame, text='Info Potongan',
                                              command= lambda: self.info_variabel_kategorikal('Potongan'))
        self.button_potongan.grid(row=4, column=0, pady=10)

        self.button_clarity = tkinter.Button(self.frame, text='Info Clarity',
                                             command= lambda: self.info_variabel_kategorikal('Clarity'))
        self.button_clarity.grid(row=5, column=0, pady=10)

        self.button_depth = tkinter.Button(self.frame, text='Info Depth',
                                           command= lambda: self.info_variabel_numerik('Depth', 50, 70))
        self.button_depth.grid(row=6, column=0, pady=10)

        self.button_table = tkinter.Button(self.frame, text='Info Table',
                                           command= lambda: self.info_variabel_numerik('Table', 45, 70))
        self.button_table.grid(row=7, column=0, pady=10)

        self.button_volume = tkinter.Button(self.frame, text='Info Volume',
                                            command= lambda: self.info_variabel_numerik('Volume', 40, 325))
        self.button_volume.grid(row=8, column=0, pady=10)

        self.button_dataset = tkinter.Button(self.frame, text='Info Dataset dan \nModel',
                                             command= self.info_dataset_model)
        self.button_dataset.config(bg= 'black', fg= 'white')
        self.button_dataset.grid(row=9, column=0, pady=10)

        self.label_judul_bawah = tkinter.Label(self.frame, text='-------------------------', font=('Courier', 12))
        self.label_judul_bawah.grid(row=10, column=0)
        self.label_judul_bawah.config(bg=THEME_COLOR, fg='white', pady=10)

    def info_dataset_model(self):
        messagebox.showinfo(title= 'Info Model And Dataset',
                            message='Isi Infonya')

    def info_variabel_numerik(self, nama_var, batasBawah, batasAtas):
        tambahan = ''
        if nama_var != 'Carat':
            tambahan = 'Satuan : Milimeter (mm)\n'
        messagebox.showinfo(title= f'Info variabel {nama_var}',
                            message=f"Ketentuan Input Variabel : \n\n"
                                    f"Nama Variabel : {nama_var}\n"
                                    f"Tipe Variabel : Numerik \n"
                                    f"{tambahan}"
                                    f"Range Input : {batasBawah} < X < {batasAtas} \n\n"
                                    f"Info dari variabel {nama_var} : \n"
                                    f"{VAR_INFO[nama_var]} \n \n"
                                    f"Catatan: \n"
                                    f"Pemberian batas input pada variabel {nama_var} karena model prediksi dilakukan pelatihan pada range diatas, jadi untuk pemaksimalan hasil prediksi diberikan batasan di atas, Terima Kasih!"
                                    )



    def info_variabel_kategorikal(self, nama_var):
        messagebox.showinfo(title= f'Info Variabel {nama_var}',
                            message=f'Variabel {nama_var} bertipe Kategorikal hanya dapat diinputkan dari list yang sudah disediakan \n\n'
                                    f'Info dari variabel {nama_var} : \n'
                                    f'{VAR_INFO[nama_var]}\n\n'
                                    f'Catatan : \n'
                                    f'Pemberian pilihan input pada variabel {nama_var} karena model prediksi dilakukan dengan menggunakan data yang ada pada list yang disediakan.\n'
                                    f'Jadi jika Anda memasukkan nilai baru, program akan gagal karena ditakutkan hasil prediksi yang dihasilkan tidak baik, Terima Kasih!'
                                    f'')




