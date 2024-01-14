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
    return render_template('personal.html', name=name, tags_available=tags_available, id =id)  

# delete indv users
@app.route('/users/<int:id>/delete', methods=['POST'])
def delete_member(id):
    # stuff=User.query.get_or_404(id)
    User.query.filter(User.id == id).delete()
    db.session.commit()
    # all_blogs=Blog.query.filter(Blog.user_id==id)

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
    # image_url= request.form['image_url']
    
    
    
    # for ele in all_subjects:
    #     if ele.first_name == first_name:
    #         pass
    #     else:
    #         User.query.filter(User.first_name==first_name).delete()
            
            
    # for ele in all_subjects:
    #     if ele.last_name == last_name:
    #         pass
    #     else:
    #         User.query.filter(User.last_name==last_name).delete()
            
            
    
    new_user = User(first_name=first_name, last_name=last_name)
    db.session.add(new_user)
    
    db.session.commit()

  

    
    return render_template('user_list.html')

@app.route('/personal', methods=['GET','POST'])
def personal():
    if 'title' in request.form:
        title=request.form['title']
    if 'content' in request.form:
        content=request.form['content']
    if 'created_at' in request.form:
        created_at=request.form['created_at']
    if 'user_id' in request.form:
        user_id=request.form['user_id']
    else:
        all_blogs= 'There is no such thing!'
    new_blog= Blog(title=title, content=content, created_at=created_at, user_id=user_id)
    db.session.add(new_blog)
    db.session.commit()
    all_blogs=Blog.query.filter(Blog.user_id==user_id)
    name=User.query.filter(User.id==user_id)

    return render_template('personal.html', all_blogs=all_blogs, name=name)

@app.route('users/<int:id>/posts/new')
def new_post():
    return render_template('post_form.html')



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

@app.route("/tags/:id/delete")
def delete_tag():
    Tag.query.filter(Tag.id==id).delete()
    db.session.commit()
    return render_template("tag_list.html")
