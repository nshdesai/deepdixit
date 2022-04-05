from click import prompt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Prompt(db.Model):
    __tablename__ = 'prompts'

    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.String)

class Theme(db.Model):
    __tablename__ = 'theme'

    id = db.Column(db.Integer, primary_key=True)
    theme_name = db.Column(db.String)
    description = db.Column(db.String)

class PromptTheme(db.Model):
    __tablename__ = 'promptTheme'

    prompt_id = db.Column(db.Integer, db.ForeignKey(Prompt.id), primary_key=True)
    theme_id = db.Column(db.Integer, db.ForeignKey(Theme.id), primary_key=True)

class ImageSource(db.Model):
    __tablename__ = 'imageSource'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String)

class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    prompt_id = db.Column(db.Integer, db.ForeignKey(Prompt.id))
    source_id = db.Column(db.Integer, db.ForeignKey(ImageSource.id))
    image = db.Column(db.String)

class FakePromptSource(db.Model):
    __tablename__ = 'fakePromptSource'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String)

class FakePrompt(db.Model):
    __tablename__ = 'fakePrompt'

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey(Image.id))
    source_id = db.Column(db.Integer, db.ForeignKey(FakePromptSource.id))
    fake_prompt = db.Column(db.String)

class Play(db.Model):
    __tablename__ = 'play'

    id = db.Column(db.Integer, primary_key=True)
    multiple_choice = db.Column(db.Boolean)
    theme = db.Column(db.Integer, db.ForeignKey(Theme.id))
    image = db.Column(db.Integer, db.ForeignKey(Image.id))

class MultipleChoiceOption(db.Model):
    __tablename__ = 'multipleChoiceOption'

    play_id = db.Column(db.Integer, db.ForeignKey(Play.id), primary_key=True)
    fake_prompt_id = db.Column(db.Integer, db.ForeignKey(FakePrompt.id), primary_key=True)
    selected = db.Column(db.Boolean)

class PlayerInput(db.Model):
    __tablename__ = 'playerInput'

    play_id = db.Column(db.Integer, db.ForeignKey(Play.id), primary_key=True)
    prompt_id = db.Column(db.Integer, db.ForeignKey(Prompt.id))
    score = db.Column(db.Float)
