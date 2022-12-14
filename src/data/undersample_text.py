import click
import pandas as pd
import numpy as np
import string
from imblearn.under_sampling import RandomUnderSampler
import warnings
import os
warnings.simplefilter(action='ignore', category=FutureWarning)


def remove_punc(word):
    selected_punc = string.punctuation.translate(str.maketrans('', '', ",.?"))
    return word.translate(str.maketrans('', '', selected_punc))


def undersample_file(filepath):
    df = pd.DataFrame()

    with open(filepath, 'r', encoding='utf8') as f:
        for line in f:
            strip_line = line.strip()
            if (strip_line == ""):
                continue
            if (strip_line[-1] not in [".", "?"]):
                continue
            cleaned_line = remove_punc(strip_line)

            row = {'Text': cleaned_line}
            if (cleaned_line[-1] == '.'):
                row['Label'] = 'declarative'
            elif (cleaned_line[-1] == '?'):
                row['Label'] = 'question'
            df = df.append(row, ignore_index=True)

    print(df.head())
    print(df['Label'].value_counts())

    X = df.drop('Label', axis=1)
    y = df['Label']

    undersample = RandomUnderSampler(sampling_strategy='majority')
    X_res, y_res = undersample.fit_resample(X, y)

    print(y_res.value_counts())

    input_filename = os.path.split(filepath)[-1].split('.')[0]
    output_filepath = f"data/interim/indo4b/{input_filename}_undersampled.txt"

    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    np.savetxt(output_filepath, X_res.values, fmt='%s')


@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
def main(input_dir):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith('.txt'):
                files.append(os.sep.join([dirpath, filename]))
    for file in files:
        print(file)
        undersample_file(file)


if (__name__ == "__main__"):
    main()
