import datetime
from kirimEmail import KirimEmail

from flask import Flask, request, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY'

Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "YOUR_DATABASE"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


# ----------------------------------- LOGIN MANAGER----------------------------------- #
'''
Mudahnya login manager akan melakukan trigger ketika misalnya dua fungsi di bawah ini akan tertrigger ketika fungsi route diberikan misal decorator 

login_required

jadi dari hasil decorator tersebut nantinya dengan kondisi tertentu akan mentrigger fungsi yang menggunakan login_manager di bawah ini

'''
# load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# check user login tidak
# tertrigger ketika login_required -> False
@login_manager.unauthorized_handler
def unauthorized():
    flash('Anda Belum Login! silahkan login dahulu!')
    return redirect(url_for('login'))





# ====================================================================================== #
# ----------------------------------- TABLE/DATABASE ----------------------------------- #
# ====================================================================================== #

## --------------- USER -------------- ##
class User(UserMixin, db.Model):
    username = db.Column(db.String(100), primary_key = True)
    password = db.Column(db.String(150))
    '''
    -- Tambahan -- 
    Jika kita tidak menggunakan "id" sebagai primary key, maka dalam proses login_user pakai flask_login.login_user ada perlu di ubah seperti di bawah ini persis
    '''
    def get_id(self):
        return (self.username)






## --------------- KATEGORI -------------- ##
class Kategori(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nama_kategori = db.Column(db.String(100), nullable = False, unique = True)

class CreateKategori(FlaskForm):
    nama_kategori = StringField("Nama Kategori", validators=[DataRequired()])
    submit = SubmitField("Tambah Kategori")





## --------------- MEMBER -------------- ##
class Member(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nama_member = db.Column(db.String(100), nullable = False)
    nomor = db.Column(db.String(25), unique = True)
    email = db.Column(db.String(100), unique = True)

class CreateMember(FlaskForm):
    nama_member = StringField("Nama Member", validators=[DataRequired()])
    nomor = StringField("Nomor Telepon", validators=[DataRequired(), Length(min=9)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Tambah Member")





## --------------- MAKANAN-------------- ##
class Makanan(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nama_makanan = db.Column(db.String(100), nullable = False, unique = True)
    kategori = db.Column(db.String(100), nullable = False)
    harga = db.Column(db.Integer, nullable = False)
    diskon = db.Column(db.Integer, nullable = False)

class CreateMakanan(FlaskForm):
    all_kategori = Kategori.query.all()
    choice = [(kategori.nama_kategori, kategori.nama_kategori) for kategori in all_kategori]
    nama_makanan = StringField("Nama Makanan", validators=[DataRequired()])
    kategori = SelectField("Pilih Kategori", choices= choice )
    harga = IntegerField("Harga", validators=[DataRequired(), NumberRange(min = 0)])
    diskon = IntegerField("Diskon", validators=[NumberRange(min=0,max=100)])
    submit = SubmitField('Submit')





## --------------- TEMP CARTS ------------- ##
class Carts(db.Model):
    id_pesanan = db.Column(db.Integer, primary_key = True)
    id_makanan = db.Column(db.Integer, nullable = False)
    nama_makanan = db.Column(db.String(100), nullable = False)
    diskon = db.Column(db.Integer, nullable = False)
    harga = db.Column(db.Integer, nullable = False)
    jumlah = db.Column(db.Integer, nullable = False)
    harga_diskon = db.Column(db.Integer, nullable = False)
    harga_total = db.Column(db.Integer, nullable = False)





## --------------- HISTORY SALES ------------- ##
class HistorySales(db.Model):
    id_histori = db.Column(db.Integer, primary_key = True)
    list_order = db.Column(db.String(2000), nullable = False)
    total_jenisBarang = db.Column(db.Integer, nullable = False)
    total_order = db.Column(db.Integer, nullable = False)
    total_harga = db.Column(db.Integer, nullable = False)
    total_diskon = db.Column(db.Integer, nullable = False)
    harga_akhir = db.Column(db.Integer, nullable = False)
    total_bayar = db.Column(db.Integer, nullable = False)
    kembalian = db.Column(db.Integer, nullable = False)
    tanggal_order = db.Column(db.String(30), nullable = False)
    waktu_order = db.Column(db.String(50), nullable = False)
    member = db.Column(db.String(500))




#db.create_all()






# ======================================================================================= #
# ------------------------------------- APP/ROUTING ------------------------------------- #
# ======================================================================================= #

## --------------- TAMPILAN AWAL LOGIN -------------- ##

@app.route('/', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['uname']
        user = User.query.get(username)
        if user:
            if check_password_hash(user.password, request.form['pwd']):
                login_user(user)
                return redirect(url_for('carts'))
            else:
                flash('Password di masukan salah! silahkan coba lagi')
                return redirect(url_for('login'))
        else:
            flash('Username Salah!')
            return redirect(url_for('login'))
    return render_template('html/login.html')


@app.route('/register', methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form['uname']
        pwd = request.form['pwd']
        confirmpwd = request.form['confirmpwd']
        if not User.query.get(username):
            if pwd == confirmpwd:
                password_hash = generate_password_hash(password= pwd, salt_length=8)
                new_user = User(
                    username = username,
                    password = password_hash
                )
                db.session.add(new_user)
                db.session.commit()
                make_account = True
                flash(f'Berhasil Buat Akun {username}')
                return render_template('html/register.html', make_account = make_account)
            else:
                flash("Password Konfirmasi tidak sesuai!")
                return redirect(url_for('register'))
        else:
            flash("Username sudah Ada! Coba yang lain.")
            return redirect(url_for('register'))

    return render_template('html/register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))





## --------------- USER TABLE -------------- ##
@app.route('/user_table')
@login_required
def user_table():
    users = User.query.all()
    return render_template('html/user_table.html', users = users)

@app.route('/delete_user')
@login_required
def delete_user():
    user_deleted = User.query.get(request.args.get('username'))
    db.session.delete(user_deleted)
    db.session.commit()
    flash(f"Akun ({user_deleted.username}) Berhasil dihapus!")
    return redirect(url_for('user_table'))





## --------------- KATEGORI -------------- ##

@app.route('/kategori', methods = ["POST", "GET"])
@login_required
def kategori():
    all_kategori = Kategori.query.all()
    form = CreateKategori()

    if form.validate_on_submit():
        try:
            add_kategori = Kategori(
                nama_kategori = form.nama_kategori.data
            )
            db.session.add(add_kategori)
            db.session.commit()
            flash(f"Berhasil Tambah Kategori Baru : {form.nama_kategori.data}")
            return redirect(url_for('kategori'))
        except:
            flash(f"Maaf Input data ({form.nama_kategori.data}) GAGAL, sepertinya kategori yang sama sudah ada, silahkan coba lagi!")
            return redirect(url_for('kategori'))

    return render_template('html/kategori.html', form = form, kategori = all_kategori)

@app.route('/delete_kategori')
@login_required
def delete_kategori():
    kategori_deleted = Kategori.query.get(request.args.get('id'))
    info_kategori = f"ID : {kategori_deleted.id} | {kategori_deleted.nama_kategori} "
    db.session.delete(kategori_deleted)
    db.session.commit()
    flash(f"Berhasil Hapus Kategori : {info_kategori}")
    return redirect(url_for('kategori'))





## --------------- MEMBER -------------- ##

@app.route('/member', methods = ["POST", "GET"])
@login_required
def member():
    all_member = Member.query.all()
    form = CreateMember()

    if form.validate_on_submit():
        try:
            add_member = Member(
                nama_member = form.nama_member.data,
                nomor = form.nomor.data,
                email = form.email.data
            )
            db.session.add(add_member)
            db.session.commit()
            flash("Berhasil Menambahkan Member! : \n"
                  f"{form.nama_member.data} | {form.nomor.data} | {form.email.data}")
            return redirect(url_for('member'))
        except:
            flash(f"Menambahkan Member ({form.nama_member.data}) GAGAL!, Kemungkinan Nomor/Email sudah ada dalam data lainnya, silahkan coba lagi.")
            return redirect(url_for('member'))

    # cek ini tambah member ( fungsi dari Carts ) atau bukan
    member = request.args.get('member')

    return render_template('html/member.html', form = form, member = all_member, tambahMember = member)

@app.route('/edit_member', methods = ['POST', 'GET'])
@login_required
def edit_member():
    if request.method == "POST":
        try:
            edited_member = Member.query.get(request.form['id'])
            edited_member.nama_member = request.form['nama_member']
            edited_member.email = request.form['email']
            edited_member.nomor = request.form['nomor']
            db.session.commit()
            flash(f"Berhasil Edit Info Member dengan ID : {request.form['id']} | {request.form['nama_member']}")
            return redirect(url_for('member'))
        except:
            flash(f"Edit Info Member ({request.form['id']} | {request.form['nama_member']}) GAGAL!, Kemungkinan email/nomor sudah ada pada data lainnya, silahkan coba lagi")
            return redirect(url_for('member'))
    return redirect(url_for('member'))


@app.route('/delete_member', methods = ["POST", "GET"])
@login_required
def delete_member():
    deleted_member = Member.query.get(request.args.get('id'))
    info_member = f"ID : {deleted_member.id} | {deleted_member.nama_member} | {deleted_member.nomor} | {deleted_member.email}"
    db.session.delete(deleted_member)
    db.session.commit()
    flash(f"Berhasil Hapus Member : {info_member}")
    return redirect(url_for('member'))





## --------------- MAKANAN -------------- ##

@app.route('/makanan', methods = ["POST", "GET"])
@login_required
def makanan():
    form = CreateMakanan()
    all_makanan = Makanan.query.all()
    all_kategori = Kategori.query.all()

    if form.validate_on_submit():
        try:
            add_makanan = Makanan(
                nama_makanan = form.nama_makanan.data,
                kategori = form.kategori.data,
                diskon = form.diskon.data,
                harga = form.harga.data
            )
            db.session.add(add_makanan)
            db.session.commit()
            flash(f"Berhasil Menambahkan Makanan : \n"
                  f"{form.nama_makanan.data} | {form.kategori.data} | {form.harga.data} | {form.diskon.data}" )
            return redirect(url_for('makanan'))
        except:
            flash(f"GAGAL! Nama makanan ({form.nama_makanan.data}) sudah ada pada database, silahkan coba lagi!")
            return redirect(url_for('makanan'))

    return render_template('html/makanan.html', form = form, makanan = all_makanan, kategori = all_kategori)


@app.route('/edit_makanan', methods = ["POST", "GET"])
@login_required
def edit_makanan():

    if request.method == "POST":
        edited_makanan = Makanan.query.get(request.form['id'])
        nama_makanan_lama = edited_makanan.nama_makanan
        try:
            edited_makanan.nama_makanan = request.form['nama_makanan']
            edited_makanan.kategori = request.form['kategori']
            edited_makanan.diskon = request.form['diskon']
            db.session.commit()
            flash(f"Berhasil Edit Info Makanan dengan ID Makanan : {request.form['id']}")
            return redirect(url_for('makanan'))
        except:
            flash(f"Edit nama ({nama_makanan_lama}) menjadi ({request.form['nama_makanan']}) GAGAL! Mungkin nama makanan ({nama_makanan_lama}) sudah ada pada data yang ada, silahkan coba lagi")
            return redirect(url_for('makanan'))

    return redirect(url_for('makanan'))


@app.route('/delete_makanan')
def delete_makanan():
    makanan_deleted = Makanan.query.get(request.args.get('id'))
    info_makanan = f"ID : {makanan_deleted.id} | {makanan_deleted.nama_makanan} | {makanan_deleted.kategori}"
    db.session.delete(makanan_deleted)
    db.session.commit()
    flash(f"Berhasil hapus makanan : {info_makanan}")
    return redirect(url_for('makanan'))





## --------------- CARTS -------------- ##

@app.route('/carts', methods = ['POST', 'GET'])
@login_required
def carts():
    all_makanan = Makanan.query.all()
    carts = Carts.query.all()

    if request.method == "POST":
        # karena carts bersifat temp maka setiap tambahkan cart baru hapus data pada carts yang ada sebelumnya sebelum nantinya tambah yang baru
        db.session.query(Carts).delete()  # ketika menambahkan carts baru, maka pastikan carts sebelumnya akan dihapus dahulu
        try:

            for makanan in all_makanan:
                jumlah_makanan = int(request.form[f'jumlah{makanan.id}'])

                # carts hanya menambahkan dari daftar pilih makanan yang punya jumlah order > 0
                if jumlah_makanan > 0:
                    harga_diskon = int(makanan.harga) - (int(makanan.harga) * (int(makanan.diskon) / 100))
                    harga_total = harga_diskon * int(jumlah_makanan)

                    tambah_carts = Carts(
                        id_makanan = makanan.id,
                        nama_makanan = makanan.nama_makanan,
                        harga = makanan.harga,
                        diskon = makanan.diskon,
                        jumlah = jumlah_makanan,
                        harga_diskon = harga_diskon,
                        harga_total = harga_total
                    )

                    # setelah dihapus di awal, tambah baru carts untuk data input terbaru
                    db.session.add(tambah_carts)


            flash('Makanan Berhasil ditambahkan ke Carts!')

        except:
            db.session.query(Carts).delete()
            flash('GAGAL tambahkan Carts, TAMBAHAN --> ketika tambahkan Carts, Pastikan tabel Pilih Makanan TIDAK FOKUS pada SATU/BEBERAPA jenis makanan, HARUS dalam posisi AWAL/SEMUA ITEM TAMPAK/TAMPIL pada tabel')


        db.session.commit()
        return redirect(url_for('carts'))

    # Berdasarkan data yang diquery dari Carts, lakukan perhitungan untuk melihat summary dan hasil akhir dari belanjaan user
    # DATA SUMMARY CARTS -> berdasarkan data dari Carts
    total_jenis_barang = len(carts)
    total_jumlah_barang = 0
    total_harga = 0
    total_harga_diskon = 0
    for makanan in carts:
        total_jumlah_barang = total_jumlah_barang + int(makanan.jumlah)
        total_harga = total_harga + (int(makanan.harga) * int(makanan.jumlah))
        total_harga_diskon = total_harga_diskon + int(makanan.harga_total)
    total_diskon = total_harga - total_harga_diskon
    data_summary = [total_jenis_barang, total_jumlah_barang, total_harga, total_diskon, total_harga_diskon]


    # CEK PAKAI MEMBER ATAU TIDAK -> mempengaruhi tampilan pada summary order
    if request.args.get('member'):
        member = Member.query.get(request.args.get('member'))
    else:
        member = False


    return render_template('html/carts.html', all_makanan = all_makanan, carts = carts, summary = data_summary, member = member)


@app.route('/edit_cartsItem', methods = ["POST" , "GET"])
@login_required
def edit_cartsItem():
    # Edit hanya bisa edit jumlah order
    if request.method == "POST":
        item_edited = Carts.query.get(request.form['id'])
        jumlah_awal = item_edited.jumlah
        item_edited.jumlah = int(request.form['jumlah'])
        db.session.commit()
        flash(f'Berhasil Edit Jumlah Item {item_edited.nama_makanan} dari ({jumlah_awal}) menjadi ({request.form["jumlah"]})')
        return redirect(url_for('carts'))

    return redirect(url_for('carts'))


@app.route('/cartsItem', methods = ['POST', "GET"])
@login_required
def delete_cartsItem():
    deleted_item = Carts.query.get(request.args.get('id'))
    info_delete = f"{deleted_item.nama_makanan} | jumlah : {deleted_item.jumlah}"
    db.session.delete(deleted_item)
    db.session.commit()
    flash(f"Berhasil Hapus Item dari Carts : {info_delete}")
    return redirect(url_for('carts'))


@app.route('/delete_allCarts')
@login_required
def delete_allCarts():
    db.session.query(Carts).delete()
    db.session.commit()
    flash("Berhasil hapus seluruh Carts")
    return redirect(url_for('carts'))


## --------------- KONFIRMASI PEMBAYARAN -------------- ##

@app.route('/konfirmasi_bayar', methods = ["POST", "GET"])
@login_required
def konfirmasi_bayar():

    if request.method == "POST":
        # ------------- ATUR PEMBAYARAN ------------- #
        # CEK APAKAH PAKAI MEMBER ATAU TIDAK
        if request.form['memberConfirm'] == "True":
            member = Member.query.get(request.form['member'])
            member_info = f"{member.id} | {member.nama_member} | {member.email} | {member.nomor}"
        else:
            member = False
            member_info = " "

        # HITUNG TOTAL HARGA TAGIHAN DAN TOTAL UANG DIBAYARKAN
        totalAKhir = request.form['jumlahHargaAkhir']
        jumlah_bayar = request.form['jumlah_bayar']

        # kondisi cek bayar sudah > tagihan belum
        if int(jumlah_bayar) < int(totalAKhir):
            flash("Pembayaran Gagal, jumlah bayar kurang dari jumlah tagihan, silahkan coba lagi!")
            return redirect(url_for('carts'))

        # INPUT DATA CARTS KE HISTORI SALES
        carts = Carts.query.all()
        # data berisi kumpulan semua barang dari carts
        list_order = ""
        for data in carts:
            try:
                order = f"( {data.nama_makanan} | {data.harga} | {data.diskon} | {data.jumlah} ) "
            except:
                order = " "
            list_order = list_order + order

        add_histori = HistorySales(
            list_order = list_order,
            total_jenisBarang = request.form['totalJenisBarang'],
            total_order = request.form['totalJumlahBarang'],
            total_harga = request.form['totalHarga'],
            total_diskon = request.form['totalDiskon'],
            harga_akhir = request.form['jumlahHargaAkhir'],
            total_bayar = request.form['jumlah_bayar'],
            kembalian = int(jumlah_bayar) - int(totalAKhir),
            tanggal_order = str(datetime.datetime.now().date()),
            waktu_order = str(datetime.datetime.now().time()).split('.')[0],
            member = member_info
        )

        # bersama dengan konfirmasi bayar juga menghapus carts karena sudah dikonfirmasi pesanan
        db.session.query(Carts).delete()
        db.session.add(add_histori)
        db.session.commit()

        # ------------- ATUR KIRIM DATA ------------- #

        latest_transaction = db.session.query(HistorySales).order_by(HistorySales.id_histori.desc()).first()

        # CEK BERDASAR MEMBER DI ATAS, JIKA PAKAI MEMBER, MAKA KIRIM EMAIL PADA EMAIL DARI MEMBER
        if member != False:
            # KIRIM EMAIL ke MEMBER
            kirim_email = KirimEmail(carts= carts, transaksi= latest_transaction, member= member)
            kirim_email.kirim_email_mailjet(user_address_tujuan=member.email)

        return render_template('html/selesai_pembayaran.html', transaksi = latest_transaction ,member=member, carts = carts)

    return redirect(url_for('carts'))





## --------------- HISTORY SALES -------------- ##

@app.route('/history_sales')
@login_required
def history_checkout():
    histori = HistorySales.query.all()
    return render_template('html/history_sales.html', histori = histori)


@app.route('/delete_history')
def delete_history():
    delete_history_data = HistorySales.query.get(request.args.get('id'))
    info_histori = f"ID : {delete_history_data.id_histori} | {delete_history_data.list_order} "
    db.session.delete(delete_history_data)
    db.session.commit()
    flash(f'Berhasil hapus History Sales : {info_histori}')
    return redirect(url_for('history_checkout'))




## --------------- RUN -------------- ##

if __name__ == "__main__":
    app.run(debug = True)
