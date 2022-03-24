import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from dotenv import load_dotenv
import random
from app.models import *

load_dotenv()
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})
print(f'DEBUG: {os.environ.get("DATABASE_URI")}')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
db.init_app(app)


@app.route('/')
def index():
    db.create_all()
    return "Hello, World!"


@app.route('/image')
def image():
    img = ImageSource.query.get(1)
    print(img.source[:100])
    return f'<img src="data:image/png;base64, {img.source}">'


@app.route('/random-image')
def random_image():
    img = Image.query.order_by(func.random()).first()

    prompt_ids = []

    actual_prompt_id = img.prompt_id
    actual_prompt = Prompt.query.get(actual_prompt_id).prompt

    prompt_ids += [{
        'id': actual_prompt_id,
        'prompt': actual_prompt,
        'real': True
    }]

    fake_prompts = FakePrompt.query.filter_by(image_id=img.id).all()
    select_random = random.sample(fake_prompts, 3)

    for i in range(len(select_random)):
        prompt_ids += [{
            'id': select_random[i].id,
            'prompt': select_random[i].fake_prompt,
            'real': False
        }]

    response = jsonify({
        "image": ImageSource.query.get(img.source_id).source.rstrip(),
        "prompts": prompt_ids
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/prompt/<int:prompt_id>')
def prompt(prompt_id):
    prompt = Prompt.query.get(prompt_id)
    return {"prompt": prompt.prompt}
