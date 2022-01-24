This is a small flask app with mariaDB  backend. Its sole purpose is to learn how a small web app + db deployed on k8s.  
You can learn  
1. define secret and use it in container as environment variables. (we defined secret, show it in container as env variables. Inside code we used this env variables to define db access variables)
2. define persistenVolumeClaim and use it in db backend (you can use a storageClass or simpler a hostPath for this purpose. If you use hostPath, please make directory before using it in yaml files. look at kubernetes/tododb.yaml)
3. define deployment, statefulset, service, secret and pvc
4. you can even learn Flask + python by studying the code (app.py)

## Running in docker

1.
for the DB backend, you need to run mariadb container
```shell
#run mariadb container
docker run -e MYSQL_USER=taskuser -e MYSQL_PASSWORD=taskpass -e MYSQL_DATABASE=TASKDB  -e MYSQL_ROOT_PASSWORD=abrakadabra  -d --name taskdb -p 3306:3306 mariadb:10.7
# find IP address of this continer
docker ps 
docker inspect <Container ID from previous> | grep "IPAddress"
#We will use this IP below..

```
2.
 you can pull container image from docker.io/mskaraca/todoapp:v1.0 
 
 or build container image yourself by first clonening this github repo and then building the image. 
```shell
github clone https://github.com/selcukKaraca/todoapp.git
docker image build -t todoapp:v1.0 .
```
OR shortly run the container
```shell
docker run -e USERNAME=taskuser -e PASSWORD=taskpass -e DBNAME=TASKDB -d --rm --name todoapp -p 5000:5000 --add-host=taskdb:<Above_IPAddress> mskaraca/todoapp:v1.0

```

Now you can access app by opening your browser and hit the following URL:  
```shell
localhost:5000
```

firstly, select "Install/Reset Database" from left side. when a secret code is asked, enter 333. You need to this just at the beginning. then you can add,delete and update todo records..

## Running in Kubernetes

1. This app is designed to run in k8s. To deploy in k8s, look at kubernetes folder. It includes all resource definitions in 2 files. todoapp.yaml for web app and tododb.yaml for mariadb

3. tu run in k8s,

```shell
kubectl apply -f taskdb.yaml
kubectl apply -f  todoapp.yaml 
```

## MariaDB configuration
    when run in k8s, mariadb can initialize itself by some predefined environment variables. we followed this way. if you want to create mariadb and DB  yourself you can use the following commands..

    ```shell
    #after ssh to the mariadb server..
    mysql -u root -p
    create database TASKDB;
    grant all privileges on TASKDB.* to 'taskuser'@'%' identified by 'taskpass';
    flush privileges;
    ```
## Building docker image and pushing it to docker.io
 to put your docker image in hub.docker.com. (Note docker.io can be accessed from hub.docker.com)

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
This works according to DBAPI /Database API) specifictation. mysql is the dialect (a kind of SQL language) and pymysql is the pyton module to tak with the mariadb.  

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
- at the end to make transactions:
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
1. create a DB engine to connect  
2. use this engine to create session  
3. create a table object from declerative_base class  
4. Now use session.query(table) to interact with the DB