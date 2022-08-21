import click
import os

INPUT_DIR_PATH = 'data/raw/indo4b'
OUTPUT_DIR_PATH = 'data/interim'


@click.command()
@click.argument('output_filename', type=click.Path())
def main(output_filename):
    output_lines = []
    for filename in os.listdir(INPUT_DIR_PATH):
        output_lines.append(f'Filename : {filename}\n')
        period_count = 0
        comma_count = 0
        qmark_count = 0
        line_count = 0
        with open(os.path.join(INPUT_DIR_PATH, filename), 'r', encoding='utf8') as f:
            for line in f:
                if line == '\n':
                    continue
                period_count += line.count('.')
                comma_count += line.count(',')
                qmark_count += line.count('?')
                line_count += 1

            output_lines.append(f'Sentence count : {line_count}\n')
            output_lines.append(f'Period count : {period_count}\n')
            output_lines.append(
                f'Period per line: {round(period_count / line_count, 4)}\n')
            output_lines.append(f'Comma count : {comma_count}\n')
            output_lines.append(
                f'Comma per line: {round(comma_count / line_count, 4)}\n')
            output_lines.append(f'Question mark count : {qmark_count}\n')
            output_lines.append(
                f'Question mark per line: {round(qmark_count / line_count, 4)}\n')

        output_lines.append('\n')
        print(f'{filename} finished')

    output_file = open(os.path.join(OUTPUT_DIR_PATH, output_filename), 'w')
    output_file.writelines(output_lines)
    output_file.close()


if (__name__ == '__main__'):
    main()
