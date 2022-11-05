from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
import datetime

# HEX COLOR
from rgb_hex import Rgb_hex
import pandas as pd

# Text to Speech
from tts import textToSpeech

app = Flask(__name__)
Bootstrap(app= app)


@app.route('/')
def main():
    hari = datetime.datetime.today().strftime("%A")
    return render_template('awal.html', hari = hari)

@app.route('/tts_speech', methods = ['POST', "GET"])
def tts():
    hasil = False
    hasil_path = ''
    text_input = ''

    if request.method == "POST":
        text_input = request.form['text']

        input = text_input.split()
        if len(text_input) > 1000:
            text_input = " ".join(input[:1000])

        hasil_path = textToSpeech.text_to_speech(text_input)
        hasil = True


    return render_template('tts.html', hasil = hasil, hasil_path = hasil_path,
                           input_file = text_input)


@app.route('/tts_pdf', methods = ['POST', "GET"])
def tts_pdf():
    hasil = False
    hasil_path = ''
    if request.method == "POST":

        pdf_input = request.files['pdf_file']
        file_path_save = 'static/input_user/input_pdf_user.pdf'
        pdf_input.save(file_path_save)

        hasil_path = textToSpeech.pdf_to_speech(filepath= file_path_save)
        hasil = True

    return render_template('tts_pdf.html', hasil = hasil, hasil_path = hasil_path)



@app.route('/hexcolor', methods = ["POST", "GET"])
def hexcolor():
    konversi = False
    filepath = ""
    hex_code = []

    if request.method == "POST":

        file_input = request.files['image']
        jumlah_tampil = int(request.form['jumlah_warna'])

        filepath = 'static/input_user/input_img_user.jpg'
        file_input.save(filepath)

        rgb_to_hex = Rgb_hex(img_path= filepath, jumlah_tampil= jumlah_tampil)
        list_hex = rgb_to_hex.img_to_hex()

        top_n_hex = pd.DataFrame(data = {'hex':list_hex}).value_counts().sort_values(ascending=False).reset_index()
        top_n_hex.columns = ['hex', "jumlah_total"]

        hex_code = top_n_hex.hex.values
        konversi  = True

    return render_template('hex.html', konversi = konversi, path_gambar = filepath, list_hex_code = hex_code)


if __name__ == "__main__":
    app.run(debug= True)