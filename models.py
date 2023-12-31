from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                    primary_key= True,
                    autoincrement= True)
    
    first_name = db.Column(db.String(50),
                    nullable=False)
    last_name = db.Column(db.String(50),
                    nullable=False)
    image_url = db.Column(db.String(50))


class Blog(db.Model):

    __tablename__= 'blogs'

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement= True)
    title = db.Column(db.Text,
                    nullable=False)
    content = db.Column(db.Text,
                    nullable=False)
    created_at = db.Column(db.Date,
                    nullable = True)
    user_id= db.Column(db.Integer,
                    db.ForeignKey('users.id'))   
    
    join=db.relationship('User', backref='blogs')
    