from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import  datetime

app = Flask(__name__) # refers to this file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # '////' implies an absolute path & '///' is a relative path, ie, it will reside in the project folder
db = SQLAlchemy(app) # init db

# creating model
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text_content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods = ['POST', 'GET']) # @ is a decorator
def index():
    if request.method == 'POST':
        task_content = request.form['content'] # id of i/p is 'content'
        new_task = ToDo(text_content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task...'

    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks = tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting your task...'


@app.route('/update/<int:id>', methods = ['POST', 'GET'])
def update(id):
    task_to_update = ToDo.query.get_or_404(id)

    if request.method == 'GET':
        return render_template('update.html', task = task_to_update)
    else:
        task_to_update.text_content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task...'


if __name__ == '__main__':
    app.run(debug = True)