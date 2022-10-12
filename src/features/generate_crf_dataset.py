import click
import os
import csv
import string

INPUT_DIR_PATH = 'data/raw/indo4b'
OUTPUT_DIR_PATH = 'data/processed/crf'


@click.command()
@click.argument("filename", type=click.Path())
def main(filename):
    out_filename = "{}.csv".format(filename.split('.')[0])
    out_filepath = os.path.join(OUTPUT_DIR_PATH, out_filename)
    os.makedirs(os.path.dirname(out_filepath), exist_ok=True)

    out_file = open(out_filepath,
                    'w', newline='', encoding='utf8')
    out_writer = csv.writer(out_file)
    out_writer.writerow(["ID", "WORD", "TAG"])

    with open(os.path.join(INPUT_DIR_PATH, filename), "r", encoding='utf8') as f:
        for line in f:
            if (line.strip() == ""):
                continue
            sentence = line.strip().split()
            for i, word in enumerate(sentence):
                row = []
                # ID
                row.append(i + 1)

                word_no_punc = word
                for char in string.punctuation:
                    word_no_punc = word_no_punc.replace(char, '')
                # WORD
                row.append(word_no_punc)

                if ('.' in word):
                    row.append("PERIOD")
                elif (',' in word):
                    row.append("COMMA")
                elif ('?' in word):
                    row.append("QMARK")
                else:
                    row.append("NONE")

                out_writer.writerow(row)

    out_file.close()


if (__name__ == "__main__"):
    main()
