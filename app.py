from crypt import methods
#Flask: web framework and our main piece, request: to process form data inside app, render_template: to send html pages with j2 extensions, 
#redirect: to reidrect a request to another flask route
from flask import Flask, request,render_template, redirect
#to find IP and hostname
import socket
#task's date and time information taken from here
from datetime import datetime
#mariaDB support with ORM (object relational mapping)
import sqlalchemy
#mariadb connection support
from sqlalchemy import create_engine
#ORM support
from sqlalchemy.ext.declarative import  declarative_base
# to read env variables from SHELL
import os

app=Flask(__name__)
try:
    dbUsername=os.environ['USERNAME']
    dbPassword=os.environ['PASSWORD']
    dbName=os.environ['DBNAME']
except:
    print("db username,password and name can not be empty. provide those with a secret mounted as env variables!")
    print (f"conn string: {dbUsername}:{dbPassword}@{dbName}")

#get hname and IP.
hname=socket.gethostname()
IP=socket.gethostbyname(hname)

#mariaDB DB code. we define ORM (object relational mapping) method
Base=declarative_base()
Session=sqlalchemy.orm.sessionmaker()

connString=f"mysql+pymysql://{dbUsername}:{dbPassword}@taskdb/{dbName}?charset=utf8mb4"

taskdb=create_engine(connString)
Session.configure(bind=taskdb)
session=Session()



#this represents  our table.
class Todo(Base):
    __tablename__='todo'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    task_name = sqlalchemy.Column(sqlalchemy.String(100),nullable=False)
    task_date = sqlalchemy.Column(sqlalchemy.DateTime,default=datetime.now,onupdate=datetime.now)

@app.route('/installDB')
def installDB():
    return render_template('installdb.html',IP=IP,hname=hname)

#createdb checks secret code and creates db table..     
@app.route('/createdb',methods=['GET','POST'])
def createDB():
     # get the code from form
     secretCode=request.form.get('code')
     if secretCode=='333':
         try:
            #create table if not exists..
            Base.metadata.create_all(taskdb)
         except Exception as e:
            return  f"DB baglantisinda hata alindi..Error {e}"
         return "db created"
     else:
         return "kodu hatalı girdiniz..."


#if a new task added with add task then we add it to the ORM represantion of the table
@app.route('/addTask',methods=['GET','POST'])
def addTask():
  try:  
    tname=request.form.get("taskName")
    if tname=='':
        return "bos kayit girilemez.."
    newTask=Todo(task_name=tname)
    session.add(newTask)
    session.commit()
  
    return redirect('/')
  except Exception as e:
  
    return f"DB ile ilgili bir sorun olustu. \nHata mesajı {e}"

@app.route('/update/<int:id>',methods=['GET','POST'])
def updateForm(id):
     selectedTask = session.query(Todo).get(id)
     return render_template('update.html',task=selectedTask)

@app.route('/updater/<int:id>',methods=['GET','POST'])
def update (id):
   selectedTask = session.query(Todo).get(id)
   selectedText=request.form.get('taskText')
   
   selectedTask.task_name=selectedText
   session.commit()
   return redirect('/')

@app.route('/')
def index():
    try:
        tasks=session.query(Todo).all()
    except:
    
        return render_template('index.html',IP=IP,hname=hname)
    else:
        return  render_template('index.html',IP=IP,hname=hname,tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
     session.query(Todo).filter(Todo.id == id).delete()
     session.commit()
     return redirect('/')

#if we are called directly (not as a module) run the program...
if __name__=='__main__':
    #run in debug mode and listen all IP addresses
    app.run(debug=True,host="0.0.0.0")