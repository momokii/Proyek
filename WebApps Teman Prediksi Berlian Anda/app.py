from flask import Flask, render_template, url_for, request

# modul sendiri
import requests
import prediksi

from kirimEmail import KirimEmail

# ---------------- KONSTANTA -----------------
VALUES_WARNA = ['E', 'I', 'J', 'H', 'F', 'G', 'D']
VALUES_POTONGAN = ['Ideal', 'Premium', 'Good', 'Very Good', 'Fair']
VALUES_CLARITY = ['SI2', 'SI1', 'VS1', 'VS2', 'VVS2', 'VVS1', 'I1', 'IF']
FILE_MODEL = 'model'

karat = None
table = None
depth = None
volumne = None
potongan = None
warna = None
clarity = None
email = None
hasil_prediksi = None

# ---------------- CLASS -----------------

app = Flask(__name__)
app.secret_key = 'berkah'

@app.route('/', methods = ['POST', 'GET'])
def landingpage():
    try:
        email_pesan = kirimDetail()
    except:
        email_pesan = None
    return render_template('landingpage/index.html', email = email_pesan, email_user = email)

@app.route('/form')
def form():
    return render_template('form/form.html')

@app.route('/infovar')
def infovar():
    url = "https://api.npoint.io/a0d3609ca8c11159ef73"
    data = requests.get(url).json()
    data = enumerate(data)
    return render_template('infovar/infovar.html', data_var = data)


def kirimFeedback():
    nama = request.form['name']
    email_pengirim = request.form['email']
    pesan = request.form['message']
    data_email = [email_pengirim, nama, pesan]
    kirim_email = KirimEmail(data_email)
    if kirim_email.kirim_email_mailjet(data_email[0]):
        return True
    else:
        return False

@app.route('/contact', methods = ['POST', 'GET'])
def contact():
    try:
        kirim_pesan = kirimFeedback()
    except:
        kirim_pesan = None
    return render_template('landingpage/contact.html', pesan = kirim_pesan)




@app.route('/prediksi', methods = ['POST', 'GET'])
def prediksiform():
    global karat, table, depth, volume, potongan, warna, clarity, hasil_prediksi
    karat = float(request.form['karat'])
    table = float(request.form['table'])
    depth = float(request.form['depth'])
    volume = float(request.form['volume'])
    potongan = request.form['potongan']
    warna = request.form['warna']
    clarity = request.form['clarity']
    data_prediksi = [karat, potongan, warna, clarity, depth, table, volume]

    # import model
    model = prediksi.Prediksi(FILE_MODEL)
    hasil_prediksi = int(model.prediksi(data_prediksi))

    return render_template('form/hasil_prediksi.html', data_prediksi = data_prediksi, hasil = hasil_prediksi)

# kirim detail info input user dan hasil prediksi ke email yang user inputkan
def kirimDetail():
    global email
    data_prediksi = [karat, potongan, warna, clarity, depth, table, volume]

    email = request.form['emailPrediksi']
    kirim_email = KirimEmail(harga_asli_usd= hasil_prediksi, data_input_prediksi= data_prediksi)
    if kirim_email.kirim_email_detailPrediksi(email):
        return True
    else:
        return False


@app.route('/ourteam')
def meetteam():
    return render_template('landingpage/about.html')

@app.route('/infomodel')
def infomodel():
    return render_template('infomodel/index.html')




if __name__ == '__main__':
    app.run(debug= True)