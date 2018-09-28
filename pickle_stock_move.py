import pickle
import os

stock_move = " your_folder_with_csv_file_with_stock_move_for_each_company"

def pickle_stock_move():

	for fname in os.listdir(stock_move):
		if fname[-4:]=='.csv':
		    print (fname)
		    file_path=os.path.join(stock_move,fname)
		    f=open(file_path,'r')
		    lines = f.readlines()
		    f.close()
		    dic={}
		    for line in lines:
		        line=line.replace('\n','').split(',')
		        dic[line[0]]=float(line[1])

		    with open('{}{}{}'.format(stock_move_pickle , fname[:-8],'.pkl'),'wb') as pick:
		        pickle.dump(dic, pick, protocol=pickle.HIGHEST_PROTOCOL)
	
