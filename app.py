from flask import Flask, request, render_template, redirect, flash, session
#from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Person
from sqlalchemy import create_engine


app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///jeffreyng'
app.config['SQLACLHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'nowayJose'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    stuff= User.query.all()
    return render_template('home.html', stuff=stuff)

@app.route('/', methods=['POST'])
def add_user():
    first_name= request.form['first_name']
    last_name= request.form['last_name']
    image_url= request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/{new_user.id}')

@app.route('/<int:id>')
def create_user(id):
    name= User.query.get_or_404(id)
    return render_template('details.html', name=name)  

@app.route('/<int:id>', methods=['POST'])
def delete_member(id):
    User.query.filter(User.id == id).delete()
    db.session.commit()
    return render_template('edit.html')



@app.route('/edit', methods=['POST'])
def delete_user():
    all_subjects=User.query.all()
    first_name= request.form['first_name']
    last_name= request.form['last_name']
    image_url= request.form['image_url']
    
    
    
    for ele in all_subjects:
        if ele.first_name == first_name:
            pass
        else:
            User.query.filter(User.first_name==first_name).delete()
            
            
    for ele in all_subjects:
        if ele.last_name == last_name:
            pass
        else:
            User.query.filter(User.last_name==last_name).delete()
            
            
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    
    db.session.commit()

    all_subjects=User.query.all()
    
    
    return render_template('edit.html', stuff=all_subjects)
 
    