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
- at the end to make insetactionsions:
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