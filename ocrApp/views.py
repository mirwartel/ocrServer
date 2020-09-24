from ocrApp import db
from ocrApp import app
from flask import render_template, request, redirect

from ocrApp.models import Todo, Folder, Document


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task.'
    else:
        folders = Folder.query.order_by(Folder.id).all()
        print(folders)
        return render_template("index.html", folders=folders)


@app.route('/folder/<int:id>', methods=['POST', 'GET'])
def folder(id):
    folder_to_open = Folder.query.get_or_404(id)
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task.'
    else:

        documents = Document.query.filter_by(folder=id).all()
        print(documents)
        return render_template("folder.html", folder=folder_to_open, documents=documents)


@app.route('/document/<int:id>', methods=['POST', 'GET'])
def document(id):
    document_to_open = Document.query.get_or_404(id)
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task.'
    else:


        return render_template("document.html", document=document_to_open)



@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task.'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating that task.'
    else:
        return render_template('update.html', task=task)
