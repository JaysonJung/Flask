from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import *
#import requests
app=Flask(__name__)
#db설정
#app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///todo'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)
migrate = Migrate(app,db)

@app.route('/')
def index():
    todos=Todo.query.order_by(Todo.deadline.asc()).all()
    return render_template('index.html',todos=todos)

# @app.route('/posts/new')
# def new():
#     return render_template("new.html")
    
# @app.route('/posts/create',methods=['POST','GET'])
# def create():
#     todo=request.form['todo']
#     deadline=request.form.get('deadline')
#     todo=Todo(todo,deadline)
#     db.session.add.todo
#     db.session.commit()
#     return render_template("create.html")
@app.route('/todos/create',methods=['POST','GET'])
def todo():
    if request.method=="POST":
        todo=Todo(request.form['todo'],request.form['deadline'])
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        #데이터를 저장하는 로직
    return render_template('new.html')
@app.route('/todos/<int:id>/delete') 
def delete(id):
    todo =Todo.query.get(id)
    # DELETE FROM posts WHERE id=3;
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
#Edit
#Edit 경로 라우트에 추가
    #기존의 데이터를 가져와서 수정할수 있는 폼 보여주기
@app.route('/todos/<int:id>/edit')
def edit(id):
    todo=Todo.query.get(id)
    return render_template('edit.html',todo=todo)
#Update
#Update 경로 라우트에 추가
    #변경한 데이터를 가져와서 db에 반영
@app.route('/todos/<int:id>/update', methods=["POST","GET"])
def update(id):
    todo = Todo.query.get(id)
    todo.todo = request.form['todo']
    todo.deadline = request.form['deadline']
    # post.title = request.args.get('title')
    # post.content = request.args.get('content')
    db.session.commit()
    return redirect('/')
    
@app.route('/todos/<int:id>/upgrade',methods=["POST","GET"])
def upgrade(id):
    todo=Todo.query.get(id)
    if request.method=='POST':
        #게시물을 실제로 업데이트 하는 로직
        todo.todo=request.form['todo']
        todo.deadline=request.form['deadline']
        db.session.commit()
        return redirect('/')
    #수정할 수 있는 폼을 리턴
    return render_template('edit.html',todo=todo)
    