# ---------------
# Imports
# ---------------

from flask import Flask, make_response, request, jsonify, render_template, url_for, redirect
import json, os
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy import types, desc
from dictalchemy import make_class_dictable
from urllib import quote_plus


# ---------------
# Init
# ---------------

app = Flask(__name__)

if os.getenv('DEBUG') == 'false':
  app.debug = False
else:
  app.debug = True

app.secret_key = "ukl\xab\xb7\xc9\x10\xf7\xf1\x03\x087\x0by\x88X'v\xc9\x8c\xc4\xc8\xfe+"

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
db = SQLAlchemy(app)
make_class_dictable(db.Model)

# -------------------
# Models
# -------------------

class Message(db.Model):
  '''
    A unique lovey-dove message
  '''
  # Columns
  id = db.Column(db.Integer(), primary_key=True)
  password = db.Column(db.Unicode())
  text = db.Column(db.Unicode())
  sender = db.Column(db.Unicode())
  receiver = db.Column(db.Unicode())
  phone = db.Column(db.Unicode())
  email = db.Column(db.Unicode())
  __table_args__ = ( db.UniqueConstraint('password'), { } )

  def __init__(self, password, text, sender, receiver, phone, email):
    self.password = password
    self.text = text
    self.sender = sender
    self.receiver = receiver
    self.phone = phone
    self.email = email

  def asdict(self):
    '''
      Returns the documentation as a dictionary
    '''
    doc_dict = db.Model.asdict(self)
    return doc_dict

  def __repr__(self):
    return "%s to %s at %s" % (self.sender, self.receiver, self.phone)


# -------------------
# Routes
# -------------------


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
  if request.method == 'POST':
    data = {
      'password': request.form['password'],
      'text': request.form['text'],
      'sender': request.form['sender'],
      'receiver': request.form['receiver'],
      'phone': request.form['phone'],
      'email': request.form['email']
    }
    new_message = Message(**data)
    db.session.add(new_message)
    db.session.commit()
    return 'Mensaje guardado con amor <3. Espera al 14 ;)'
  else:
    return 'un mensaje'

if __name__ == "__main__":
  app.run()
