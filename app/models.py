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

    prompt_id = db.Column(db.Integer, db.ForeignKey('prompts.id'), primary_key=True)
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'), primary_key=True)
