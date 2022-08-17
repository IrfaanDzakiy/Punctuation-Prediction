import os
import click


@click.command()
@click.argument('directory_path', type=click.Path(exists=True))
def main(directory_path):
    for filename in os.listdir(directory_path):
        with open(os.path.join(directory_path, filename), 'r', encoding='utf8') as f:
            print(f'filename: {filename}')

            count = 1
            while count < 6:
                line = f.readline()
                if (line != '\n'):
                    print(f'line {count}: {line}')
                    count += 1


if (__name__ == '__main__'):
    main()
