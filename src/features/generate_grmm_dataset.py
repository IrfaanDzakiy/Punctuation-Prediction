import click
import os
import string

INPUT_DIR_PATH = 'data/raw/indo4b'
OUTPUT_DIR_PATH = 'data/processed/grmm'


def remove_punc(word):
    return word.translate(str.maketrans('', '', string.punctuation))


def word2word_tag(word):
    if ('.' in word):
        return "PERIOD"
    elif (',' in word):
        return "COMMA"
    elif ('?' in word):
        return "QMARK"
    else:
        return "NONE"


def word2sentence_tag(i, sentence):
    sentence_type = ""
    if ('.' in sentence[-1]):
        sentence_type = "DE"  # Declarative sentence
    elif ('?' in sentence[-1]):
        sentence_type = "QN"  # Question sentence

    sentence_part = ""
    if (i == 0):
        sentence_part = "BEG"  # Beginning of sentence
    else:
        sentence_part = "IN"  # In the sentence

    return sentence_type + sentence_part


def word2features(i, sent):
    word_range = 5

    # Unigram
    features = {
        '0': remove_punc(sent[i])
    }
    for j in range(1, word_range + 1):
        if (i - j >= 0):
            features["-{}".format(j)] = remove_punc(sent[i - j])
        else:
            features["-{}".format(j)] = "<START{}>".format(j - i - 1)

        if (i + j < len(sent)):
            features["{}".format(j)] = remove_punc(sent[i + j])
        else:
            features["{}".format(j)] = "<END{}>".format(i + j - len(sent))

    # Bigram and Trigram
    unigram_items = sorted(list(features.items()),
                           key=lambda item: int(item[0]))
    unigram_length = len(unigram_items)
    for idx, (k, v) in enumerate(unigram_items):
        if (idx + 1 < unigram_length):
            first_item_k = unigram_items[idx + 1][0]
            first_item_v = str(unigram_items[idx + 1][1])
            features["[{},{}]".format(k, first_item_k)
                     ] = "+".join([str(v), first_item_v])

            if (idx + 2 < unigram_length):
                second_item_k = unigram_items[idx + 2][0]
                second_item_v = str(unigram_items[idx + 2][1])
                features["[{},{}]".format(
                    k, second_item_k)] = "+".join([str(v), first_item_v, second_item_v])

    return map(lambda x: x[1] + '@' + x[0], list(features.items()))


@click.command()
@click.argument("filename", type=click.Path())
def main(filename):
    out_filename = "{}_grmm.txt".format(filename.split('.')[0])
    out_filepath = os.path.join(OUTPUT_DIR_PATH, out_filename)
    os.makedirs(os.path.dirname(out_filepath), exist_ok=True)

    out_file = open(out_filepath,
                    'w', newline='', encoding='utf8')
    with open(os.path.join(INPUT_DIR_PATH, filename), "r", encoding='utf8') as f:
        for line in f:
            if (line.strip() == ""):
                continue
            sentence = line.strip().split()
            sentence_punc_concat = []

            for word in sentence:
                if (len(sentence_punc_concat) == 0):
                    sentence_punc_concat.append(word)
                elif (word not in string.punctuation):
                    sentence_punc_concat.append(word)
                else:  # Punctuation splitted with space
                    sentence_punc_concat[-1] += word
            for i, word in enumerate(sentence_punc_concat):
                out_line = []
                out_line.append(word2word_tag(word))
                out_line.append(word2sentence_tag(i, sentence_punc_concat))
                out_line.append("----")
                out_line += word2features(i, sentence_punc_concat)

                out_file.write(" ".join(out_line))
                out_file.write('\n')

            out_file.write('\n')

    out_file.close()


if (__name__ == "__main__"):
    main()
