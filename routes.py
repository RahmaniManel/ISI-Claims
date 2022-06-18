import os
from flask_sqlalchemy import SQLAlchemy
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort, json, jsonify
from appvf import app, db, bcrypt
from appvf.forms import RegistrationForm, RegistrationFormM, LoginForm, LoginFormM, UpdateAccountForm, PostForm, Form
from appvf.models import User, Admin, Post, Student, Mater, Specialty, Feild, Group, Note
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")

@app.route("/welcome")
def welcome():
    return render_template('welcome.html', title='welcome')



@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/homea")
def homea():
    posts = Post.query.all()
    return render_template('home2.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('welcome'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))





#insert students
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
  
        my_data = Student(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
  
        flash("Student Inserted Successfully")
        return redirect(url_for('indexstudent'))
  
#update students
@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Student.query.get(request.form.get('id'))
  
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
  
        db.session.commit()
        flash("Student Updated Successfully")
        return redirect(url_for('indexstudent'))
  
#delete students
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Student.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted Successfully")
    return redirect(url_for('indexstudent'))


#insert data to mater 
@app.route('/insertm', methods = ['POST'])
def insertm():
    if request.method == 'POST':
        name = request.form['name']
        coff = request.form['coff']
        namespecialty = request.form['namespecialty']
        namefeild = request.form['namefeild']
       
  
        my_data = Mater(name, coff, namespecialty, namefeild)
        db.session.add(my_data)
        db.session.commit()
  
        flash("Mater Inserted Successfully")
        return redirect(url_for('indexmater'))
  #update Mater
@app.route('/updatem', methods = ['GET', 'POST'])
def updatem():
    if request.method == 'POST':
        my_data = Mater.query.get(request.form.get('id'))
  
        my_data.name = request.form['name']
        my_data.coff = request.form['coff']
        my_data.namespecialty = request.form['namespecialty']
        my_data.namefeild = request.form['namefeild']
        
  
        db.session.commit()
        flash("Mater Updated Successfully")
        return redirect(url_for('indexmater'))

#delete data from Mater
@app.route('/deletem/<id>/', methods = ['GET', 'POST'])
def deletem(id):
    my_data = Mater.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Mater Deleted Successfully")
    return redirect(url_for('indexmater'))


#insert data to Specialty 
@app.route('/inserts', methods = ['POST'])
def inserts():
    if request.method == 'POST':
        name = request.form['name']

        my_data = Specialty(name)
        db.session.add(my_data)
        db.session.commit()
  
        flash("Specialty Inserted Successfully")
        return redirect(url_for('indexspecialty'))

  #update Specialty
@app.route('/updates', methods = ['GET', 'POST'])
def updates():
    if request.method == 'POST':
        my_data = Specialty.query.get(request.form.get('id'))
  
        my_data.name = request.form['name']
  
        db.session.commit()
        flash("Specialty Updated Successfully")
        return redirect(url_for('indexspecialty'))
  
#delete Specialtys
@app.route('/deletes/<id>/', methods = ['GET', 'POST'])
def deletes(id):
    my_data = Specialty.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Specialty Deleted Successfully")
    return redirect(url_for('indexspecialty'))



#insert data to Feild 
@app.route('/insertf', methods = ['POST'])
def insertf():
    if request.method == 'POST':
        name = request.form['name']
        specialtyid = request.form['specialtyid']

        my_data = Feild(name,specialtyid)
        db.session.add(my_data)
        db.session.commit()
  
        flash("Feild Inserted Successfully")
        return redirect(url_for('indexfeild'))

  #update Feild
@app.route('/updatef', methods = ['GET', 'POST'])
def updatef():
    if request.method == 'POST':
        my_data = Feild.query.get(request.form.get('id'))
  
        my_data.name = request.form['name']
        my_data.specialtyid = request.form['specialtyid']
  
        db.session.commit()
        flash("Specialty Updated Successfully")
        return redirect(url_for('indexfeild'))
  
#delete Feild
@app.route('/deletef/<id>/', methods = ['GET', 'POST'])
def deletef(id):
    my_data = Feild.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Specialty Deleted Successfully")
    return redirect(url_for('indexfeild'))





#insert data to group
@app.route('/insertg', methods = ['POST'])
def insertg():
    if  request.method == 'POST':
        name = request.form['name']
        feildid = request.form['feildid']

        my_data = Group(name,feildid)
        db.session.add(my_data)
        db.session.commit()
  
        flash("Group Inserted Successfully")
        return redirect(url_for('indexgroup'))

  #update group
@app.route('/updateg', methods = ['GET', 'POST'])
def updateg():
    if request.method == 'POST':
        my_data = Group.query.get(request.form.get('id'))
  
        my_data.name = request.form['name']
        my_data.feildid = request.form['feildid']
  
        db.session.commit()
        flash("Group Updated Successfully")
        return redirect(url_for('indexgroup'))
  
#delete group
@app.route('/deleteg/<id>/', methods = ['GET', 'POST'])
def deleteg(id):
    my_data = Group.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Group Deleted Successfully")
    return redirect(url_for('indexgroup'))



@app.route('/indexgroup')
def indexgroup():
    all_data = Group.query.all()
    return render_template("indexgroup.html", groups = all_data)










@app.route('/indexfeild')
def indexfeild():
    all_data = Feild.query.all()
    return render_template("indexfeild.html", feilds = all_data)






@app.route('/indexmater')
def indexmater():
    all_data = Mater.query.all()
    return render_template("indexmater.html", maters = all_data)


@app.route('/indexspecialty')
def indexspecialty():
    all_data = Specialty.query.all()
    return render_template("indexspecialty.html", specialtys = all_data)



@app.route('/indexstudent')
def indexstudent():
    all_data = Student.query.all()
    return render_template("indexstudent.html", students = all_data)



#####admin#####################
@app.route('/home2')
def home2():
    return render_template("home2.html", title = home2)


@app.route("/registeradmin", methods=['GET', 'POST'])
def registeradmin():
    if current_user.is_authenticated:
        return redirect(url_for('home2'))
    form = RegistrationFormM()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(adminname=form.adminname.data, email=form.email.data, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('loginadmin'))
    return render_template('registeradmin.html', title='Registeradmin', form=form)


@app.route("/loginadmin", methods=['GET', 'POST'])
def loginadmin():
    if current_user.is_authenticated:
        return redirect(url_for('homea'))
    form = LoginFormM()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('homea'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('loginadmin.html', title='Loginadmin', form=form)


@app.route("/logoutadmin")
def logoutadmin():
    logout_user()
    return redirect(url_for('welcome'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn



###################addnote#########################################################

#app.py

      
@app.route('/addnote', methods=['GET', 'POST'])
def addnote():
    form = Form()
    form.specialty.choices = [(specialty.id, specialty.name) for specialty in Specialty.query.all()]
  
    if request.method == 'POST':
       group = Group.query.filter_by(id=form.group.data).first()
       specialty = Specialty.query.filter_by(id=form.specialty.data).first()
       feild = Feild.query.filter_by(id=form.feild.data).first()
       #return '<h2>Specialty : {}, Feild: {}, Group: {}</h2>'.format(specialty.name, feild.name, group.name)
       return render_template('test.html',specialty=specialty , feild=feild , group=group)
    return render_template('addnote.html', form=form)     


  


 
@app.route('/feild/<get_feild>')
def feildbyspecialty(get_feild):
    feild = Feild.query.filter_by(specialtyid=get_feild).all()
    feildArray = []
    for group in feild:
        feildObj = {}
        feildObj['id'] = group.id
        feildObj['name'] = group.name
        feildArray.append(feildObj)
    return jsonify({'feildspecialty' : feildArray})
  
@app.route('/group/<get_group>')
def group(get_group):
    feild_data = Group.query.filter_by(feildid=get_group).all()
    groupArray = []
    for group in feild_data:
        groupObj = {}
        groupObj['id'] = group.id
        groupObj['name'] = group.name
        groupArray.append(groupObj)
    return jsonify({'grouplist' : groupArray}) 

#moyen
@app.route('/moyen/<id>/', methods = ['GET', 'POST'])
def moyen(id):
    c=0
    total=0
    maters = Mater.query.all()
    notes = Note.query.filter_by(student_id=id)
    for x in notes:
        mater = Mater.query.get_or_404(x.mater_id)
        coff = mater.coff
        total = total + (x.note_TP/3 + x.note_ds*2/9 + x.note_examen*4/9)*coff
        c = c + coff
    moyen = total / c
    return render_template('moyen.html', moyen=moyen)
  