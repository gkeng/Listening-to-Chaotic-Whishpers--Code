from datetime import timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
start_date = date(2015, 1, 1)
end_date = date(2018, 1, 1)
i=0
l=[]
for single_date in daterange(start_date, end_date):
    date=single_date.strftime("%Y-%m-%d")
    nb=str(i).zfill(4)
    l.append([date,nb])
    i+=1
date_dic={x[0]:x[1] for x in l}
date_dic