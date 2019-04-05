# Sentiment Based Cyber Intelligence System

This project scrapes twitter for cyber security related data and finds the sentiment of that data. It then checks if the data points are 
associated with a certain entities such as a company name and displays the average sentiment of all tweets related to that entity.


The project is comprised of three files scrape_tweet.py, tweet_cleaner.py are the backend files used to scrape and classify tweets. This 
creates a csv file containing the data that is displayed in the GUI.

Display.py is the frotend that reads the data from the files and display it.
