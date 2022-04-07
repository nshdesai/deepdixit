from app import database_loading

import os
import base64


def get_base64_string(image_path):
    with open(image_path, "rb") as image:
        return base64.b64encode(image.read())


subfolders = ['Clothing', 'Food', 'Home', 'Nature', 'Sport']

for subfolder in subfolders:
    images = os.listdir(f'Images/{subfolder}')
    images = [img for img in images if img.endswith('.best.png')]
    for img in images:
        image_string = get_base64_string(f'Images/{subfolder}/{img}')
        
        prompt = img.split('--')[0].replace('_', ' ')
        theme = subfolder
        print(theme, prompt)
        
        database_loading.write_image_to_db(prompt,
                                           image_string.decode('utf-8'),
                                           image_source='BigSleep',
                                           theme=theme)

images = os.listdir(f'Images/misc')
for img in images:
    image_string = get_base64_string(f'Images/misc/{img}')
    
    prompt = img.split('.')[0].replace('_', ' ')
    if 'siren' in prompt:
        prompt = prompt.split(' siren')[0]
        
    print(prompt)
    
    image_source = 'Siren' if 'siren' in img else 'BigSleep'
       
    database_loading.write_image_to_db(prompt,
                                       image_string.decode('utf-8'),
                                       image_source=image_source,
                                       theme='General')