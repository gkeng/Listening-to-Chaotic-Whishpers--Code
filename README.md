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
- han_training : Implementation and training of HAN
- pickle : a folder with all pickle files for stock price of companies
- pickle_article : a folder with all pickle files for articles on each company
- daterange : to link the ID of day to the actual day (year/month/day).

Folders : 

- sample_of_scrap : sample of the articles we scraped
- stock_value : Contains stock values and stock moves of the companies.
- pickle : Contains dictionaries of all stock moves in pickles files. Used to create y_train and y_test
- pickle_article : Contains dictionnaries { str day : str [ list of all articles ID for this company on this day] } in pickle file.
- firm_csv_folder_old : Contains csv with IDs of all articles for each company.

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

Now, focus on the stock prices and stock moves. We took most of our stock values from here :
https://www.kaggle.com/camnugent/sandp500
You can also find many here : https://www.kaggle.com/borismarjanovic/price-volume-data-for-all-us-stocks-etfs

5.  Run pickle_stock_value.py to transform all csv of stock values in a pickle file containing a dictionary :
    { str day : float stock_value }

6.  Run make_stock_move.py to create a csv of stock moves from day t to day t+1.
   
7.  Run pickle_stock_move.py to create a dic of stock moves from day t to day t+1 stored in a pickle.
    { str day : int stock_move }

8.  Run create_dataset.py to create the 4 dimension datase. tRefer to the comments in the code for more details.

9.  Train the model with han_training.py

10. Test the model with show_results.py
    
    
