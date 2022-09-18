import tkinter
import re
from tkinter import ttk, messagebox
from prediksi import Prediksi
from kirimEmail import KirimEmail
from infovar_ui import InfoVar_UI
from PIL import Image, ImageTk
THEME_COLOR = "#375362"
FILE_MODEL = 'model'
# tkinter widgets -> https://coderslegacy.com/python/list-of-tkinter-widgets/



# ---------------------------------# VARIABEL GLOBAL #------------------------------------- #
entry_email = None
data_input = []
harga_prediksi_usd = 0



# ---------------------------------# FUNGSI #------------------------------------- #

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def check_email(email):
    if (re.search(regex, email)):
        return True
    else:
        messagebox.showerror(title= 'Email Salah!', message= 'Mohon Maaf, Anda tidak Memasukkan Format Email yang sesuai')


def kirim_email(harga_asli_usd, data_input_prediksi,
                entry_email):

    kirim_email = KirimEmail(harga_asli_usd = harga_asli_usd,
                             data_input_prediksi= data_input_prediksi)
    check_kirim_email = kirim_email.kirim_email_mailjet(
        user_address_tujuan = entry_email
    )
    if check_kirim_email:
        messagebox.showinfo(title='Berhasil Kirim Email', message=f'Email ke {entry_email} telah berhasil, silahkan cek email Anda!')
        jendela_email.destroy()
    else:
        messagebox.showerror(title='Kirim Email Gagal', message=f'Kirim Email ke {entry_email} Gagal!')


def konfirmasi_email():
    konfirmasi = messagebox.askyesno(title= 'Konfirmasi Email',
                                     message=f'Pengiriman akan dilakukan ke email berikut : {entry_email.get()}\n')
    if konfirmasi:
        # tiga data input yang digunakan untuk isi parameter dibawah, semuanya adalah variabel global
        kirim_email(harga_asli_usd= harga_prediksi_usd,
                    data_input_prediksi= data_input,
                    # karena entry_email adalah global variabel, maka attribute yang melekat bisa dipanggil di tempat lain tanpa harus terhubung langsung
                    entry_email= entry_email.get())


def masukan_email():
    global jendela_email
    jendela_email = tkinter.Tk()
    jendela_email.title('Input Email')
    frame_email = tkinter.Frame(jendela_email, bg= THEME_COLOR)
    frame_email.pack()

    label_judul = tkinter.Label(frame_email, text='Masukan Email Tujuan Pengiriman', font=('Courier', 12))
    label_judul.grid(row=0, column=0)
    label_judul.config(bg=THEME_COLOR, fg='white', pady=15, padx=15)

    # gunakan global variabel pada entry email agar nilai email dapat diambil di tempat lain
    # karena pada fungsi ini tidak mengembalikan nilai dan tidak memasukkan nilai dari (button_kirim)
    global entry_email
    entry_email = tkinter.Entry(frame_email, width=40)
    entry_email.grid(row=1, column=0)

    button_kirim = tkinter.Button(frame_email, text= 'Kirim Email', command= konfirmasi_email)
    button_kirim.grid(row=2, column=0, pady= 15)



def buat_prediksi(data_prediksi):
    model = Prediksi(FILE_MODEL)

    return int(model.prediksi(data_prediksi))


def prediksi(data_input):
    global harga_prediksi_usd
    harga_prediksi_usd = buat_prediksi(data_input)
    kirim_email = messagebox.askyesno(title='Kirim Email', message= f'Hasil prediksi berdasarkan data yang ada inputkan menghasilkan nilai hasi prediksi harga berlian : ${harga_prediksi_usd}\n\n'
                                                                    f'Apakah Anda ingin kirim detail hasil prediksi ke email Anda?')
    if kirim_email:
        masukan_email()
    else:
        messagebox.showinfo(title="Tidak Kirim Email", message="Baik, Anda tidak mengirim email, terima kasih")


def error_numerik_value(var, batasBawah, batasAtas):
    messagebox.showerror(title= f'Error Input {var}',
                         message= f"Error input, Nilai yang dimasukan tidak masuk dalam range yang sudah ditentukan yaitu pada Variabel {var} : \n"
                                  f"{batasBawah} < X < {batasAtas}")

def check_input():
    # value dari dropdown
    potongan = entry_potongan.get()
    clarity = entry_clarity.get()
    warna = entry_warna.get()

    # check value pada dropdown
    if potongan not in values_potongan or clarity not in values_clarity or warna not in values_warna :
        messagebox.showerror('Value Dropdown Error!',
                             message='Pilih Value pada bagian Dropdown ( Warna, Potongan, dan Clarity ) hanya dari list yang sudah disediakan!')

    else:
        try:
            ## check sudah diisi semua atau belum dan diisi dengan numerik atau tidak
            # value isi sendiri ( numerikal )
            carat = float(entry_carat.get())
            depth = float(entry_depth.get())
            table = float(entry_table.get())
            volume = float(entry_volume.get())

        except ValueError:
            messagebox.showerror('Value Numerikal Input Error',
                                 message='Cek kembali Value pada ( Carat, Depth, Table, Volume ) Hanya dengan isian angka/numerik dan tidak boleh Kosong!')
        else:
            # cek nilai apakah sesuai dengan data train untuk kesesuaian hasil prediksi
            if carat > 2 or carat < 0:
                error_numerik_value('Carat', 0, 2)
            elif depth > 70 or depth < 50:
                error_numerik_value('Depth',53, 70 )
            elif table > 70 or table <  45:
                error_numerik_value('Table', 48, 68)
            elif volume > 325 or volume < 40:
                error_numerik_value('Volume', 40, 325)
            else:
                # konfirmasi input user
                pilihan = messagebox.askyesno(title='Konfirmasi Data Prediksi',
                                           message=f'Yakin ingin prediksi dengan data berikut? \n'
                                                   f'Carat  : {carat} \n'
                                                   f'Depth  : {depth} \n'
                                                   f'Table  : {table} \n'
                                                   f'Volume : {volume} \n'
                                                   f'Pilihan Clarity  : {clarity} \n'
                                                   f'Pilihan Warna    : {warna} \n'
                                                   f'Pilihan Potongan : {potongan}')
                if pilihan:
                    global data_input
                    data_input = [carat, potongan, warna, clarity, depth, table, volume]
                    prediksi(data_input)
                else:
                    messagebox.showinfo(title='Pengumuman!', message= 'Anda tidak jadi melakukan prediksi, terima kasih')


# fungsi UI untuk Tampilkan Info Variabel
def cari_info():
    infovar_ui = InfoVar_UI()











# ---------------------------------# USER INTERFACE #------------------------------------- #

window = tkinter.Tk()
window.title('Prediksi Harga Berlian')
window.config(bg= THEME_COLOR, pady= 30, padx=30)

# CANVAS
kanvas = tkinter.Canvas(width= 200, height=200, highlightthickness=0, bg=THEME_COLOR )
gambar = Image.open('diamond.png')
gambar_resize = gambar.resize((300,300), Image.ANTIALIAS)
gambar_tk = ImageTk.PhotoImage(gambar_resize)
kanvas.create_image(100, 100, image = gambar_tk)
kanvas.grid(row=1, column=0, columnspan=2)



# label

label_judul = tkinter.Label(text= 'Prediksi Berlian Anda!',  font = ('Courier', 24))
label_judul.grid(row=0, column=0, columnspan=2)
label_judul.config(bg= THEME_COLOR, fg= 'white')

label_carat = tkinter.Label(text= 'Besaran Carat : ', font = ('Courier', 12))
label_carat.grid(row= 2, column= 0)
label_carat.config(bg= THEME_COLOR, fg= 'white', pady= 10)

label_warna = tkinter.Label(text= 'Pilihan Warna : ', font = ('Courier', 12))
label_warna.grid(row= 3, column= 0)
label_warna.config(bg= THEME_COLOR, fg= 'white', pady= 10)

label_potongan = tkinter.Label(text= 'Jenis Potongan : ', font = ('Courier', 12))
label_potongan.grid(row= 4, column= 0)
label_potongan.config(bg= THEME_COLOR, fg= 'white', pady= 10)

label_clarity = tkinter.Label(text= 'Jenis Clarity : ', font = ('Courier', 12))
label_clarity.grid(row= 5, column= 0)
label_clarity.config(bg= THEME_COLOR, fg= 'white', pady= 10)

label_depth = tkinter.Label(text= 'Besaran Depth : ', font = ('Courier', 12))
label_depth.grid(row= 6, column= 0)
label_depth.config(bg= THEME_COLOR, fg= 'white', pady= 10)

label_table = tkinter.Label(text= 'Besaran Table : ', font = ('Courier', 12))
label_table.grid(row= 7, column= 0)
label_table.config(bg= THEME_COLOR, fg= 'white', pady= 10)


label_volume = tkinter.Label(text= 'Perkiraan Volume : ', font = ('Courier', 12))
label_volume.grid(row= 8, column= 0)
label_volume.config(bg= THEME_COLOR, fg= 'white', pady= 10)



# ENTRY

entry_carat = tkinter.Entry(width=43)
entry_carat.grid(row=2, column=1, pady= 10)

values_warna = ['E', 'I', 'J', 'H', 'F', 'G', 'D']
entry_warna = ttk.Combobox(values= values_warna, width= 40)
entry_warna.set("Pilih Warna")
entry_warna.grid(row=3, column=1, pady= 10)

values_potongan = ['Ideal', 'Premium', 'Good', 'Very Good', 'Fair']
entry_potongan = ttk.Combobox(values= values_potongan, width= 40)
entry_potongan.set("Pilih Jenis Potongan")
entry_potongan.grid(row=4, column=1, pady= 10)

values_clarity = ['SI2', 'SI1', 'VS1', 'VS2', 'VVS2', 'VVS1', 'I1', 'IF']
entry_clarity = ttk.Combobox(values= values_clarity, width= 40)
entry_clarity.set("Pilih Clarity")
entry_clarity.grid(row=5, column=1, pady= 10)

entry_depth = tkinter.Entry(width=43)
entry_depth.grid(row=6, column=1, pady= 10)

entry_table = tkinter.Entry(width=43)
entry_table.grid(row=7, column=1, pady= 10)

entry_volume = tkinter.Entry(width=43)
entry_volume.grid(row=8, column=1, pady= 10)
# BUTTON

button_prediksi = tkinter.Button(text= 'Cari Prediksi', command= check_input)
button_prediksi.grid(row=9, column=0, pady= 10)

button_info = tkinter.Button(text= 'Info Variabel', command= cari_info)
button_info.grid(row=9, column=1,  pady= 10)


window.mainloop()












