import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from dotenv import load_dotenv
import random
from app.models import *

load_dotenv()
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
CORS(app)

print(f'DEBUG: {os.environ.get("DATABASE_URI")}')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def index():
    db.create_all()
    return "Hello, World!"


@app.route('/random-image', methods=['POST'])
def random_image():

    cache_size = 3

    body = request.get_json()
    nextImgIds = body['nextImgIds']
    if len(nextImgIds) == 0:
        nextImgIds = [x.id for x in Image.query.order_by(func.random()).limit(cache_size).all()]
        print(nextImgIds)
    elif len(nextImgIds) < cache_size:
        while len(nextImgIds) < cache_size:
            next_img = Image.query.order_by(func.random()).first()
            if next_img.id not in nextImgIds:
                nextImgIds.append(next_img.id)
        print(nextImgIds)
    img = Image.query.get(nextImgIds.pop(0))    

    prompt_ids = []

    actual_prompt_id = img.prompt_id
    actual_prompt = Prompt.query.get(actual_prompt_id).prompt

    prompt_ids += [{
        'id': actual_prompt_id,
        'prompt': actual_prompt,
        'real': True
    }]

    fake_prompts = Prompt.query.filter(Prompt.id != actual_prompt_id).all()
    select_random = random.sample(fake_prompts, 3)

    for i in range(len(select_random)):
        prompt_ids += [{
            'id': select_random[i].id,
            'prompt': select_random[i].prompt,
            'real': False
        }]

    response = jsonify({
        "image": img.image.rstrip(),
        "prompts": prompt_ids,
        "nextImgIds": nextImgIds
    })
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response
