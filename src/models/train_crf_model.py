import click
import os
import math
import pandas as pd
import sklearn_crfsuite

from sklearn.model_selection import train_test_split
from sklearn_crfsuite import metrics


INPUT_DIR_PATH = 'data/processed/crf'


def word2features(sent, i):
    word_range = 5

    # Unigram
    features = {
        'C0': sent[i][0]
    }
    for j in range(1, word_range + 1):
        if (i - j >= 0):
            features["C-{}".format(j)] = sent[i - j][0]
        if (i + j < len(sent)):
            features["C{}".format(j)] = sent[i + j][0]

    # Bigram and Trigram
    unigram_items = list(features.items())
    unigram_length = len(unigram_items)
    for idx, (k, v) in enumerate(unigram_items):
        if (idx + 1 < unigram_length):
            first_item_k = unigram_items[idx + 1][0]
            first_item_v = str(unigram_items[idx + 1][1])
            features[k + first_item_k] = " ".join([str(v), first_item_v])

            if (idx + 2 < unigram_length):
                second_item_k = unigram_items[idx + 2][0]
                second_item_v = str(unigram_items[idx + 2][1])
                features[k + first_item_k +
                         second_item_k] = " ".join([str(v), first_item_v, second_item_v])

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [word[1] for word in sent]


def format_data(csv_data):
    sents = []
    for i in range(len(csv_data)):
        if math.isnan(csv_data.iloc[i, 0]):
            continue
        elif csv_data.iloc[i, 0] == 1.0:
            sents.append([[csv_data.iloc[i, 1], csv_data.iloc[i, 2]]])
        else:
            sents[-1].append([csv_data.iloc[i, 1], csv_data.iloc[i, 2]])
    for sent in sents:
        for i, word in enumerate(sent):
            if type(word[0]) != str:
                del sent[i]
    return sents


@click.command()
@click.argument("filename", type=click.Path())
def main(filename):
    data = pd.read_csv(os.path.join(INPUT_DIR_PATH, filename))

    print(data)

    sents = format_data(data)

    X = [sent2features(s) for s in sents]
    y = [sent2labels(s) for s in sents]

    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.2)

    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.25,
        c2=0.3,
        max_iterations=100,
        all_possible_transitions=True
    )
    crf.fit(Xtrain, ytrain)

    labels = ['NONE', 'COMMA', 'PERIOD', 'QMARK']

    ypred = crf.predict(Xtrain)
    print('F1 score on the train set = {}\n'.format(
        metrics.flat_f1_score(ytrain, ypred, average='weighted', labels=labels)))
    print('Accuracy on the train set = {}\n'.format(
        metrics.flat_accuracy_score(ytrain, ypred)))

    sorted_labels = sorted(
        labels,
        key=lambda name: (name[1:], name[0])
    )
    print('Train set classification report: \n\n{}'.format(metrics.flat_classification_report(
        ytrain, ypred, labels=sorted_labels, digits=3
    )))

    # obtaining metrics such as accuracy, etc. on the test set
    ypred = crf.predict(Xtest)
    print('F1 score on the test set = {}\n'.format(metrics.flat_f1_score(ytest, ypred,
                                                                         average='weighted', labels=labels)))
    print('Accuracy on the test set = {}\n'.format(
        metrics.flat_accuracy_score(ytest, ypred)))

    sorted_labels = sorted(
        labels,
        key=lambda name: (name[1:], name[0])
    )
    print('Test set classification report: \n\n{}'.format(
        metrics.flat_classification_report(ytest, ypred, labels=sorted_labels, digits=3)))


if (__name__ == "__main__"):
    main()
