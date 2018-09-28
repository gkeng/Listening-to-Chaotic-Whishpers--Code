import os

stock_value_folder = " your_folder_with_csv_file_with_stock_value_for_each_company"
stock_move=stock_values_folder+'stock_move/'

label_line=[]

def make_stock_move() :

	for x in os.listdir(stock_values_folder):
		count_up=0
		count_neut=0
		count_down=0
		if x[-4:]=='.csv':
		    file_path=os.path.join(stock_values_folder,x)
		    print(x)
		    f3=open(file_path,'r')
		    lia=f3.readlines()
		    f3.close()
		    for i in range(len(lia)-1):
		        
		        taux_t=float(lia[i].split(',')[1])
		        taux_tp1=float(lia[i+1].split(',')[1])
		        raise_t=(taux_tp1-taux_t)/taux_t
		        if raise_t>0.0045:
		            label=1
		            count_up+=1
		        if (raise_t<= 0.0045 and raise_t>=-0.0045):
		            label=0
		            count_neut+=1
		        if raise_t<-0.0045:
		            label=-1
		            count_down+=1
		        line='{}{}{}{}'.format(lia[i].split(',')[0],',',str(label),'\n')
		        label_line.append(line)

		    with open('{}{}{}'.format(stock_move,x,'.csv'),'w') as f:
		        for line in label_line:
		            f.write(line)
	return(count_up,count_neut,count_down)
