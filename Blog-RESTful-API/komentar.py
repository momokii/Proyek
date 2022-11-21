import datetime

from src import *
from models import *

komentar = Blueprint('komentar', __name__,
                     url_prefix= '/api/komentar')


BASE_PATH_DOCS = './docs/komentar'


### ---------------- KOMENTAR -------------- ###

@komentar.get('/all')
@swag_from(f'{BASE_PATH_DOCS}/komentar_get_all.yaml')
def get_all_komen():

    all_komen = Komentar.query.order_by(Komentar.post_id).all()
    komen_dict = []
    for data in all_komen:
        komen = {
            'id_komentar' : data.id,
            'id_post' : data.post_id,
            'id_user' : data.user_id,
            'komentar' : data.body_komentar
        }
        komen_dict.append(komen)

    if komen_dict != []:
        json_return = jsonify(komen_dict), HTTP_200_OK
    else:
        json_return  = jsonify({}), HTTP_204_NO_CONTENT

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return



@komentar.get('/post/<int:id_post>')
@swag_from(f'{BASE_PATH_DOCS}/komentar_get_page.yaml')
def get_page_komen(id_post):
    all_komentar = Komentar.query.filter_by(post_id = id_post).all()

    get_post = Post.query.get(id_post)
    post = {
        'id_post' : get_post.id,
        'title' : get_post.title,
        'subtitle' : get_post.subtitle,
        'owner_id' : get_post.user_id,
        'owner_username' : get_post.user.username,
        'comment_count' : get_post.comment_count
    }

    komen_dict = []
    for data in all_komentar:
        komen = {
            'id_komentar': data.id,
            'id_post': data.post_id,
            'id_user': data.user_id,
            'komentar': data.body_komentar
        }
        komen_dict.append(komen)

    if komen_dict != []:
        json_return = jsonify({
            'post_info' : post,
            'data_komentar' : komen_dict
        }), HTTP_200_OK
    else:
        json_return = jsonify({}), HTTP_204_NO_CONTENT

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return






@komentar.post('/add')
@jwt_required()
@swag_from(f'{BASE_PATH_DOCS}/komentar_add.yaml')
def make_komen():
    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':
        data = request.get_json()
        try:
            body = data['komentar']
            user = User.query.get(current_user.id)
            post = Post.query.get(data['id_post'])

            komentar = Komentar(
                body_komentar = body,
                user = user,
                post = post,
                created_at = datetime.datetime.now()
            )
            db.session.add(komentar)
            post.comment_counter()
            user.komen_counter()
            db.session.commit()

            json_return = jsonify({
                'success' : {
                    'komentar' : komentar.body_komentar,
                    'id_user' : komentar.user_id,
                    'id_post' : komentar.post_id,
                    'id_komentar' : komentar.id
                }
            }), HTTP_201_CREATED

        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(check_req)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return





@komentar.delete('/delete')
@jwt_required()
@swag_from(f'{BASE_PATH_DOCS}/komentar_delete.yaml')
def delete_komentar():
    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':

        try:

            data = request.get_json()
            deleted_komentar = Komentar.query.get(data['id'])
            user_id_requested = current_user.id
            if deleted_komentar:
                if deleted_komentar.check_valid_access(user_id_requested):

                    body_komentar = deleted_komentar.body_komentar
                    komentar_owner = deleted_komentar.user_id
                    komentar_post_id = deleted_komentar.post_id

                    post_comment_deleted = Post.query.get(komentar_post_id)
                    user_owner = User.query.get(komentar_owner)

                    db.session.delete(deleted_komentar)
                    post_comment_deleted.comment_counter()
                    user_owner.komen_counter()

                    db.session.commit()
                    json_return = jsonify(
                        success = {
                            'komentar' : body_komentar,
                            'komentar_owner_id' : komentar_owner,
                            'post_id' : komentar_post_id,
                            'aksi' : 'hapus'
                        }
                    ), HTTP_200_OK

                else:
                    json_return = jsonify(
                        error = 'tidak punya akses'
                    ), HTTP_401_UNAUTHORIZED

            else:
                json_return = jsonify(
                    error = 'komentar tidak ditemukan'
                ), HTTP_404_NOT_FOUND

        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(check_req)

    json_return[0].headers.add_header('Allow-Access-Control-Origin', '')
    return json_return






















