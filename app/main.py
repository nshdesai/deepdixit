import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db.init_app(app)

@app.route('/')
def index():
    db.create_all()
    prompt = Prompt(prompt='What is your favorite color?')
    db.session.add(prompt)
    db.session.commit()
    return str(app.config['SQLALCHEMY_DATABASE_URI'])