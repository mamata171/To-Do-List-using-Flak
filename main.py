
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/todo-flask'

db.init_app(app)

class todos(db.Model):
    title = db.Column(db.String(80),primary_key=True , unique=True, nullable=False,)
    desc = db.Column(db.Text, unique=True, nullable=False)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/todo',methods = ['GET','POST'])
def todo():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        
        entry = todos(title = title,desc = desc)
        db.session.add(entry)
        db.session.commit()

        print('data has been added to db successfully')

    return render_template('todo.html')

@app.route('/dashboard')
def dashboard():
    task = todos.query.all()
   
    return render_template('dashboard.html',tasks = task)


@app.route('/edit/<string:title>',methods = ['GET','POST'])
def edit(title):

    if request.method == "POST":
        title_form = request.form.get('title')
        desc_form = request.form.get('desc')
        
        if title == '0':
            entry = todos(title = title_form,desc = desc_form)
            db.session.add(entry)
            db.session.commit()
            print("new data added")
            return redirect('/edit/'+title)
    
        else:
            task = todos.query.filter_by(title = title).first()
            task.title = title_form
            task.desc = desc_form
            db.session.commit()
            print("daatta edited *************************")
            print(task.title)
            print(task.desc)
            return redirect('/edit/'+title)

            

    task = todos.query.filter_by(title = title).first()
    print(task)
    print(title)
    return render_template('edit.html',task = task,title = title)

            


app.run(debug=True)