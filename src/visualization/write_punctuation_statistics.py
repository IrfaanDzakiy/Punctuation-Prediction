import click
import os
import string

INPUT_DIR_PATH = 'data/raw/indo4b'
OUTPUT_DIR_PATH = 'data/interim'


def count(l1, l2): return sum([1 for x in l1 if x in l2])


@click.command()
@click.argument('output_filename', type=click.Path())
def main(output_filename):
    output_lines = []
    for filename in os.listdir(INPUT_DIR_PATH):
        output_lines.append(f'Filename : {filename}\n')
        period_count = 0
        comma_count = 0
        qmark_count = 0
        emark_count = 0
        punct_count = 0
        line_count = 0
        word_count = 0
        qsentence_count = 0
        dsentence_count = 0
        isentence_count = 0
        with open(os.path.join(INPUT_DIR_PATH, filename), 'r', encoding='utf8') as f:
            for line in f:
                line = line.strip()
                if line == '':
                    continue
                period_count += line.count('.')
                comma_count += line.count(',')
                qmark_count += line.count('?')
                emark_count += line.count('!')
                punct_count += count(line, set(string.punctuation))
                word_count += len(line.split())
                line_count += 1
                if ('.' in line):
                    dsentence_count += 1
                if ('?' in line):
                    qsentence_count += 1
                if ('!' in line):
                    isentence_count += 1

            output_lines.append(f'Sentence count : {line_count}\n')
            output_lines.append(f'Word count : {word_count}\n')
            output_lines.append(
                f'Word per sentence : {round(word_count / line_count, 4)}\n')
            output_lines.append(
                f'Declarative sentence count : {dsentence_count}\n')
            output_lines.append(
                f'Declarative sentence percentage : {round(dsentence_count * 100 / line_count, 4)}\n')
            output_lines.append(
                f'Question sentence count : {qsentence_count}\n')
            output_lines.append(
                f'Question sentence percentage : {round(qsentence_count * 100 / line_count, 4)}\n')
            output_lines.append(
                f'Imperative sentence count : {isentence_count}\n')
            output_lines.append(
                f'Imperative sentence percentage : {round(isentence_count * 100 / line_count, 4)}\n')
            output_lines.append(f'Punctuation count : {punct_count}\n')
            output_lines.append(f'Period count : {period_count}\n')
            output_lines.append(f'Comma count : {comma_count}\n')
            output_lines.append(f'Question mark count : {qmark_count}\n')
            output_lines.append(f'Exclamation mark count : {emark_count}\n')

        output_lines.append('\n')
        print(f'{filename} finished')

    output_file = open(os.path.join(OUTPUT_DIR_PATH, output_filename), 'w')
    output_file.writelines(output_lines)
    output_file.close()


if (__name__ == '__main__'):
    main()
