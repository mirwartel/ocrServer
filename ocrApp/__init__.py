from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

app.secret_key = 'secret_key'

UPLOAD_FOLDER = 'C:\\Users\\Lord of Eight peaks\\PycharmProjects\\ocrServer\\ocrApp\\static\\uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///document-db.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

from ocrApp import views
