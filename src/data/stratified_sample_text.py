import click
import os
import random

OUTPUT_DIR_PATH = 'data/interim/sampled'

def stratified_sample_file(input_filename, output_file, percentage):
    with open(input_filename, 'r', encoding='utf8') as f:
      linecount = sum(1 for line in f)
      samplecount = (linecount * percentage) // 100
      f.seek(0)

      random_linenos = sorted(random.sample(range(linecount), samplecount), reverse = True)
      lineno = random_linenos.pop()
      for n, line in enumerate(f):
        if n == lineno:
          output_file.write(line)
          if len(random_linenos) > 0:
            lineno = random_linenos.pop()
          else:
            break

@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('output_filename', type=click.Path())
@click.argument('percentage', type=int)
def main(input_dir, output_filename, percentage):
    files = []
    output_filepath = os.sep.join([OUTPUT_DIR_PATH, output_filename])
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

    output_file = open(output_filepath, 'w', encoding='utf8')
    
    for (dirpath, dirnames, filenames) in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith('.txt'):
                files.append(os.sep.join([dirpath, filename]))
    i = 0
    for file in files:
        print(file)
        stratified_sample_file(file, output_file, int(percentage))

    output_file.close()

if (__name__ == "__main__"):
    main()