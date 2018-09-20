import pickle
article_firm_folder='/home/zeninvest/firm_csv_folder/'
article_firm_pickle= article_firm_folder+'pickle/'
import csv
import os


def picklizer():

    """
    Picklize all press articles
    :return:
    """

    for fname in os.listdir(article_firm_folder):
        if fname[-4:] == '.csv':
            print(fname)
            file_path = os.path.join(article_firm_folder, fname)
            f = open(file_path, 'r')
            lines = f.readlines()
            f.close()
            dic = {}
            for line in lines:
                line = line.replace('\n', '').split(',')
                dic[line[0]] = line[1:]

            with open(article_firm_pickle + fname+'.pkl','wb') as pick:
                pickle.dump(dic, pick, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    picklizer()
