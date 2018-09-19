from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import os
import numpy as np


class OurDoc2Vec(object):

    """
	Class to create a doc2vec model
    """

    def __init__(self, dirname, model_path):

        """
        Constructor of the class
        :param dirname: folder nam
        :param model_path: path to save the model
        """

        self.dirname = dirname
        self.model_path = model_path
        self.tagged_data = []

    def prepare_data(self):

        """
		Prepares the data by creating an array of articles. Each of them will be assigned a tag
        :return:
        """

        data = []
        tag = []
        i = 0
		
		# simple for loops to get all the articles and add them to the data and tag list 
        for newspaper in os.listdir(self.dirname):
            days = os.path.join(self.dirname, newspaper)
            for day in os.listdir(days):
                day_path = os.path.join(days, day)
                for fname in os.listdir(day_path):
                    f_path = os.path.join(day_path, fname)
                    print(f_path)
                    data.append(open(f_path, 'rb').read())
                    tag.append(fname[:-5])
                    print(i)
                    i += 1

		# tagging all the articles
        self.tagged_data = [TaggedDocument(words=word_tokenize(str(_d.lower())), tags=[str(tag[i])]) for i, _d in
                            enumerate(data)]

        # Freeing memory

        data = []
        tag = []

    def train_doc2vec(self, max_epochs=15, vec_size=200, alpha=0.025):
        """
        Training our doc2vec model. The articles will be vectorized in a 200 dimensions vector space
        :param max_epochs: Sets the number of epochs in our training
        :param vec_size: dimension of the vector space used
        :param alpha: Learning rate used in the gradient descent
        :return:
        """
        model = Doc2Vec(vector_size=vec_size, alpha=alpha, min_alpha=0.025, min_count=5,
                        dm=1, workers=30)

        model.build_vocab(self.tagged_data)


        for epoch in range(max_epochs):
            print('iteration {0}'.format(epoch))
            model.train(self.tagged_data,
                        total_examples=model.corpus_count,
                        epochs=model.iter)
            # decrease learning rate
            model.alpha -= 0.0002
            # and reinitialize it
            model.min_alpha = model.alpha

        model.save(self.model_path)
        print("Model savec")

    def clean_train_model(self):

        """
		Aims at using the model trainned by first deleting the temporary training data. Use it carefully you can lose all the progress made in the training.
        :return:
        """

        model = Doc2Vec.load(self.model_path)
        # Be careful here
        model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

    def test_doc2vec(self):

        """
        To test the  model
        :return:

        """
        model = Doc2Vec.load(self.model_path)

        model.docvecs.doctags

        # test_data = word_tokenize("Odorizzi".lower())
        # test_data2 = word_tokenize("Page".lower())

        # v1 = model.infer_vector(test_data)
        # v2 = model.infer_vector(test_data2)

        # to print the vectorized article using tags
        vector = model.docvecs['0000_40']
        print(type(vector))
        print("Vector of document:", vector)

    def readFile(self):

        """
        To read the files created by doc2vec model
        :return:
        """

        model = Doc2Vec.load(self.model_path)

        print(type(model.docvecs.doctags))

        file = np.load('/Users/rugerypierrick/PycharmProjects/doc2vec/d2v.model.docvecs.vectors_docs.npy')

        fil2 = np.load('/Users/rugerypierrick/PycharmProjects/doc2vec/d2v.model.trainables.syn1neg.npy')

        file3 = np.load('/Users/rugerypierrick/PycharmProjects/doc2vec/d2v.model.wv.vectors.npy')


        print(file3)


if __name__ == '__main__':
    model = OurDoc2Vec("text_data", "d2v.model")
    #model.test_doc2vec()
    model.readFile()

