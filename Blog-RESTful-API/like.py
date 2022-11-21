from src import *
from models import *


like = Blueprint('like', __name__,
                 url_prefix= '/api/liked')




# ------------------ LIKE ------------------- #


@like.post('/<int:id>')
@jwt_required()
@swag_from('./docs/like/like_post.yaml')
def like_post(id):

    request.access_control_request_headers

    post_liked = Post.query.get(id)
    user = User.query.get(current_user.id)

    if user and post_liked:

        check_liked = Like.query.filter_by(id_post = id,
                                           id_user = current_user.id).first()

        if check_liked:
            db.session.delete(check_liked)
            hasil = 'sudah pernah like sebelumnya, like dihapus'
        else:
            new_liked = Like(
                id_post = post_liked.id,
                user = user
            )
            db.session.add(new_liked)
            hasil = 'postingan dilike'

        post_liked.like_counter()
        db.session.commit()
        json_return = jsonify(success = hasil), HTTP_200_OK



    else:
        json_return = jsonify(error = 'terjadi kesalaha, post/ user tidak ditemukan'), HTTP_404_NOT_FOUND




    json_return[0].headers.add_header('Allow-Control-Access-Origin', "*")
    return json_return