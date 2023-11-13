from app import app
from models import Blog, db, User

db.drop_all()
db.create_all()

db.session.commit()