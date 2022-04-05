"""
Some questions:

Is the API fine? I'm accepting the images as a pre-encoded string right now...
There might be a lot of redundant queries, since we're using the same themes + image_sources repeatedly... Maybe we should memoize?
I think we should rename the source column in the FakePrompt table to source_id, to be consistent with the Image table.
Should I expose the session in this way? Where should I put the link to avoid hard-coding it in?
We might want to use session.fetch() instead of commit() in some/all places, not sure about this...
Should this file even be in app/?
"""

from models import *

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(os.environ.get('DATABASE_URL'))
session = sessionmaker(bind=engine)()


def write_record_to_db(prompt : str, fake_prompts : list, image : str, image_source : str, fake_prompt_source : str, theme : str = 'General', theme_description : str = None):
    image_id = write_image_to_db(prompt, image, image_source, theme, theme_description)
    for fp in fake_prompts:
        write_fake_prompt_to_db(fp, image_id, fake_prompt_source)


def write_image_to_db(prompt : str, image : str, image_source : str, theme : str = 'General', theme_description : str = None) -> int:
    """
    prompt: The prompt used to generate the image, as a string
    image: base64 encoded string of image
    image_source: The tag for what we used to generate the image e.g. 'DeepDaze v1.0'
    theme: The prompt theme, as a string
    theme_description: The description for the theme, as a string
    
    Return identifier for newly inserted image.
    """
    prompt_entry = Prompt(prompt = prompt)
    prompt_id = insert_if_new_and_get_id(Prompt, 'prompt', prompt_entry, 'id')
    
    theme_entry = Theme(theme_name = theme, description = theme_description)
    theme_id = insert_if_new_and_get_id(Theme, 'theme_name', theme_entry, 'id')
    
    prompt_theme_entry = PromptTheme(prompt_id = prompt_id, theme_id = theme_id)
    session.add(prompt_theme_entry)
    session.commit()
    
    image_source_entry = ImageSource(source = image_source)
    image_source_id = insert_if_new_and_get_id(ImageSource, 'source', image_source_entry, 'id')
    
    image_entry = Image(prompt_id = prompt_id, source_id = image_source_id, image = image)
    session.add(prompt_theme_entry)
    session.commit()
    
    return image_entry.id
    

def write_fake_prompt_to_db(fake_prompt : str, image_id : int, fake_prompt_source : str) -> int:
    """
    fake_prompt: The generated fake prompt, as a string
    image_id: Database identified for the image associated with the fake prompt
    fake_prompt_source: The tag for what we used to generate the image e.g. 'Manual'
    
    Return identifier for newly inserted fake prompt.
    """
    fake_prompt_source_entry = FakePromptSource(source = image_source)
    fake_prompt_source_id = insert_if_new_and_get_id(FakePromptSource, 'source', fake_prompt_source_entry, 'id')
    
    fake_prompt_entry = FakePrompt(image_id = image_id, source = fake_prompt_source_id, fake_prompt = fake_prompt)
    session.add(fake_prompt_entry)
    session.commit()
    
    return fake_prompt_entry.id


def insert_if_new_and_get_id(table, col_to_match, item, id_col):
    """
    Return the id_col value of the first entry in table where the value of col_to_match matches item.col_to_match.
    If no such entry exists, insert item into table and return the new id.
    """
    old_entry = session.query(table).filter_by(**{col_to_match : getattr(item, col_to_match)}).first()
    if old_entry is not None:
        return getattr(old_entry, id_col)
    else: # Add to table first
        session.add(item)
        session.commit()
        retirn getattr(item, id_col)
