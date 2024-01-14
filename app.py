from flask import Flask, request, render_template, redirect, flash, session
#from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Blog, Tag
from sqlalchemy import create_engine


app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///template1'
app.config['SQLACLHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'nowayJose'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)




#home page
@app.route('/')
def home_page():
    return render_template('home.html')

# List of users
@app.route("/users")
def all_users():
    name = User.query.all()
    return render_template('user_list.html', name=name)

@app.route("/", methods=['POST'])
def user_signup():
    first_name = request.form['first_name']
    last_name = request.form['last_name']

    new_user = User(first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users')    

# create user form
@app.route("/users/new")
def new_user():
    return render_template('add_user.html')

# creates/add user
@app.route('/users/new', methods=['POST'])
def add_user():
    first_name= request.form['first_name']
    last_name= request.form['last_name']
    image_url= request.form['image_url']

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users')

#individual users details with tag avail
@app.route('/users/<int:id>')
def get_indv_user(id):
    name= User.query.get_or_404(id)
    tags_available = Tag.query.all()
    blogs= Blog.query.filter(Blog.user_id==id)
    return render_template('personal.html', name=name, tags_available=tags_available, blogs=blogs, id=id)  

# delete indv users
@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_member(id):
    User.query.filter(User.id == id).delete()
    db.session.commit()
    return render_template('user_list.html')

@app.route('/users/<int:id>/edit')
def edit_user_form(id):
    name = User.query.get_or_404(id)
    return render_template('edit.html', name=name)

@app.route('/users/<int:id>/edit', methods=['POST'])
def edit_user(id):
    all_subjects=User.query.all()
    user= User.query.get_or_404(id)
    first_name= request.form['first_name']
    last_name= request.form['last_name']
    new_user = User(first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    
    db.session.commit()

  

    
    return render_template('user_list.html')





@app.route("/tags")
def tag_list():
    results = Tag.query.all()
    return render_template("tag_list.html", results=results)

@app.route("/tags/:id")
def tag_details():
    results = Tag.query.get_or_404(id)
    return render_template("tag.html", results = results)

@app.route("/tags/:id/edit")
def edit_tag():
    return render_template("edit_tag_form.html")

@app.route("/tags/:id/edit", methods=['POST'])
def edit_tag_post():
    tag_name = request.form['name']
    # edit_tag = Tag(name=name)
    tag = Tag.query.get_or_404(id)
    tag.name = tag_name
    db.session.commit()
    return render_template("tag_list.html")


@app.route("/tags/new")
def new_tag():
    return render_template("tag_form.html")

@app.route("/tags/<int:id>/delete")
def delete_tag():
    Tag.query.filter(Tag.id==id).delete()
    db.session.commit()
    return render_template("tag_list.html")

@app.route('/users/<int:id>/posts/new', methods=['POST'])
def personal(id):
    title=request.form['title']
    content=request.form['content']
    created_at=request.form['created_at']
    user_id=request.form['user_id']
    new_blog= Blog(title=title, content=content, created_at=created_at, user_id=user_id)
    db.session.add(new_blog)
    db.session.commit()
    name= User.query.filter(User.id==id)
    blogs= Blog.query.filter(Blog.user_id==id)
    return render_template('personal.html', name=name, blogs=blogs)

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    
    blogs=Blog.query.filter(Blog.id==post_id)
    
    return render_template('post_detail.html', blogs=blogs)

@app.route('/users/<int:id>/posts/new')
def new_post(id):
    name= User.query.get_or_404(id)
    return render_template('post_form.html', name=name)

@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    Blog.query.filter(Blog.id==post_id).delete()
    db.session.commit()
    return render_template("personal.html")