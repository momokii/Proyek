import requests.utils

from src import *
from models import *


post = Blueprint('post', __name__,
                 url_prefix= '/api/post')

BASE_PATH_DOCS = './docs/post'



### ----------------------- POST ----------------------- ###

@post.get('/all')
@swag_from(f'{BASE_PATH_DOCS}/post_get_all.yaml')
def get_all_post():

    all_post = Post.query.all()
    post_dict = []
    for post in all_post:
        data = post.post_info()
        post_dict.append(data)

    if post_dict != []:
        meta = {
            'post_count': len(post_dict),
            'user_has_posted': len(Post.query.with_entities(Post.user_id).distinct().all()),
            'comment_count': len(Komentar.query.all()),
            'id_post_most_comment': Post.query.order_by(Post.comment_count.desc()).first().id,
            'id_post_most_liked': Post.query.order_by(Post.like.desc()).first().id,
            'id_user_most_post': User.query.order_by(User.post_count.desc()).first().id
    }

        json_return = jsonify({
            'data' : post_dict,
            'meta' : meta
        }), HTTP_200_OK


    else:
        json_return = jsonify({}), HTTP_204_NO_CONTENT

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return




@post.get('/page')
@swag_from(f'{BASE_PATH_DOCS}/post_get_pagination.yaml')
def get_post_page():

    page = request.args.get('page', default= 1, type= int)
    per_page = request.args.get('per_page', default= 5, type= int)

    post_page = Post.query.paginate(page = page, per_page = per_page)

    page_post = []
    for post in post_page.items:
        data = post.post_info()
        page_post.append(data)

    if page_post != []:
        meta = {
            'page' : post_page.page,
            'total_page' : post_page.pages,
            'total_post' : post_page.total,
            'prev_page' : post_page.prev_num,
            'next_page': post_page.next_num,
            'has_prev': post_page.has_prev,
            'has_next': post_page.has_next
        }

        json_return = jsonify({
            'data': page_post,
            'meta': meta
        }), HTTP_200_OK

    else:
        json_return = jsonify({}), HTTP_204_NO_CONTENT

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return





@post.get('/<int:id>')
@swag_from(f"{BASE_PATH_DOCS}/post_get_single.yaml")
def get_post(id):

    request.access_control_request_headers

    post = Post.query.get(id)
    komen = {
        'id' : post.komentar
    }
    if post:
        post.visit += 1
        db.session.commit()

        json_return = jsonify({
            'info' : post.post_info()
        }), HTTP_200_OK



    else:
        json_return = jsonify(
            error = 'post tidak ditemukan'
        ), HTTP_404_NOT_FOUND

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return





@post.post('/add')
@jwt_required()
@swag_from(f"{BASE_PATH_DOCS}/post_add.yaml")
def add_post():

    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':

        data = request.get_json()
        try:
            title = data['title']
            subtitle = data['subtitle']
            body = data['body']

            user = User.query.get(current_user.id)

            new_post = Post(
                title = title,
                subtitle = subtitle,
                body = body,
                user = user
            )


            db.session.add(new_post)
            user.post_counter()
            db.session.commit()

            json_return = jsonify({
                'success' : {
                    'id_post' : new_post.id,
                    'title' : new_post.title,
                    'subtitle' : new_post.subtitle,
                    'body' : new_post.body,
                    'owner_id' : new_post.user_id,
                    'owner_username' : new_post.user.nama,
                    'created_at' : new_post.created_at,
                    'aksi' : 'tambah post'
                }
            }), HTTP_201_CREATED



        except KeyError:
            json_return  = wrong_parameter_input()

    else:
        json_return = non_json_input(check_req)


    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return





@post.put('/edit')
@post.patch('/edit')
@jwt_required()
@swag_from(f'{BASE_PATH_DOCS}/post_edit.yaml')
def edit_post():

    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':

        data = request.get_json()

        try:
            id_user_request = current_user.id
            id_post = data['id']
            title_new = data['new_title']
            subtitle_new = data['new_subtitle']
            body_new = data['new_body']

            edited_post = Post.query.get(id_post)
            if edited_post:
                if edited_post.check_access_post(id_user_request):

                    edited_post.title = title_new
                    edited_post.subtitle = subtitle_new
                    edited_post.body = body_new
                    db.session.commit()

                    json_return = jsonify(
                        success = {
                            'id_post' : edited_post.id,
                            'new_title' : edited_post.title,
                            'new_subtitle' : edited_post.subtitle,
                            'new_body' : edited_post.body,
                            'aksi' : 'edit_post',
                            'owner_username' : edited_post.user.username
                        }
                    ), HTTP_200_OK

                else:
                    json_return = jsonify(
                        error = 'Anda bukan pemilik post, tidak punya akses'
                    ), HTTP_401_UNAUTHORIZED

            else:
                json_return = jsonify(
                    error = 'post tidak ditemukan'
                ), HTTP_404_NOT_FOUND

        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(check_req)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return





@post.delete('/delete')
@jwt_required()
@swag_from(f'{BASE_PATH_DOCS}/post_delete.yaml')
def delete_post():

    request.access_control_request_headers
    check_req = request.headers.get('Content-Type')
    if check_req == 'application/json':
        try:
            data = request.get_json()
            id_requested = current_user.id
            id_post = data['id']

            deleted_post = Post.query.get(id_post)
            user = User.query.get(id_requested)
            if deleted_post and user:

                if deleted_post.check_access_post(user.id):

                    all_post_komen = Komentar.query.filter_by(post_id = deleted_post.id).all()
                    all_like = Like.query.filter_by(id_post = deleted_post.id).all()
                    if all_post_komen != []:
                        for x in all_post_komen:
                            db.session.delete(x)

                    if all_like != []:
                        for x in all_like:
                            db.session.delete(x)

                    db.session.delete(deleted_post)
                    user.post_counter()
                    user.komen_counter()
                    db.session.commit()

                    json_return = jsonify(
                        success = 'Berhasil hapus post'
                    ), HTTP_200_OK

                else:
                    json_return = jsonify(
                        error = 'Anda bukan pemilik, tidak punya akses'
                    ), HTTP_401_UNAUTHORIZED


            else:
                json_return = jsonify(
                    error = 'post/ user tidak ditemukan'
                ), HTTP_404_NOT_FOUND

        except KeyError:
            json_return = wrong_parameter_input()

    else:
        json_return = non_json_input(check_req)

    json_return[0].headers.add_header('Allow-Control-Access-Origin', '*')
    return json_return

























