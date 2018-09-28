import pickle
import os

firm_folder = " your_folder_with_csv_file_with_stock_value_for_each_company"
def pickle_stock_value():
	for fname in os.listdir(firm_folder):
		if fname[-4:]=='.csv':
		    print (fname)
		    file_path=os.path.join(article_firm_folder,fname)
		    f=open(file_path,'r')
		    lines = f.readlines()
		    f.close()
		    dic={}
		    for line in lines:
		        line=line.replace('\n','').split(',')
		        dic[line[0]]=line[1:]

		    with open(article_firm_pickle + fname+'.pkl','wb') as pick:
		        pickle.dump(dic, pick, protocol=pickle.HIGHEST_PROTOCOL)
