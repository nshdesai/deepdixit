#! usr/bin/env python

from pathlib import Path
import click
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from big_sleep import Imagine
import signal

# terminate = False

# def signal_handler(sig, frame):
#     global terminate
#     terminate = True

# signal.signal(signal.SIGINT, signal_handler)


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
    
    output_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(output_dir)
    print(f'Generating data in {output_dir}...')

    df = pd.read_csv(prompt_file)
    for i, (prompt, cat) in tqdm(df.iterrows(), total=df.shape[0]):
        imagine = Imagine(
            text=prompt,
            text_min='blur|'
            open_folder=False,
            gradient_accumulate_every=3,
            epochs=2,
            save_best=True, 
            iterations=100
        )
        imagine()
        # if terminate:
        #     print("Gracefully exiting.")
        #     return 
        # print(prompt)


if __name__ == '__main__':
    main()