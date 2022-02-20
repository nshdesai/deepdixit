from click import prompt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Prompt(db.Model):
    __tablename__ = 'prompts'

    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String)

class Theme(db.Model):
    __tablename__ = 'themes'

    id = db.Column(db.Integer, primary_key=True)
    theme_name = db.Column(db.String)
    description = db.Column(db.String)

class PromptTheme(db.Model):
    __tablename__ = 'promptThemes'

    prompt_id = db.Column(db.Integer, db.ForeignKey(Prompt.id), primary_key=True)
    theme_id = db.Column(db.Integer, db.ForeignKey(Theme.id), primary_key=True)

class ImageSource(db.Model):
    __tablename__ = 'imageSources'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String)

class Image(db.Model):
    __tableame__ = 'images'

    id = db.Column(db.Integer, primary_key=True)
    prompt_id = db.Column(db.Integer, db.ForeignKey(Prompt.id))
    source_id = db.Column(db.Integer, db.ForeignKey(ImageSource.id))

class FakePromptSource(db.Model):
    __tablename__ = 'fakePromptSources'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String)

class FakePrompt(db.Model):
    __tablename__ = 'fakePrompts'

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    source = db.Column(db.Integer, db.ForeignKey(FakePromptSource.id))
    fake_prompt = db.Column(db.String)

class Play(db.Model):
    __tablename__ = 'plays'

    id = db.Column(db.Integer, primary_key=True)
    multiple_choice = db.Column(db.Boolean)
    theme = db.Column(db.Integer, db.ForeignKey(Theme.id))
    image = db.Column(db.Integer, db.ForeignKey(Image.id))

class MultipleChoiceOption(db.Model):
    __tablename__ = 'multipleChoiceOptions'

    play_id = db.Column(db.Integer, db.ForeignKey(Play.id), primary_key=True) # should this be primary?
    fake_prompt_id = db.Column(db.Integer, db.ForeignKey(FakePrompt.id), primary_key=True) # should this be primary?
    selected = db.Column(db.Boolean)

class PlayerInput(db.Model):
    __tablename__ = 'playerInputs'

    play_id = db.Column(db.Integer, db.ForeignKey(Play.id), primary_key=True) # should this be primary?
    prompt_id = db.Column(db.Integer, db.ForeignKey(Prompt.id), primary_key=True) # should this be primary?
    score = db.Column(db.Float)
