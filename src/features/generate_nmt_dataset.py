import click
import os
import re
import string

INPUT_DIR_PATH = 'data/raw/indo4b'
OUTPUT_DIR_PATH = 'data/processed/nmt'


@click.command()
@click.argument("filename", type=click.Path())
def main(filename):
    out_foldername = filename.split('.')[0]
    out_path = os.path.join(OUTPUT_DIR_PATH, out_foldername)

    # os.makedirs(out_path)
    src_train_file = open(os.path.join(
        out_path, "src-train.txt"), 'w', encoding='utf8')
    tgt_train_file = open(os.path.join(
        out_path, "tgt-train.txt"), 'w', encoding='utf8')
    src_val_file = open(os.path.join(
        out_path, "src-val.txt"), 'w', encoding='utf8')
    tgt_val_file = open(os.path.join(
        out_path, "tgt-val.txt"), 'w', encoding='utf8')
    src_test_file = open(os.path.join(
        out_path, "src_test.txt"), 'w', encoding='utf8')

    with open(os.path.join(INPUT_DIR_PATH, filename), "r", encoding='utf8') as f:
        train_count = 0
        val_count = 0
        test_count = 0

        while train_count < 10000:
            line = f.readline()
            if (line == '\n'):
                continue
            tgt_train_file.write(line)
            line_word_only = line
            for char in string.punctuation:
                line_word_only = line_word_only.replace(char, '')
            src_train_file.write(line_word_only)
            train_count += 1

        while val_count < 1000:
            line = f.readline()
            if (line == '\n'):
                continue
            tgt_val_file.write(line)
            line_word_only = line
            for char in string.punctuation:
                line_word_only = line_word_only.replace(char, '')
            src_val_file.write(line_word_only)
            val_count += 1

        while test_count < 1000:
            line = f.readline()
            if (line == '\n'):
                continue
            line_word_only = line
            for char in string.punctuation:
                line_word_only = line_word_only.replace(char, '')
            src_test_file.write(line_word_only)
            test_count += 1

    src_train_file.close()
    tgt_train_file.close()
    src_val_file.close()
    tgt_val_file.close()
    src_test_file.close()


if (__name__ == "__main__"):
    main()
