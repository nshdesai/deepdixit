#! usr/bin/env python

from pathlib import Path
import click
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from big_sleep import Imagine
import signal
from shutil import rmtree

@click.command()
@click.argument('prompt_file', type=click.Path(exists=True, resolve_path=True, path_type=Path))
@click.argument('output_dir', type=click.Path(resolve_path=True, path_type=Path))
def main(prompt_file, output_dir):
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

    imagine = Imagine(
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
        os.chdir(output_dir)

if __name__ == '__main__':
    main()