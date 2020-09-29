import os

from werkzeug.utils import secure_filename

from ocrApp import db
from ocrApp import app
from flask import render_template, request, redirect, flash, url_for

from ocrApp.forms import LoginForm, RegisterForm
from ocrApp.models import Todo, Folder, Document, User
from ocrApp.ocrEngine2 import runOcrEngine2
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    folders = Folder.query.order_by(Folder.id).all()
    print(folders)
    return render_template("index.html", folders=folders)


@app.route('/folder/<int:id>', methods=['GET'])
def folder(id):
    folder_to_open = Folder.query.get_or_404(id)

    documents = Document.query.filter_by(folder=id).all()
    print(documents)
    return render_template("folder.html", folder=folder_to_open, documents=documents)


@app.route('/folder/<int:id>/create_new_document', methods=['POST', 'GET'])
@login_required
def create_new_document(id):
    uploader = 'user'  # create login system to replace
    folder_to_open = Folder.query.get_or_404(id)
    if request.method == 'POST':

        if 'image_original' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image_original']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        document_name = request.form['name']

        document_image_original = file.filename

        number_of_documents = len(Document.query.filter_by(folder=id).all()) + 1
        new_document = Document(page_number=number_of_documents, name=document_name,
                                image_original=document_image_original, uploader=uploader, folder=id)
        print(new_document)
        try:
            db.session.add(new_document)

            print(new_document)
            db.session.commit()

            print(new_document)
            return redirect('/')
        except:
            return 'There was an issue adding your task.'

    else:

        return render_template("create_new_document.html", folder=folder_to_open)


@app.route('/document/<int:id>', methods=['POST', 'GET'])
def document(id):
    document_to_open = Document.query.get_or_404(id)

    try:
        with open('static/textFiles/' + document_to_open.text, mode='r') as f:
            textFromFile = f.read()
    except:
        textFromFile = None

    if request.method == 'POST':
        try:
            img = document_to_open.image_original

            file = "document" + str(document_to_open.id) + ".text"

            runOcrEngine2(img, file)

            document_to_open.text = file
            db.session.commit()

            return redirect(url_for('document', id=id))
        except:
            return 'There was an issue with the OCR.'

    else:

        return render_template("document.html", document=document_to_open, text=textFromFile)


# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)
#
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that task.'
#
#
# @app.route('/update/<int:id>', methods=['POST', 'GET'])
# def update(id):
#     task = Todo.query.get_or_404(id)
#     if request.method == 'POST':
#         task.content = request.form['content']
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was a problem updating that task.'
#     else:
#         return render_template('update.html', task=task)
#

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        return '<h1> invalid username or password</h1>'

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>new user has been created</h1>'

    return render_template('signup.html', form=form)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
