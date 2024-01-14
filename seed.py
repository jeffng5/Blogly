from app import app
from models import Blog, db, User, Blog_Tag, Tag

db.drop_all()
db.create_all()

db.session.commit()