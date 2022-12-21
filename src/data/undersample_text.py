import click
import pandas as pd
import numpy as np
import string
from imblearn.under_sampling import RandomUnderSampler
import warnings
import os
warnings.simplefilter(action='ignore', category=FutureWarning)

Q_TARGET_COUNT = {
    "bppt": 171,
    "conllu_all_uncased": 2583127,
    "frog_storytelling": 21,
    "jw300": 74215,
    "kompas": 2130,
    "opensubtitles": 4040026,
    "oscar_all_uncased": 4868458,
    "parallel_corpus": 254,
    "talpco_indonesia": 68,
    "tempo": 2318,
    "wiki": 9749,
    "wikipedia_conllu": 19125
}

def remove_punc(word):
    selected_punc = string.punctuation.translate(str.maketrans('', '', ",.?"))
    return word.translate(str.maketrans('', '', selected_punc))


def undersample_file(filepath):
    input_filename = os.path.split(filepath)[-1].split('.')[0]
    output_filepath = f"data/interim/indo4b/{input_filename}_undersampled.txt"

    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    output_file = open(output_filepath, 'w', encoding='utf8')

    with open(filepath, 'r', encoding='utf8') as f:
        dec_count = 0
        ques_count = 0
        for line in f:
            strip_line = line.strip()
            if (strip_line == ""):
                continue
            if (strip_line[-1] not in [".", "?"]):
                continue
            cleaned_line = remove_punc(strip_line)
            if (cleaned_line[-1] == '.' and dec_count < Q_TARGET_COUNT[input_filename]):
                dec_count += 1
                output_file.write(f"{cleaned_line}\n")
            elif (cleaned_line[-1] == '?'):
                ques_count += 1
                output_file.write(f"{cleaned_line}\n")

    output_file.close()

@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
def main(input_dir):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith('.txt'):
                files.append(os.sep.join([dirpath, filename]))
    # for file in files:
    #     print(file)
    undersample_file("data/raw/indo4b/bppt.txt")


if (__name__ == "__main__"):
    main()
