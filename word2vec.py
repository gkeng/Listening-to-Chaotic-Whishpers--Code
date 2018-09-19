from keras.layers import Embedding, merge
from keras.engine import Input
from keras.models import Model
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import os
import json
import numpy as np

tokenize = lambda x: simple_preprocess(x)

"""
    Ce programme n'a pas été utilisé, après les premiers tests nous avons choisis doc2vec qui donne des
    meilleurs résultats
"""


class SentenceGenerator(object):

    """
    Class qui permet tokeniser les lignes en créant un itérateur
    """

    def __init__(self, dirname):

        """
        Constructeur
        :param dirname: nom du répertoire
        """
        self.dirname = dirname

    def __iter__(self):

        """
        Itérateur
        :return:
        """

        i = 0
        for newspaper in os.listdir(self.dirname):
            days = os.path.join(self.dirname, newspaper)
            for day in os.listdir(days):
                day_path = os.path.join(days, day)
                for fname in os.listdir(day_path):
                    f_path = os.path.join(day_path, fname)
                    print(f_path)
                    print(i)
                    i += 1
                    for line in open(f_path, 'rb'):
                        yield tokenize(line)


def create_embeddings(data_dir, embeddings_path, vocab_path, **params):

    """

    :param data_dir: répertoire de travail
    :param embeddings_path: répertoire poids de chaque mot
    :param vocab_path: répertoire du vocabulaire
    :param params:
    :return:
    """

    sentences = SentenceGenerator(data_dir)

    # Pour chaque phrase d'un article on attribue un poids à chaque mot
    model = Word2Vec(sentences, **params)
    # poids de chaque mot
    weights = model.wv.syn0
    np.save(open(embeddings_path, 'wb'), weights)

    # vocabulaire disponnible
    vocab = dict([(k, v.index) for k, v in model.wv.vocab.items()])
    with open(vocab_path, 'w') as f:
        f.write(json.dumps(vocab))


def load_vocab(vocab_path):
    """
    Vocabulaire disponnible après le train sur les articles
    :param vocab_path:
    :return:
    """
    with open(vocab_path, 'r') as f:
        data = json.loads(f.read())
    word2idx = data
    idx2word = dict([(v, k) for k, v in data.items()])
    return word2idx, idx2word


def word2vec_embedding_layer(embeddings_path):
    """
    permet d'associer l'indice du mot à son poids
    :param embeddings_path:
    :return:
    """
    weights = np.load(open(embeddings_path, 'rb'))
    layer = Embedding(input_dim=weights.shape[0], output_dim=weights.shape[1], weights=[weights])
    return layer


if __name__ == '__main__':

    data_path = ['text_data/',
                 '/home/zeninvest/weights',
                 '/home/zeninvest/vocab']

    # variable arguments are passed to gensim's word2vec model
    create_embeddings(data_path[0], data_path[1], data_path[2], size=300, min_count=5,
                      window=10, sg=1, iter=15)

    word2idx, idx2word = load_vocab(data_path[2])

    # cosine similarity model
    input_a = Input(shape=(1,), dtype='int32', name='input_a')
    input_b = Input(shape=(1,), dtype='int32', name='input_b')
    embeddings = word2vec_embedding_layer(data_path[1])
    embedding_a = embeddings(input_a)
    embedding_b = embeddings(input_b)
    similarity = merge([embedding_a, embedding_b],
                       mode='cos', dot_axes=2)

    model = Model(input=[input_a, input_b], output=[similarity])
    model.compile(optimizer='sgd', loss='mse')

    while True:
        word_a = input('First word: ')
        if word_a not in word2idx:
            print('Word "%s" is not in the index' % word_a)
            continue
        word_b = input('Second word: ')
        if word_b not in word2idx:
            print('Word "%s" is not in the index' % word_b)
            continue
        output = model.predict([np.asarray([word2idx[word_a]]),
                                np.asarray([word2idx[word_b]])])
        print(output)
