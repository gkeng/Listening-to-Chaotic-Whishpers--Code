import csv
import pandas as pd
import os
import numpy as np
import multiprocessing as mp


def create_csv_firm(spnas):

    """
    
    Create a csv containing articles associated with a company each day
    :param spnas:
    :return:
    """

    for x in spnas:
        firm_name = str(x[1])
        if firm_name in lis:
            csv_stock = open('{}{}{}'.format(firm_csv_folder, firm_name, ".csv"), 'w')
            writer = csv.writer(csv_stock, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            for day in os.listdir(dirname):
                day_path = os.path.join(dirname, day + '/reuters/')
                if os.path.isdir(day_path):
                    non_empty_day = False
                    row = ""
                    for fname in os.listdir(day_path) :
                        if firm_name in fname or firm_name.upper() in fname:
                            non_empty_day = True
                            row += "%s%s" % (',', fname[:-4])
  
                        else :
                            f_path=os.path.join(day_path,fname)
                            file = open(f_path, 'r')
                            found=False
                            for line in file:
                                if firm_name in line or firm_name.upper() in line:
                                    non_empty_day=True
                                    found=True
                                    break
                            file.close()
  
                            if found:
                                row += "%s%s" % (',', fname[:-4])
  
  
                    if non_empty_day:

                        row='%s%s'%(day[:4], row)
                        writer.writerow([row])
            csv_stock.close()


def rename_dir(dirname):

    """
    Rename folder to day by day giving a standard code
    :param dirname: name of folder to modify
    :return:
    """

    day_list = []
    for day in os.listdir(dirname):
        day_path = os.path.join(dirname, day + ' /reuters/')
        if os.path.isdir(day_path):
            day_list.append(day)

    day_list = sorted(day_list)
    double_list = []
    for i,x in enumerate(day_list):
        double_list.append([x, str(i)])

    for double in double_list:
        for day in os.listdir(dirname):
            if double[0] == day:
                day_path = os.path.join(dirname, day)
                new_name = double[1].zfill(4) + '_' + double[0][-10:]
                new_path = os.path.join(dirname, new_name)
                os.rename(day_path, new_path)


def rename_file(dirname):

    """
    Standardization of article filenames
    :param dirname: name of day folder
    :return:
    """

    for day in os.listdir(dirname):
        i = 0
        day_path = os.path.join(dirname, day)
        reuters_path = os.path.join(dirname, day + '/reuters/')
        if os.path.isdir(reuters_path):
            for fname in os.listdir(reuters_path):
                new_fname = "%s%s%s%s" % (day[:4], "_", str(i), ".txt")
                old_path = os.path.join(reuters_path, fname)
                new_path = os.path.join(reuters_path, new_fname)
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                i += 1


if __name__ == '__main__':

    # Loading of files
    spnas = '/home/zeninvest/SP500_nasdaq100.csv'
    spnas_df = pd.read_csv(spnas)
    spnas_list = spnas_df[['Symbol', 'Name1']].values.tolist()
    dirname = '/home/zeninvest/text_data/'
    firm_csv_folder = '/home/zeninvest/firm_csv_folder/'
    lis = [' HP ', 'KeyCorp', ' Gap ', 'CF Industries']

    # Parallelization of the task
    nb_process = 35
    l = list(np.array_split(spnas_list, nb_process))
    l = [x.tolist() for x in l]
    process_list = [mp.Process(target=create_csv_firm,
                               args=(spnas,)) for spnas in l]

    for p in process_list:
        p.start()

    for p in process_list:
        p.join()



