from src import *
from user import *
from komentar import *
from post import *
from like import *
from models import *


## ----------- GLOBAL ERROR HANDLER ------------ ##

@app.errorhandler(HTTP_404_NOT_FOUND)
def handler_404(e):
    return jsonify({
        'error' : 'halaman tidak ditemukan'
    }), HTTP_404_NOT_FOUND


@app.errorhandler(HTTP_405_METHOD_NOT_ALLOWED)
def handler_405(e):
    return jsonify({
        'error' : 'fungsi request tidak sesuai'
    }), HTTP_405_METHOD_NOT_ALLOWED


@app.errorhandler(HTTP_400_BAD_REQUEST)
def handler_400(e):
    return jsonify({
        'error': 'bad request'
    }), HTTP_400_BAD_REQUEST


@app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def handler_500(e):
    return jsonify({
        'error': 'server error'
    })


## ----------- BLUEPRINT CONFIG -------------- ##


app.register_blueprint(user)
app.register_blueprint(komentar)
app.register_blueprint(post)
app.register_blueprint(like)




if __name__ == '__main__':
    app.run(debug= True)