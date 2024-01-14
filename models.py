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
    image_url = db.Column(db.String(50), nullable = True)

    user = db.relationship("Blog", cascade='all,delete', backref='users')


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
    
    user=db.relationship('User', backref='blogs')
    
    tags= db.relationship('Tag', secondary = 'blogtags', backref= 'blogs')
    
class Blog_Tag(db.Model):
    __tablename__ = "blogtags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)

class Tag(db.Model):
    __tablename__= "tags"
    id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    name = db.Column(db.Text, nullable = False)
        
        