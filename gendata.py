#! usr/bin/env python

from db.write import write_image_to_db

from pathlib import Path
import click
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from big_sleep import Imagine as bsImagine
from deep_daze import Imagine as ddImagine
import signal
from shutil import rmtree
import base64

def _get_base64_string(image_path):
    with open(image_path, "rb") as image:
        return base64.b64encode(image.read())


@click.group()
def generate():
    pass


@generate.command()
@click.argument('prompt_file', type=click.Path(exists=True, resolve_path=True, path_type=Path))
@click.argument('output_dir', type=click.Path(resolve_path=True, path_type=Path))
def deepdaze(prompt_file, output_dir):
    """
    Generate data for the prompt-response task.
    """
    print("Generating image/prompt data")
    print("-"*50)
    if output_dir.exists():
        overwrite=click.confirm("Output directory already exists. Erase and Overwrite?", default=False)
        if not overwrite:
            print("Exiting.")
            exit(1)
        else:
            print(f"Erasing and overwriting {output_dir}.")
            rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(output_dir)
    print(f'Generating data in {output_dir}...')

    df = pd.read_csv(prompt_file)

    for i, (prompt, cat) in tqdm(df.iterrows(), total=df.shape[0]):
        subdir = output_dir / cat
        subdir.mkdir(parents=True, exist_ok=True)
        os.chdir(subdir)

        imagine = ddImagine(
            text=prompt.lower(),
            open_folder=False,
            gradient_accumulate_every=4,
            epochs=2,
            save_progress=False,
            num_layers=42,
            batch_size=64,
            iterations=100
        )
        imagine()

        os.chdir(output_dir)


@generate.command()
@click.argument('prompt_file', type=click.Path(exists=True, resolve_path=True, path_type=Path))
@click.argument('output_dir', type=click.Path(resolve_path=True, path_type=Path))
def bigsleep(prompt_file, output_dir):
    """
    Generate data for the prompt-response task.
    """
    print("Generating image/prompt data")
    print("-"*50)
    if output_dir.exists():
        overwrite=click.confirm("Output directory already exists. Erase and Overwrite?", default=False)
        if not overwrite:
            print("Exiting.")
            exit(1)
        else:
            print(f"Erasing and overwriting {output_dir}.")
            rmtree(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(output_dir)
    print(f'Generating data in {output_dir}...')

    df = pd.read_csv(prompt_file)

    imagine = bsImagine(
        text_min="blur|zoom",
        open_folder=False,
        larger_clip=False,
        gradient_accumulate_every=3,
        epochs=1,
        save_best=True,
        iterations=100
    )

    for i, (prompt, cat) in tqdm(df.iterrows(), total=df.shape[0]):
        subdir = output_dir / cat
        subdir.mkdir(parents=True, exist_ok=True)
        os.chdir(subdir)
        imagine.reset()
        imagine.set_text(prompt.lower()  + "|" + cat.lower())
        imagine.img = prompt.lower() + ".png"
        imagine()
        image_string = _get_base64_string(imagine.text_path + ".best.png")
        write_image_to_db(
            prompt.lower(),
            image_string.decode('utf-8'),
            image_source='BigSleep',
            theme=cat.lower().replace(" ", "_")
            )
        os.chdir(output_dir)


if __name__ == '__main__':
    generate()
