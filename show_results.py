import pickle
import matplotlib.pyplot as plt
import numpy as np


def open_pickle(url):
    with open(url, 'rb') as file:
        return pickle.load(file)


def open_numpy(url):
    with open(url, 'rb') as file:
        f = np.load(file)
        return f


def create_article_list(dic_file, nb_article=362):
    dic = sorted(dic_file.items(), reverse=True)
    articles = []
    for i in dic:
        if nb_article > 0:
            articles.append([i[0], i[1]])
            nb_article -= 1
    return articles


def compute_accuracy(real_value, prediction):
    ech_len = len(real_value)
    errors = 0
    assert len(real_value) == len(prediction)
    for i, j in enumerate(real_value):
        if real_value[i] != prediction[i]:
            errors += 1
    if ech_len > 0:
        return (errors/ech_len)*100
    else:
        return


def plot_data(real_value, prediction, accuracy):
    assert len(real_value) == len(prediction)
    fig, ax = plt.subplots()
    fig.suptitle('Plot real variation of stock prices')
    y = []
    y_pred = []
    for i in range(0, 50):
        y.append(real_value[i])
        y_pred.append(prediction[i])
    x = np.arange(0, 50, 1)
    ax.set_title('Accuracy = ' + str(accuracy) + " %")
    ax.set_xlabel("Days")
    ax.set_ylabel("Variation of stock prices")
    ax.plot(x, y)
    ax.plot(x, y_pred)
    plt.show()


if __name__ == '__main__':
    f = open_pickle('./pickle_article/Amazon.csv.pkl')
    articles_list = create_article_list(f)
    share_price = open_pickle('./pickle/Amazon.pkl')
    share_price_value = [share_price[i[0]] for i in articles_list]
    model_prediction_share_price = open_numpy('./Amazon_y_test.npy')
    model_prediction_share_price_normalize = []
    for i in model_prediction_share_price:
        if i[0] == 1:
            model_prediction_share_price_normalize.append(-1)
        elif i[1] == 1:
            model_prediction_share_price_normalize.append(0)
        else:
            model_prediction_share_price_normalize.append(1)
    print("Accuracy = ", str(compute_accuracy(share_price_value, model_prediction_share_price_normalize)) + " %")
    plot_data(share_price_value, model_prediction_share_price_normalize, compute_accuracy(share_price_value, model_prediction_share_price_normalize))
