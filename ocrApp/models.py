from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.dialects.sqlite import DATETIME

from sqlalchemy.ext.automap import automap_base

from ocrApp import db

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key="true", nullable=False, unique=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


class Folder(db.Model):
    __tablename__ = 'folders'
    id = db.Column(db.Integer, primary_key="true", nullable=False, unique=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uploader = db.Column(db.String, db.ForeignKey('users.username'), nullable=False, )
    name = db.Column(db.String, nullable=False, unique=True)
    users = db.relationship("User")

    def __repr__(self):
        return '<Folder %r>' % self.id


class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key="true", nullable=False, unique=True)
    page_number = db.Column(db.Integer, nullable=False, )
    text = db.Column(db.String, default=None)
    name = db.Column(db.String, default=None)
    image_original = db.Column(db.String, default=None)
    image_processed = db.Column(db.String, default=None)
    image_boxes = db.Column(db.String, default=None)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uploader = db.Column(db.String, db.ForeignKey('users.username'), nullable=False, )
    users = db.relationship("User")
    folder = db.Column(db.Integer, db.ForeignKey('folders.id'), nullable=False, )
    folders = db.relationship("Folder")

    def __repr__(self):
        return '<Document %r>' % self.id


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key="true", nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False, )
    password = db.Column(db.String, nullable=False, )
    authenticated = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
