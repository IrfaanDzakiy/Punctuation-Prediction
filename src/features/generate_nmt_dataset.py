import click
import os
import string

INPUT_DIR_PATH = 'data/raw/indo4b'
OUTPUT_DIR_PATH = 'data/processed/nmt'

def remove_punc(word):
    return word.translate(str.maketrans('', '', string.punctuation))

@click.command()
@click.argument("input_file", type=click.Path(exists=True))
def main(input_file):
    _, filename = os.path.split(input_file)
    src_filepath = os.sep.join([OUTPUT_DIR_PATH, f"src-{filename}"])
    tgt_filepath = os.sep.join([OUTPUT_DIR_PATH, f"tgt-{filename}"])

    os.makedirs(os.path.dirname(src_filepath), exist_ok=True)
    os.makedirs(os.path.dirname(tgt_filepath), exist_ok=True)
    src_file = open(src_filepath, 'w', encoding='utf8')
    tgt_file = open(tgt_filepath, 'w', encoding='utf8')

    with open(input_file, 'r', encoding='utf8') as f:
        for line in f:
            src_file.write(f"{remove_punc(line).strip()}\n")
            tgt_file.write(line)

    src_file.close()
    tgt_file.close()


if (__name__ == "__main__"):
    main()
