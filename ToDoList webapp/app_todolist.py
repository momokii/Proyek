from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin, current_user

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash, check_password_hash

from functools import wraps

import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todolist.db"
app.config["SQLALCHEMY_TRACK_MODOIFICATIONS"] = False
db = SQLAlchemy(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app= app)

# ----------------------------------------------------------------------
# --------------------- LOGIN/ACCOUNT SETTING ---------------------------
# -----------------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return None
    return user

@login_manager.unauthorized_handler
def unathorized():
    flash("Belum Login!")
    return redirect(url_for('login'))

# decorator admin only
def check_user_status(f):
    @wraps(f)
    def decorated_function(taskfilter ,*args, **kwargs):
        if current_user.id != taskfilter.user_id:
            flash("Anda tak punya akses ke tempat orang lain, blok!")
            return redirect(url_for('list_data'))
        return f(*args, **kwargs)
    return decorated_function



# ----------------------------------------------------------------------
# -------------------------- DB SETTING --------------------------------
# ----------------------------------------------------------------------

class UserFormRegister(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Konfirmasi Password", validators=[DataRequired()])
    submit = SubmitField("Daftar Akun")

class UserFormLogin(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(200), unique = True ,nullable = False)
    # relationship
    todolist = relationship('Todolist', back_populates = 'user')
    history_todolist = relationship('History_todolist', back_populates = 'user')

class Todolist(db.Model):
    __tablename__ = "todolist"
    id = db.Column(db.Integer(), primary_key = True)
    task = db.Column(db.String(500), nullable = False)
    tanggal_input = db.Column(db.String(20), nullable = False)
    tanggal_deadline = db.Column(db.String(20), nullable = False)
    status = db.Column(db.String(15), nullable = False)
    # relationship
    user_id = db.Column(db.Integer(), ForeignKey('user.id'), nullable = False)
    user = relationship('User', back_populates = "todolist")

class History_todolist(db.Model):
    __tablename__ = "history_todolist"
    id = db.Column(db.Integer(), primary_key=True)
    task = db.Column(db.String(500), nullable=False)
    tanggal_deadline = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(15), nullable=False)
    # relationship
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable = False)
    user = relationship('User', back_populates = 'history_todolist')

#db.create_all()

# ----------------------------------------------------------------------
# ----------------------------- APP ------------------------------------
# ----------------------------------------------------------------------


# ------- LOGIN AND STUFF ----------
@app.route('/', methods = ["POST", "GET"])
def login():
    form = UserFormLogin()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username = username).first()
        print(user.username)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('main'))
            else:
                flash("username/password salah")
        else:
            flash("username tak ada")
    return render_template('login.html', form = form)


@app.route('/register', methods = ["POST", "GET"])
def register():
    form = UserFormRegister()
    if form.validate_on_submit():
        try:
            password = form.password.data
            if password == form.password_confirm.data:
                new_user = User(
                    username = form.username.data,
                    password = generate_password_hash(password, salt_length=8),
                    email = form.email.data
                )
                db.session.add(new_user)
                db.session.commit()
                flash("Berhasil tambah akun, silahkan login")
                return redirect(url_for('login'))
            else:
                flash('Password konfirmasi tidak sesuai')
        except:
            flash("Username/ Email sudah ada!")

    return render_template('register.html', form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




# ------- MAIN ----------
@app.route("/main", methods = ["POST", "GET"])
@login_required
def main():
    day = datetime.datetime.today().strftime("%A")
    date = str(datetime.datetime.today().date())
    # query semua task namun filter tentu dengan id user-nya
    task = Todolist.query.filter_by(user_id = current_user.id).all()
    all_tanggal = Todolist.query.filter_by(user_id = current_user.id).with_entities(Todolist.tanggal_deadline).distinct()

    ada_kadaluarsa = False
    for data in task:
        if str(data.tanggal_deadline) < str(datetime.datetime.today().date()):
            if data.status != "Finished":
                data.status = 'Not Finished'
            new_history = History_todolist(
                task = data.task,
                tanggal_deadline = data.tanggal_deadline,
                status = data.status,
                user = current_user
            )
            db.session.add(new_history)
            db.session.delete(data)
            ada_kadaluarsa = True
    db.session.commit()
    if ada_kadaluarsa:
        return redirect(url_for('main'))

    if request.method == "POST":
        tanggal = request.form['deadline']
        if tanggal == "all":
            return redirect(url_for('main'))
        else:
            return redirect(url_for('main_filter', filter = tanggal))

    return render_template('main.html', day = day, date = date, task = task, all_tanggal = all_tanggal)


@app.route('/main_filter')
@login_required
def main_filter():
    filter = request.args.get('filter')
    if filter == "all" or filter == "":
        return redirect(url_for('main'))
    day = datetime.datetime.today().strftime("%A")
    date = str(datetime.datetime.today().date())

    # hanya query yang sesuai dengan id yang sedang login
    all_tanggal = Todolist.query.filter_by(user_id = current_user.id).with_entities(Todolist.tanggal_deadline).distinct()
    taskfilter = Todolist.query.filter_by(user_id = current_user.id).filter_by(tanggal_deadline = filter).all()

    return render_template('main_filter.html', taskfilter = taskfilter, all_tanggal = all_tanggal, day = day, date = date)



@app.route('/tambah_task', methods = ["POST", "GET"])
@login_required
def tambah_task():
    if request.method == "POST":

        tanggal_deadline = request.form['date']
        if str(tanggal_deadline) < str(datetime.datetime.today().date()):
            flash("GAGAL INPUT TASK!, Tanggal deadline kurang dari hari ini, tidak masuk akal!")
            return redirect(url_for('main'))

        new_task = Todolist(
            task = request.form['task'],
            tanggal_input = str(datetime.datetime.today().date()),
            tanggal_deadline = tanggal_deadline,
            status = 'On Progress',
            user = current_user
        )
        db.session.add(new_task)
        db.session.commit()

    return redirect(url_for('main_filter', filter = tanggal_deadline))


@app.route('/finished', methods = ["POST", "GET"])
@login_required
def finished_task():
    try:
        finish_task = Todolist.query.get(request.form['id'])
    except:
        finish_task = Todolist.query.get(request.args.get('id'))
    else:
        filter = request.form['filter']
        if filter != "":
            return redirect(url_for('main_filter', filter = filter))
    finally:
        finish_task.status = 'Finished'
        db.session.commit()
    return redirect(url_for('main'))


@app.route('/unfinished', methods = ["POST", "GET"])
@login_required
def unfinished_task():
    try:
        unfinish_task = Todolist.query.get(request.form['id'])
    except:
        unfinish_task = Todolist.query.get(request.args.get('id'))
    else:
        filter = request.form['filter']
        if filter != "":
            return redirect(url_for('main_filter', filter = filter))
    finally:
        unfinish_task.status = 'On Progress'
        db.session.commit()
    return redirect(url_for('main'))


@app.route('/delete', methods = ["POST", "GET"])
@login_required
def delete_task():
    try:
        task_deleted = Todolist.query.get(request.form['id'])
    except:
        task_deleted = Todolist.query.get(request.args.get('id'))
    else:
        filter = request.form['filter']
        if filter != "":
            return redirect(url_for('main_filter', filter = filter))
    finally:
        db.session.delete(task_deleted)
        db.session.commit()
    return redirect(url_for('main'))


# ------- HISTORY ----------
@app.route('/history', methods = ["POST", "GET"])
@login_required
def history():
    day = str(datetime.datetime.today().strftime("%A"))

    # sama dengan history, hanya query sesuai dengan id user yang login
    all_history = History_todolist.query.filter_by(user_id = current_user.id).all()
    all_tanggal = History_todolist.query.filter_by(user_id = current_user.id).with_entities(History_todolist.tanggal_deadline).distinct()

    if request.method == "POST":
        tanggal = request.form['deadline']
        if tanggal == "all":
            return redirect(url_for('history'))
        else:
            return redirect(url_for('history_filter', filter = tanggal))

    return render_template('history.html', history = all_history, all_tanggal = all_tanggal, day = day)

@app.route('/history_filter')
@login_required
def history_filter():
    tanggal = request.args.get('filter')
    if tanggal == "all":
        return redirect(url_for('history'))

    all_tanggal = History_todolist.query.filter_by(user_id = current_user.id).with_entities(History_todolist.tanggal_deadline).distinct()

    day = str(datetime.datetime.today().strftime("%A"))

    history_selected = History_todolist.query.filter_by(tanggal_deadline=tanggal).filter_by(user_id = current_user.id).all()

    return render_template('history_filter.html', history = history_selected, all_tanggal = all_tanggal, day = day)


@app.route('/delete_history', methods = ["POST", "GET"])
@login_required
def delete_history():
    try:
        history_deleted = History_todolist.query.get(request.form['id'])
    except:
        history_deleted = History_todolist.query.get(request.args.get('id'))
    else:
        filter = request.form['filter']
        if filter != '':
            return redirect(url_for('history_filter', filter=filter))
    finally:
        db.session.delete(history_deleted)
        db.session.commit()

    return redirect(url_for('history'))



if __name__ == "__main__":
    app.run(debug= True)