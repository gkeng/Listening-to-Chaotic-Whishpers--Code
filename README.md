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
