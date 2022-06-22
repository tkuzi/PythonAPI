from flask import Flask,jsonify, request
from datetime import datetime
# standaard lib dat meekomt met python
from sqlite3 import Connection as SQLite3Connection
# ORM wrappper voor SQL en flask
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
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQL_TRACK_MODIFICATIONS"] = 0

#config sqlite om de foreign key constraints te editten -> dan kan je tabellen met elkaar joinen dmv de primary key
# om de db connnectie te configureren voor foreign keys te gebruiken -> niet leren !!!!!
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")


###
# models
###

# De ORM zorgt voor simpelere modellen

class User(db.model):
    __tablename__ = "user"