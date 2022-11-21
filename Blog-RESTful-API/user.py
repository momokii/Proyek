import datetime
from src import *
from models import *
import validators


user = Blueprint('user', __name__,
                 url_prefix= '/api/user')

BASE_PATH_DOCS = "./docs/user"


## ----------- USER ---------------- ##


@user.get('/all')
@swag_from(f'{BASE_PATH_DOCS}/user_all.yaml')
def get_all_user():

    all_user = User.query.all()
    data = []
    for user in all_user:
        user_data = {
            'id' : user.id,
            'username' : user.username,
            'email' : user.email,
            'nama' : user.nama
        }
        data.append(user_data)

    if data != []:

        summary = {
            'user_count' : len(User.query.all()),
            'user_most_post_id' : User.query.order_by(User.post_count.desc()).first().id,
            'user_most_komen_id' : User.query.order_by(User.komen_count.desc()).first().id
        }

        json_return = jsonify({
            'data' : data,
            'summary' : summary
        }), HTTP_200_OK

    else:
        json_return = jsonify({}), HTTP_204_NO_CONTENT

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return





@user.post('/login')
@swag_from(f'{BASE_PATH_DOCS}/user_login.yaml')
def login():

    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':

        try:
            data = request.get_json()
            username = data['username']
            password = data['password']



            user = User.query.filter_by(username = username).first()
            if user:
                if user.check_password(password):

                    # jwt token
                    access_token = create_access_token(identity= user,
                                                       expires_delta= datetime.timedelta(seconds=600))

                    refresh_token = create_refresh_token(identity= user,
                                                         expires_delta= datetime.timedelta(
                                                             days= 7
                                                         ))


                    data = {
                        'username' : user.username,
                        'email' : user.email,
                        'nama' : user.nama,
                        'access_token' : access_token,
                        'refresh_token' : refresh_token
                    }
                    json_return = jsonify(success = data), HTTP_200_OK
                else:
                    json_return = jsonify(error = 'username/password salah'), HTTP_401_UNAUTHORIZED
            else:
                json_return = jsonify(error = 'username/password salah'), HTTP_401_UNAUTHORIZED

        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(check_req)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return



@user.get('/info')
@jwt_required()
@swag_from(f'{BASE_PATH_DOCS}/user_get_personal_info.yaml')
def cek_user():
    return jsonify({
        'username' : current_user.username,
        'email' : current_user.email,
        'nama' : current_user.nama,
        'password_hash' : current_user.password_hash,
        'id' : current_user.id,
        'post_count' : current_user.post_count,
        'komen_count' : current_user.komen_count
    }), HTTP_200_OK



@user.get('/refresh_token')
@jwt_required(refresh = True)
@swag_from(f'{BASE_PATH_DOCS}/user_get_refresh_token.yaml')
def get_refresh_token():
    id = get_jwt_identity()
    user = User.query.get(id)

    access_token = create_access_token(identity= user,
                                       expires_delta= datetime.timedelta(minutes=10))
    return jsonify({
        'access_token' : access_token
    }), HTTP_200_OK





@user.post('/add')
@swag_from(f'{BASE_PATH_DOCS}/user_add.yaml')
def add_user():
    request.access_control_request_headers
    req_check = request.headers.get('Content-Type')
    if req_check == 'application/json':

        try:
            data = request.get_json()
            username = data['username']
            password = data['password']
            email = data['email']
            nama = data['nama']


        except KeyError:
            json_return = wrong_parameter_input()


        else:
            if len(username) < 5:
                json_return = jsonify(error='username terlalu pendek, minimal 5 karakter'), HTTP_400_BAD_REQUEST

            elif len(password) < 8:
                json_return = jsonify(error='password terlalu pendek, minimal 8 karakter'), HTTP_400_BAD_REQUEST

            elif len(nama) < 5:
                json_return = jsonify(error='nama terlalu pendek, minimal 5 karakter'), HTTP_400_BAD_REQUEST

            elif not username.isalnum():
                json_return = jsonify(error='username salah bukan alpa numeric'), HTTP_400_BAD_REQUEST

            elif not validators.email(email):
                json_return = jsonify(error='format email tidak sesuai'), HTTP_400_BAD_REQUEST

            else:

                # 2nd try catch -> konfirmasi input data
                try:
                    user = User(
                        username = username,
                        password = password,
                        email = email,
                        nama = nama
                    )

                    db.session.add(user)
                    db.session.commit()
                    json_return = jsonify({
                        'success' : {
                            'id' : user.id,
                            'username' : username,
                            'email' : email,
                            'nama' : nama,
                            'aksi' : 'tambah akun'
                        }
                    }), HTTP_201_CREATED

                except IntegrityError:
                    json_return = jsonify({
                        'error': 'username / email sudah digunakan'
                    }), HTTP_409_CONFLICT


    else:
        json_return = non_json_input(req_check)


    json_return[0].headers.add_header('Access-Control-Allow-Origin', '*')
    print(json_return[0].headers)
    return json_return





@user.put('/edit_info')
@user.patch('/edit_info')
@jwt_required()
@swag_from(f'{BASE_PATH_DOCS}/user_edit.yaml')
def edit_user():

    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':

        try:
            data = request.get_json()
            id = current_user.id
            email = data['email']
            nama = data['nama']

        except KeyError:
            json_return = wrong_parameter_input()


        else:
            edited_user = User.query.get(id)
            if edited_user:

               if len(nama) < 5:
                   json_return = jsonify(error='nama terlalu pendek, minimal 5 karakter'), HTTP_400_BAD_REQUEST

               elif not validators.email(email):
                   json_return = jsonify(error='format email tidak sesuai'), HTTP_400_BAD_REQUEST

               else:
                   try:
                        edited_user.email = email
                        edited_user.nama = nama

                        db.session.commit()
                        json_return = jsonify({
                            'success' : {
                                'email_baru' : email,
                                'nama_baru' : nama
                            }
                        }), HTTP_200_OK

                   except IntegrityError:
                       json_return = jsonify(error = 'email diganti sudah digunakan pada akun lain'), HTTP_409_CONFLICT


            else:
                json_return = jsonify(error = 'user tidak ditemukan'), HTTP_404_NOT_FOUND

    else:
        json_return = non_json_input(check_req)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return





@user.put('/pass_change')
@user.patch('/pass_change')
@jwt_required()
@swag_from(f'{BASE_PATH_DOCS}/user_change_pass.yaml')
def change_password():
    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':

        data = request.get_json()
        try:
            pass_lama = data['pass_lama']
            pass_baru = data['pass_baru']
            id = current_user.id

        except KeyError:
            json_return = wrong_parameter_input()

        else:
            user = User.query.get(id)
            if user:

                if user.check_password(pass_lama):

                    if len(pass_baru) < 8:
                        json_return = jsonify(error='password terlalu pendek, minimal 8 karakter'), HTTP_400_BAD_REQUEST

                    else:
                        user.password = pass_baru
                        db.session.commit()
                        json_return = jsonify({
                            'success': {
                                'username': user.username,
                                'aksi': 'ubah password'
                            }
                        }), HTTP_200_OK

                else:
                    json_return = jsonify(
                        error='password lama salah!'
                    ), HTTP_401_UNAUTHORIZED

            else:
                json_return = jsonify(
                    error='user tidak ada'
                ), HTTP_404_NOT_FOUND


    else:
        json_return = non_json_input(check_req)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return






@user.delete('/delete')
@jwt_required()
@swag_from(f'{BASE_PATH_DOCS}/user_delete.yaml')
def delete_user():

    request.access_control_request_headers
    try:
        id  = current_user.id
        user_delete = User.query.get(id)
        if user_delete:

            all_komen_related = Komentar.query.filter_by(user_id = id).all()
            all_post_related = Post.query.filter_by(user_id = id).all()
            all_like_related = Like.query.filter_by(id_user = id).all()

            for like in all_like_related:
                like_deleted = like
                db.session.delete(like)
                if like_deleted.post.user_id != id:
                    post = Post.query.get(like_deleted.id_post)
                    post.like_counter()


            for komen in all_komen_related:
                komen_deleted = komen
                db.session.delete(komen)
                if komen_deleted.post.user_id != id:
                    post_related = Post.query.get(komen_deleted.post_id)
                    post_related.comment_counter()


            for post in all_post_related:
                post_deleted = post

                like_related = Like.query.filter_by(id_post = post_deleted.id).all()
                for like in like_related:
                    db.session.delete(like)

                komen_related = Komentar.query.filter_by(post_id = post_deleted.id).all()
                for komen in komen_related:
                    db.session.delete(komen)

                db.session.delete(post)

            all_user_updated = User.query.all()
            for user in all_user_updated:
                user.komen_counter()


            db.session.delete(user_delete)
            db.session.commit()

            json_return = jsonify({
                'success' : 'berhasil hapus user'
            }), HTTP_200_OK

        else:
            json_return = jsonify({
                'error' : 'user tidak ditemukan'
            }), HTTP_404_NOT_FOUND

    except KeyError:
        json_return = wrong_parameter_input()


    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return















