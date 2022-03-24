import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from dotenv import load_dotenv
from app.models import *

load_dotenv()
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
print(f'DEBUG: {os.environ.get("DATABASE_URL")}')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    db.create_all()
    return str(app.config['SQLALCHEMY_DATABASE_URI'])

@app.route('/image')
def image():
    img = ImageSource.query.get(1)
    print(img.source[:100])
    return f'<img src="data:image/png;base64, {img.source}">'

@app.route('/random-image')
def random_image():
    img = Image.query.order_by(func.random()).first()
    return {
        "image": ImageSource.query.get(img.source_id).source,
        "prompt_id": img.prompt_id
    }

@app.route('/prompt/<int:prompt_id>')
def prompt(prompt_id):
    prompt = Prompt.query.get(prompt_id)
    return {"prompt": prompt.prompt}