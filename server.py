from flask import Flask, jsonify, request
from datetime import datetime
import random

# standaard lib dat meekomt met python
from sqlite3 import Connection as SQLite3Connection
from matplotlib.pyplot import title

# ORM wrappper voor SQL en flask

# nodig voor de foreing keys te kunnen editen en de tables bij elkaar te voegen
from sqlalchemy import event
from sqlalchemy.engine import Engine


from flask_sqlalchemy import SQLAlchemy

# @@@@@@@@@@@@@
import linked_listv3
import hashTable
import binary_search_tree

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

# config sqlite om de foreign key constraints te editten -> dan kan je tabellen met elkaar joinen dmv de primary key
# om de db connnectie te configureren voor foreign keys te gebruiken -> niet leren !!!!!
@event.listens_for(Engine, "connect")  # @event is een decorator
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# linken van flask met sqlite via de ORM
db = SQLAlchemy(app)  # Creating an instance of SQLalchemy class

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
    posts = db.relationship("BlogPost", cascade="all, delete") #wnr we de user deleten wordt ook de blogpost delete


class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # link maken naar de andere table


print("run the script succesfull")

###
# routes
###

# need to use the decorator


@app.route(
    "/user", methods=["POST"]
)  # als een user in de url zit, dan wordt de create_user functie opgeroepen
def create_user():
    data = request.get_json() #de data dat in de post requset zit in de json tab
    # dit is de payload van de request
    new_user = User(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        adress=data["adress"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "user created"}), 200


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    users = (
        User.query.all()
    )  # ORM functie om alles in de User DB te queryen volgens ID -> standaard!
    print("users", users)
    all_users_ll = linked_listv3.LinkedList()

    for user in users:
        all_users_ll.insert_start(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "adress": user.adress,
            }
        )
        # deze functie zet de data om van een array naar een json file
    return jsonify(all_users_ll.to_list()), 200


@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    users = (
        User.query.all()
    )  # ORM functie om alles in de User DB te queryen volgens ID -> standaard!
    print("users", users)
    all_users_ll = linked_listv3.LinkedList()

    for user in users:
        all_users_ll.insert_end(  #
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "adress": user.adress,
            }
        )
        # deze functie zet de data om van een array naar een json file
    return jsonify(all_users_ll.to_list()), 200


@app.route(
    "/user/<user_id>", methods=["GET"]
)  # <user_id> is een variabele dat we uit de route gaan halen#
def get_one_user(user_id):
    users = User.query.all()
    print("users", users)
    all_users_ll = linked_listv3.LinkedList()

    for user in users:
        all_users_ll.insert_start(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "adress": user.adress,
            }
        )
    user = all_users_ll.get_user_by_id(user_id)
    print("user dictionary get by id: ",user)
    return jsonify(user),200


# <user_id> is een variabele dat we uit de route gaan halen
@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    # naast de user moet ook de blogpost die gelinked is ook verwijdert worden 
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"user {user_id} deleted"}), 200



@app.route("/blog_post/<user_id>", methods=["POST"])
def create_blog_post(user_id):

    ## getting the blog post data from the request
    data = request.get_json()
    user = User.query.filter_by(id=user_id).first()
    print(user)
    if not user:
        return jsonify({"message": "user not found"}),400
    ht = hashTable.Hash_Table(10)
    ht.add_key_value("title",data["title"])
    ht.add_key_value("body",data["body"])
    ht.add_key_value("date",now)
    ht.add_key_value("user_id",user_id)

    ## creating the blogpost in SQL
    new_blog_post = BlogPost(
        title=ht.get_value("title"),
        body=ht.get_value("body"),
        date=ht.get_value("date"),
        user_id = ht.get_value("user_id")
    )
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify({"message":"the blog post has been created"}),200

    

# binary search tree -> retrieve one blogpost based on its ID
@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_all_blog_posts(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)
    # als de query niet random is dan krijg je geen tree maar gewoon een lijst omdat de node altijd links ofwel altijd rechts zullen toegevoegd worden
    bst = binary_search_tree.BinarySearchTree()
    for post in blog_posts:
        #we voegen deze toe als dictionaries
        bst.insert({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "user_id":post.user_id

        })
    post = bst.search(blog_post_id) # returns the blogpost of the past blogpost ID
    # als de post niet bestaat krijg je een None
    if not post:
        return jsonify({"message:": "post not found"})
    return jsonify(post)

@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    pass


@app.route("/blog_post/<blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id):
    pass


# if we run this server.py file as our main application, then we are going to start our api with debug on True
# als we in de terminal python server.py runnen, dan gaat de interne variable __name__ gelijk zijn aan __main__
if __name__ == "__main__":
    app.run(debug=True)
