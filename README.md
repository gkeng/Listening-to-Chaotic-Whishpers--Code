# LCW-Code

This repo is in progress. It is dedicated to an implementation of Listening to Chaotic Whispers. https://arxiv.org/abs/1712.02136v1
We are writing a serie of blogpost to explain each step of our workflow. 
You may find the first the first post on Medium : https://medium.com/@gkeng/make-your-computer-invest-like-a-human-ef0654ccdcff

Description of each file :
- SP500_nasdaq100.csv : Csv file containing all companies in S&P 500 and Nasdaq
- extract_reuters : Parallelized scraping of article from reuters.com
- extract_wsj : Attempt of scraping Wall Street Journal
- data_process : some data processing on articles collected
- doc2vec : Doc2Vec vectorization of press articles
- word2vec : Word2Vec vectorization of press articles, but we preferred to continue with Doc2vec
- list_firm : List of all firms we choosed for this implementation
- create_dataset : A script to create our 4 dimensions dataset for each company
- picklizer : A script to make pickle file of all press articles for each firm
- action : A class that implements methods and object to simulate a portfolio
- han : Implementation of the Hybrid Attention Network
- pickle : a folder with all pickle files for stock price of companies
- pickle_article : a folder with all pickle files for articles on each company.

Steps to follow to run the project :
1.  Run extract_reuters.py it will organize articles in folder like this : 
    your_chosen_folder <=== day_folder <== journal_dir <== article_title.txt
    
2.  Use functions in data_process.py to process the data. In this order :
    - rename_dir : will rename all directories. The directory for the first day( 1st January 201X) will be "0001"
    - rename_file : will give an ID to every file. The 15th article of the first day will be "0001_15.txt"
    - create_csv_firm will create a csv for each company in which one can find every day and ID of articles in 
      which the company is cited
  
3.  Run picklizer.py. This creates a dictionnary for each company and saves it as a pickle file.
    { str day : str [ list of all articles ID for this company on this day] }
   
      
4.  Run doc2vec.py to train the doc2vec model and vectorize all the press articles. 
    The output file is heavy.. For years 2015 to 2017 our doc2vec file was 2 Go of size


https://www.kaggle.com/camnugent/sandp500

5.  
    
    
