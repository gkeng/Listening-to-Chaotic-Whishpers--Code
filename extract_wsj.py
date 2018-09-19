from datetime import datetime
import multiprocessing as mp
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import time


def extraction_wsj(folder, year,nb_days,nb_articles_per_day, days_list):
    """
    Scrapping des articles de Wall Street Journal
    :param folder: nom du répertoire de sauvegarde
    :param year: l'année à scrapper
    :param nb_days: le nombre de jours
    :param nb_articles_per_day: nombre d'article par jour
    :param days_list: la liste des jours
    :return:
    """

    year_str = str(year)
    total = 0
    year_pattern = "http://www.wsj.com/public/page/archive-" +year_str
    article_pattern = 'http://www.wsj.com/articles/'
    article_pattern2 = 'https://www.wsj.com/articles/'

    journal = 'wsj/'
    articles_list = []
    day_count = 0
    articles_count = 0

    for link_d in days_list:
        if day_count < nb_days:

            date = link_d[39:49]
            date = date.replace(".", "").replace("h", "").replace("m", "")
            date = datetime.strptime(date, '%Y-%m-%d')
            date = str(date)[:10]
            print("-"*25)
            print('\n scrapping WSJ for date ; {}\n'.format(date))
            print('total articles scrapped : {} \n'.format(total))

            date_dir = date + '/'
            # on liste les dossiers présent dans le répertoire
            day_path = os.path.join(folder, date_dir)
            if not os.path.exists(day_path):
                os.makedirs(day_path)

            journal_dir = os.path.join(day_path, journal)
            if not os.path.exists(journal_dir):
                os.makedirs(journal_dir)

            # on stock le texte de l'article
            articles_count = 0
            html_d = urlopen(link_d)
            bs2 = BeautifulSoup(html_d.read())

            l2 = [x.get('href') for x in bs2.find_all("a")][1:]
            article_list = [x for x in l2 if (x[:len(article_pattern)]== article_pattern or
                                              x[:len(article_pattern2)] == article_pattern2)]

            day_count += 1

            for link_a in article_list:
                if articles_count < nb_articles_per_day:

                    #On récupère seulement les informations nécessaires de l'article
                    html_a = urlopen(link_a)
                    bs3 = BeautifulSoup(html_a.read())
                    title = bs3('h1')[0].text + ' '
                    title = title.replace("/", " ")
                    for tag in bs3():
                        del tag['class']
                    article = bs3('p')
                    del article[0]
                    article = [tex.text for tex in article if len(tex.text) > 150]
                    text = ''.join([x for x in article])
                    text = title + text

                    filename = title + '.txt'
                    file_path = os.path.join(journal_dir, filename)

                    f = open(file_path, 'w')
                    f.write(text)
                    f.close()
                    articles_count += 1
                    total += 1
                else:
                    break
            else:
                break
    print('Total articles scrapped : {}'.format(total))
    return('Total articles scrapped : {}'.format(total))


def main():

    """
    Lancement du scapping, initilialisation
    :return:
    """

    start_time = time.time()
    # Répertoire ou stocker les articles
    folder = '/home/zeninvest/text_data/'
    # Nombre de jour à récupérer
    nb_days = 1000
    # nombre d'article max par jour
    nb_articles_per_day = 10000
    # liste d'années
    year_list = [2017, 2016, 2015, 2014]
    nb_process = 15
    day_per_process = int(365 / nb_process)

    for year in year_list:
        year_str = str(year)
        journal = 'wsj/'
        html_year = urlopen("http://www.wsj.com/public/page/archive-" + year_str + "-1-1.html")
        bs1 = BeautifulSoup(html_year.read())
        year_pattern = "http://www.wsj.com/public/page/archive-" + year_str
        article_pattern = 'http://www.wsj.com/articles/'
        article_pattern2 = 'https://www.wsj.com/articles/'

        l = [x.get('href') for x in bs1.find_all("a")][1:]
        days_list = [x for x in l if x[:len(year_pattern)] == year_pattern]

        day_repartition = []

        for i in range(1, nb_process+1):
            day_repartition.append(days_list[(i-1) * day_per_process:i * day_per_process])

            day_repartition.append(days_list[i * day_per_process:])

        arg_list = [ [folder, year, nb_days, nb_articles_per_day, x] for x in day_repartition]

        process_list = [ mp.Process(target=extraction_wsj, args=arg) for arg in arg_list]

        for t in process_list :
            t.start()

        for t in process_list :
            t.join()


if __name__ == '__main__':
    main()
