This is a small flask app with mariaDB  backend. Its sole purpose is to learn how a small web app + db deployed on k8s.  
You can learn  
1. define secret and use it in container as environment variables
2. define persistenVolumeClaim and use it in db backend
3. define deployment, statefulset, service, secret and pvc
4. you can even learn Flask + python by studying the code (app.py)

## Running in Kubernetes

1. you can pull container image from docker.io/mskaraca/todoapp:v1.0 or build container image yourself by first cloneing this github repo and then building the image. Note docker.io can be accessed from hub.docker.com
```shell
github clone https://github.com/selcukKaraca/todoapp.git
docker image build -t todoapp:v1.0 .
```

1. This app is designed to run in k8s. To deploy in k8s, look at kubernetes/todoapp.yaml. It includes all resource definitions in 2 files. todoapp.yaml for web app and tododb.yaml for mariadb

3. tu run in k8s,

```shell
kubectl apply -f taskdb.yaml
kubectl apply -f  todoapp.yaml 
```

## MariaDB configuration
    when run in k8s, mariadb can initialize itself by some predefined environment variables. we followed this way. if you want to create mariadb and DB in it, you can use the following commands..

    ```shell
    #after ssh to the mariadb server..
    mysql -u root -p
    create database TASKDB;
    grant all privileges on TASKDB.* to 'taskuser'@'%' identified by 'taskpass';
    flush privileges;
    ```
## Building docker image and pushing it to docker.io
 to put your docker image in hub.docker.com

1. docker image build -t todoapp:v1.0
2. docker login --username=yourUserName  
3. docker tag todoapp:v1.0 yourUserName/todoapp:v1.0
4. docker push yourUsername/todoapp:v1.0

## SQLAlchemy
SQLAlchemy is what we interact with the DB in python.
It uses the following componenets:  
- engine: this defines the connection string to the database  
```shell
from sqlalchemy import create_engine
engine=create_engine('mysql+pymysql://user:pass@host/db')
```
This works according to DBAPI /Database API) specifictation. mysql is the lang and pymysql is the pyton module to tak with the mariadb.  

- ORM: Object relational Mapping ise a feature of sqlAlchemy. it provides us with working with python objects and it automatically constructs sql statements for us.
```shell
from sqlaalchemy.ext.declerative import decarative_base
Base=declarative_base()

class Product(Base):
   #this object will be mapped to this table..
   __tablename__='products'
   #these types come from Base class which is constructed from declarative_base class
   id=sqlalchmey.Column(sqlalchemy.Integer,primary_key=True)
   title=sqlalchemy.Column(sqlalchemy.String(50),nullable=False)
   creation_date=sqlalchemy.Column(sqlalchemy.DateTime,default=datetime.now)
```
- session: this is the transaction object. we work with sessions to make changes in db.
```shell

from sqlalchemy.orm import sessionmaker
engine=create_engine(...)
Session=sessionmaker(bind=engine)
session=Session()
```
- at the end to make actionsions:
```shell
#query
products=session.query(Product).all()
#query with a condition
products=session.query(Product)..filter(id=5)
for p in products:
   print(f"product name {p.title")

#insert
newproduct=Product(title='tennis ball')
session.add(newproduct)
#delete
products=session.query(Product).delete(id=5)
#update
id=5
oldp=session.query(Product).get(id)
oldp.title='tennis ball size 2'

session.commit()
sesion.close()
```

shortly;  
create a DB engine to connect  
use this engine to create session  
create a table object from declerative_base class  
Now use session.query(table) to interact with the DB