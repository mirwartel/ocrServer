from datetime import datetime
from sqlalchemy.dialects.sqlite import DATETIME

from sqlalchemy.ext.automap import automap_base

from ocrApp import db

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key="true")
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


class Folder(db.Model):
    __tablename__ = 'folders'
    id = db.Column(db.Integer, primary_key="true")
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uploader = db.Column(db.String, db.ForeignKey('users.username'))
    name = db.Column(db.String)
    users = db.relationship("User")

    def __repr__(self):
        return '<Folder %r>' % self.id


class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key="true")
    page_number = db.Column(db.Integer, nullable=False, )
    text = db.Column(db.String)
    name = db.Column(db.String)
    image_original = db.Column(db.String)
    image_processed = db.Column(db.String)
    image_boxes = db.Column(db.String)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    uploader = db.Column(db.String, db.ForeignKey('users.username'))
    users = db.relationship("User")
    folder = db.Column(db.Integer, db.ForeignKey('folders.id'))
    folders = db.relationship("Folder")

    def __repr__(self):
        return '<Document %r>' % self.id


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key="true")
    username = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self):
        return '<User %r>' % self.username
