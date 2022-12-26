import click
import os

OUTPUT_DIR_PATH = 'data/processed'

@click.command()
@click.argument('input_filename', type=click.Path(exists=True))
def main(input_filename):
    output_dir = os.path.split(input_filename)[-1].split('.')[0]
    output_dirpath = os.sep.join([OUTPUT_DIR_PATH, output_dir])

    os.makedirs(output_dirpath, exist_ok=True)
    fold_arr = []

    for i in range(5):
      fold_dirpath = os.sep.join([output_dirpath, f"fold_{i+1}"])
      os.makedirs(fold_dirpath, exist_ok=True)
      fold_arr.append([
        open(os.sep.join([fold_dirpath, 'train.txt']), 'w', encoding='utf8'),
        open(os.sep.join([fold_dirpath, 'val.txt']), 'w', encoding='utf8'),
      ])


    test_file = open(os.sep.join([output_dirpath, 'test.txt']), 'w', encoding='utf8')
    i = 0
    with open(input_filename, 'r', encoding='utf8') as f:
      for line in f:
        if i == 5:
          test_file.write(line)
          i = 0
        else:
          for idx, fold in enumerate(fold_arr):
            if (idx == i):
              fold[1].write(line)
            else:
              fold[0].write(line)
          i += 1

    test_file.close()

    for fold in fold_arr:
      fold[0].close()
      fold[1].close()


if (__name__ == "__main__"):
    main()