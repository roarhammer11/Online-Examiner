from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os 

#region Instantiate
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/'
db = SQLAlchemy(app)
app.secret_key = os.urandom(24)
#endregion

from app import routes

