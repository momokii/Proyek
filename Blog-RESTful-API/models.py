from src import *
import datetime

def get_now_time():
    return datetime.datetime.now()



### ----------------------- JWT CALLBACKS ----------------------- ###
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    print(identity)
    return User.query.filter_by(id=identity).one_or_none()




### ----------------------- USER ----------------------- ###
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    password_hash = db.Column(db.String(300), nullable = False)
    email = db.Column(db.String(200), unique = True, nullable = False)
    nama = db.Column(db.String(50), nullable = False)
    post_count = db.Column(db.Integer, default = 0)
    komen_count = db.Column(db.Integer, default = 0)
    # relationship
    post = relationship('Post', back_populates = 'user')
    komentar = relationship('Komentar', back_populates = 'user')
    like = relationship('Like', back_populates = 'user')


    @property
    def password(self):
        self._password

    @password.setter
    def password(self, plain_password):
        self.password_hash = generate_password_hash(plain_password, salt_length= 8)


    def check_password(self, password_checking):
        if check_password_hash(self.password_hash, password_checking):
            return True
        else:
            return False

    def post_counter(self):
        self.post_count = len(self.post)

    def komen_counter(self):
        self.komen_count = len(self.komentar)





### ----------------------- POST ----------------------- ###

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    subtitle = db.Column(db.String(150), nullable = False)
    body = db.Column(db.Text, nullable = False)
    like_count = db.Column(db.Integer, default = 0)
    visit = db.Column(db.Integer, default = 0)
    comment_count = db.Column(db.Integer, default = 0)
    created_at = db.Column(db.DateTime, default = get_now_time())
    updated_at = db.Column(db.DateTime, onupdate = get_now_time())
    # relatonship
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates = 'post')
    komentar = relationship('Komentar', back_populates = 'post')
    like = relationship('Like', back_populates = 'post')

    def like_counter(self):
        self.like_count = len(self.like)

    def comment_counter(self):
        self.comment_count = len(self.komentar)

    def post_info(self):
        data = {
            'id_post': self.id,
            'title': self.title,
            'subtitle': self.subtitle,
            'body': self.body,
            'owner_id': self.user_id,
            'owner_name': self.user.nama,
            'visit': self.visit,
            'comment_count': self.comment_count,
            'created_at': self.created_at,
            'last_updated': self.updated_at
        }
        return data


    def check_access_post(self, id_request_access):
        if self.user_id == id_request_access:
            return True
        else:
            return False





### ----------------------- KOMENTAR ----------------------- ###

class Komentar(db.Model):
    __tablename__ = 'komentar'
    id = db.Column(db.Integer, primary_key = True)
    body_komentar = db.Column(db.String(240), nullable = False)
    created_at = db.Column(db.DateTime)
    # relationship
    post_id = db.Column(db.Integer, ForeignKey('post.id'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates = 'komentar')
    post = relationship('Post', back_populates = 'komentar')

    def check_valid_access(self, id_ingin_hapus):
        if (id_ingin_hapus == self.user_id) or (id_ingin_hapus == self.post.user_id):
            return True
        else:
            return False





class Like(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_post = db.Column(db.Integer, ForeignKey('post.id'))
    id_user = db.Column(db.Integer, ForeignKey('user.id'))

    # relationship
    user = relationship('User', back_populates = 'like')
    post = relationship('Post', back_populates = 'like')



db.create_all()





















