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

    cache_size = 10

    body = request.get_json()
    nextImgIds = body['nextImgIds']

    beatles_prompt_ids = PromptTheme.query.filter(PromptTheme.theme_id == 7).with_entities(PromptTheme.prompt_id)

    if len(nextImgIds) == 0:
        nextImgIds = [x.id for x in Image.query.filter(Image.prompt_id.not_in(beatles_prompt_ids)).order_by(func.random()).limit(cache_size).all()]
        print(nextImgIds)
    elif len(nextImgIds) < cache_size:
        while len(nextImgIds) < cache_size:
            next_img = Image.query.filter(Image.prompt_id.not_in(beatles_prompt_ids)).order_by(func.random()).order_by(func.random()).first()
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

    img_theme_id = PromptTheme.query.filter(PromptTheme.prompt_id == actual_prompt_id).first().theme_id
    promtps_same_theme = PromptTheme.query.filter(PromptTheme.theme_id == img_theme_id).with_entities(PromptTheme.prompt_id)

    fake_prompts = Prompt.query.filter(Prompt.id != actual_prompt_id).filter(Prompt.id.in_(promtps_same_theme)).order_by(func.random()).all()
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
