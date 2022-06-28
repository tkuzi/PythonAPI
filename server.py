from flask import Flask,jsonify, request
from datetime import datetime
# standaard lib dat meekomt met python
from sqlite3 import Connection as SQLite3Connection
# ORM wrappper voor SQL en flask

# nodig voor de foreing keys te kunnen editen en de tables bij elkaar te voegen
from sqlalchemy import event
from sqlalchemy.engine import Engine


from flask_sqlalchemy import SQLAlchemy

###
# app
###

# name is een standaard voor flask en geeft access to routes etc
app = Flask(__name__)

# linken van een env var naar een andere dictionary
# zonder deze config krijgen we errors
# bij setup genruikt sqlite geen key constraints
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

#config sqlite om de foreign key constraints te editten -> dan kan je tabellen met elkaar joinen dmv de primary key
# om de db connnectie te configureren voor foreign keys te gebruiken -> niet leren !!!!!
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

#linken van flask met sqlite via de ORM
db = SQLAlchemy(app) # Creating an instance of SQLalchemy class 

# wordt gebruikt om later de tables te updaten
now = datetime.now()
###
# models
###

# De ORM zorgt voor simpelere modellen

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    adress = db.Column(db.String(200))
    posts = db.relationship("BlogPost")
    
class BlogPost(db.Model):
    __tablename__ = 'blog_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable = False) #link maken naar de andere table

print('run the script succesfull')

###
# routes
###

# need to use the decorator

@app.route("/user", methods=["POST"]) #als een user in de url zit, dan wordt de create_user functie opgeroepen
def create_user():
    pass



@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    pass


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    pass


@app.route("/user/<user_id>", methods=["GET"]) #<user_id> is een variabele dat we uit de route gaan halen
def get_one_user(user_id):
    pass


# <user_id> is een variabele dat we uit de route gaan halen
@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    pass




@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):
    pass


@app.route("/user/<user_id>", methods=["GET"])
def get_all_blog_posts(user_id):
    pass


@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    pass


@app.route("/blog_post/<blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id):
    pass


#if we run this server.py file as our main application, then we are going to start our api with debug on True
#als we in de terminal python server.py runnen, dan gaat de interne variable __name__ gelijk zijn aan __main__
if __name__ == "__main__":
    app.run(debug=True)