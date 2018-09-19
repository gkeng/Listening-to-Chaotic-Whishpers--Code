import pickle
import numpy as np
from gensim.models.doc2vec import Doc2Vec
from sklearn.model_selection import train_test_split
import os
import multiprocessing as mp


def create_x_y(name, model, firm_article, firm_stock, k_max=40, test_size=0.33, window=10):
    """
	Creates a 4 dimensions array.Takes a lot of mem
    :param name: name of the company
    :param model: doc2vec model that give the vector associated to each article
    :param firm_article: pickle file contening a dictionnary day : [ list of articles of the day ]
    :param firm_stock: pickle file contening a  dictionnary day : stock variation of that day
    :param k_max: max number of article per day
    :param test_size: ratio of data that we keep for testing
    :param window: number of pasted days used for the prediction
    :return: x_train, x_test, y_train, y_test
    """

    # opening the pickle for article dictionnary
    with open(firm_article, 'rb') as dict_article:
        dico_article = pickle.load(dict_article)
    # opening pickle for stock trend dictionnary
    with open(firm_stock, 'rb') as dict_stock:
        dico_stock = pickle.load(dict_stock)

    # check if both dict are non empty
    if (len(dico_article) > 0) and (len(dico_stock) > 0):
		
		''' So we build a 4 dimensions array
        # i, 1st dimension the corresponds to the days for which we have got articles about the company over the last 10 days
        # j, 2nd dimension is the window, number of pasted days used to make the prediction
        # k, 3rd dimension is the number of articles that we've got on the corresponding day
        # l, 4th dimension is the vector representing the article. In 200 dimensions'''

        # creating the array
        data = np.zeros((1, 11, k_max, 200), dtype='float32')

        y = []
        dates = []

        for i in range(int(1095)):
            # bool to know if any article was puslihed during the 11 days
            to_add = False
            # we want to predict the trend on day i+1, so we check if day i+1 is actually a key in dico_stock dictionnary
            next_day_key = str(i + 1).zfill(4)
            if next_day_key in dico_stock:
                y_i = int(dico_stock[next_day_key])
                # new row to add to the data array
                new_row = np.zeros((1, 11, k_max, 200), dtype='float32')
                for j in range(11):
                    # we look from i-k_max to i
                    day_key = str(i - j).zfill(4)
                    if (day_key in dico_article):
                        list_article = dico_article[day_key]
                        to_add = True
                        # k= key, x=value=list of ID of articles of that day
                        for k in range(k_max):
                            if k < len(dico_article[day_key]):
                                article_id = list_article[k]
                                vector = model.docvecs[article_id]
                                new_row[0, j, k, :] = vector
                            else:
                                new_row[0, j, k, :] = np.zeros(200)

                if to_add:
                    # we add the line
                    data = np.vstack([data, new_row])
                    y.append(y_i)
                    dates.append(next_day_key)

        y_vec = np.asarray(y)
        x_mat = np.delete(data, (0), axis=0)  # deletes the first line full of zeros
        x_train, x_test, y_train, y_test = train_test_split(
            x_mat, y_vec, test_size=test_size, random_state=42, shuffle=False)

        y_train_size = y_train.shape[0]
        dates_test = dates[y_train_size:]

        with open('./dates/dates' + name + '.pkl', 'wb') as handle:
            pickle.dump(dates_test, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return (x_train, x_test, y_train, y_test)
    else:
        print("Error File")
        return [], [], [], []

#just a test
def open_pickle(name_file):
    with open(name_file, 'rb') as handle:
        b = pickle.load(handle)
    print(b)


# just a test
def open_numpy():
    x1_test = np.load('./3M_x_train.npy')
    x2_test = np.load('./Abbott_x_train.npy')
    print(x1_test.shape)
    print(x2_test.shape)


def create_dataset(stockfile_list, articlefile_list):
    """
    function qui permet de lancer la création des datasets
    :param stockfile_list: liste des fichiers de cours de la bourses pour n entreprises
    :param articlefile_list: liste des fichiers d'articles pour n entreprises
    :return:
    """

    # check if we have the same number of companies
    assert len(stockfile_list) == len(articlefile_list)

    # loading d2v model
    model = Doc2Vec.load('./d2v.model')


    for i, j in enumerate(stockfile_list):
        # get the name of firm and delete the file extension
        name = articlefile_list[i][:-8]

        print('./pickle_article/' + articlefile_list[i])
        print('./pickle/' + stockfile_list[i])
        print(name)

        x_train, x_test, y_train, y_test = create_x_y(name, model, './pickle_article/' + articlefile_list[i],
                                                      './pickle/' + stockfile_list[i], 10, 0.33, 10)

        if len(x_train) > 0:

            # Encoding y_test to have 3 dimension ( to perfom 3 class classification )
            y_test_encode_start = list()

            for trend in y_test:
                new_value = trend + 1
                code = [0 for _ in range(3)]
                code[new_value] = 1
                y_test_encode_start.append(code)
            y_test_encode_end = np.asarray(y_test_encode_start)
            

            # Create numpy files
            np.save('./x_train/' + name + '_x_train.npy', x_train)
            np.save('./x_test/' + name + '_x_test.npy', x_test)

            np.save('./y_train/' + name + '_y_train.npy', y_train)
            np.save('./y_test/' + name + '_y_test.npy', y_test_encode_end)

        # Counts iteration
        nb_iteration = len(stockfile_list) - i
        print("Nb itérations restantes :", nb_iteration)


'''stock_directory = './pickle'
article_directory = './pickle_article'
stockfile_list = os.listdir(stock_directory)
articlefile_list = os.listdir(article_directory)
nb_process = 8

# trie des listes avant le split
stockfile_list.sort()
articlefile_list.sort()

#split des listes des fichiers des cours de bourses et d'articles
stock_repartition = list(np.array_split(stockfile_list, nb_process))
article_repartition = list(np.array_split(articlefile_list, nb_process))

stock_repartition = [list(x) for x in stock_repartition]
article_repartition = [list(x) for x in article_repartition]

# création d'un tableau à passer en argument
arg_list = []
for i in range(len(stock_repartition)):
    stock_arg = stock_repartition[i]
    article_arg = article_repartition[i]
    arg = [stock_arg, article_arg]
    arg_list.append(arg)

# Lancement du multi thread
process_list = [mp.Process(target=create_dataset, args=arg) for arg in arg_list]

for p in process_list:
    p.start()

for p in process_list:
    p.join()'''


if __name__ == "__main__":
    create_dataset('./pickle', './pickle_article')
    open_pickle('/Users/rugerypierrick/ZenIvest/pickle/3M .pkl')








