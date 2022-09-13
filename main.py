import berita
import data_saham
import kirim_pesan
import tkinter
from tkinter import messagebox

THEME_COLOR = "#375362"

# -------------------------- FUNGSI --------------------------

def cari_info_saham():
    saham_input = entry_saham.get().upper()
    perusahaan_input = entry_perusahaan.get()
    if saham_input == '':
        messagebox.showinfo('Field Kosong', 'Mari Tulis Code Saham dan Nama Perusahaannya yang ingin dicari')
    else:
        cari_saham = messagebox.askokcancel(f'Cari Saham', f'Ingin cari saham dengan kode {saham_input}?')
        if cari_saham:
            try:
                saham = data_saham.Saham(saham_input)
            except KeyError:
                messagebox.showinfo('Gagal!', 'Code Saham tidak ditemukan')
            else:
                messagebox.showinfo(f'Berhasil', f'Info Saham {saham_input} ditemukan!')
                info_saham = f"Sekilas Info Saham {saham_input} \n" \
                             f"Harga Saham Kemarin : ${saham.harga_akhir_kemarin} \n" \
                             f"Harga Saham Kemarin Lusa : ${saham.harga_akhir_kemarin_lusa} \n" \
                             f"Selisih Harga : ${saham.selisih_harga_akhir} \n" \
                             f"Persentase Perubahan : {saham.perc_selisih_harga_akhir}%"
                messagebox.showinfo(f'Info Saham {saham_input}', info_saham)
            finally:
                if perusahaan_input == '':
                    messagebox.showinfo(f"Nama Perusahaan Kosong", 'Nama perusaaan masih kosong, jika ingin mencari berita terkait perusahaan saham terkait, isi kolom terlebih dahulu dengan nama perusahaan dari saham yang dicari')
                else:
                    cari_berita = messagebox.askokcancel(f'Cari Berita', f'Ingin Mencari Berita terkait saham {saham_input} yaitu berita tentang perusahaan {perusahaan_input}? ')
                    if cari_berita:
                        berita_obj = berita.Berita(perusahaan_input, saham)
                        info_berita = berita_obj.format_berita()
                        try:
                            kirim_pesan.Kirim_Pesan(berita= info_berita)
                        except:
                            messagebox.showinfo("Terjadi Kesalahan", f"Mengirim pesan mengenai Saham {saham_input} dan perusahaan {perusahaan_input} Gagal!")
                        else:
                            messagebox.showinfo(f'Behasil', f'Info Saham {saham_input} dan Berita mengenai Perusahaan {perusahaan_input} Sudah Terkirim Ke Handphone Anda, Silahkan Cek Pesan pada Handphone Anda')




# -------------------------- UI --------------------------
# WINDOW
window = tkinter.Tk()
window.title('Mencari Info Saham')
window.config(bg= THEME_COLOR, pady= 30, padx= 50)

# LABEL

label_cariSaham = tkinter.Label(text= 'Cari Info Saham')
label_cariSaham.grid(row= 0, column=0, columnspan=2)
label_cariSaham.config(pady=20, bg= THEME_COLOR, fg = 'white', font = {'Arial', 150, 'bold'})

label_saham = tkinter.Label(text= 'Cari Saham')
label_saham.grid(row= 1, column=0)
label_saham.config(bg=THEME_COLOR, fg = 'white', font = {'Arial', 18, 'bold'})

label_perusahaan = tkinter.Label(text= 'Nama Perusahaan Saham yang dicari')
label_perusahaan.grid(row= 2, column=0)
label_perusahaan.config(bg= THEME_COLOR, fg = 'white', font = {'Arial', 18, 'bold'})

# ENTRY
entry_saham = tkinter.Entry(width=40)
entry_saham.grid(row=1, column=1)

entry_perusahaan = tkinter.Entry(width=40)
entry_perusahaan.grid(row=2, column=1)


# BUTTON
button_cari = tkinter.Button(text= 'Cari Info', command= cari_info_saham)
button_cari.grid(row=3, column=0,  pady= 20)
button_cari.config(font= {'Arial', 24, 'bold'}, fg= 'black', bg= 'green')

button_infoPenggunaan = tkinter.Button(text= 'Cara Pakai')
button_infoPenggunaan.grid(row= 3, column=1, pady=20)
button_infoPenggunaan.config(font= {'Arial', 24, 'bold'}, fg= 'black')

window.mainloop()

