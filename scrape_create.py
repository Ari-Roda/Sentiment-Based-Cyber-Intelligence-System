###python 2.7

import tweepy
import datetime, os
import tweet_cleaner
import pandas as pd
from sklearn.externals import joblib
import matplotlib.pyplot as plt
import time
from collections import defaultdict

pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 100)
pd.set_option('max_colwidth', 200)

df = pd.DataFrame()
df1 = pd.DataFrame()
df2 = pd.DataFrame()
df3 = pd.DataFrame()

###########setting dictionaries, lists and variables#####
neg_sec_tweet_dict = {}
pos_sec_tweet_dict = {}
latest_tweets = []
TSA_dict = {}
company_sent_dict = {}
total_count = []
comp_sec_list = {}
comp_sec_word_count = {}
company_total_tweets = {}
neg_company_sent_dict = {}
pos_company_sent_dict = {}
min_company_sentsec_dict = {}
pos_company_sentsec_dict = {}
neg_comp_sec_words = {}
tot_company_sentsec_dict = {}
comp_tweets_dictionary = {}
company_tweet_record = {}
#########################################################
##########################################################################################################
############################Setting twitter authentication keys###########################################
##########################################################################################################
consumer_key = ""  #
consumer_secret = ""  #
access_token = ""  #
access_token_secret = ""  #
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  #
auth.set_access_token(access_token, access_token_secret)  #
api = tweepy.API(auth)  #
##########################################################################################################
############################twitter accounts to use and sec words to filter by########################################################################################################
security_words = [] # insert security words list here
company_names = []  # insert companies to track here
accounts = []       # insert twitter accounts to follow here
gen_words = []      # insert second associated words filter here

original_filter = []# same as security words list


##############################################################################################################################
##########################getting tweets from site and putting them in a csv##################################################
def retreive_make_tweets():  #
    try:  #
        for users in accounts:
            item = api.user_timeline(screen_name=users, count=1000, include_rts=True)
            for status in item:  #
                if status.created_at + datetime.timedelta(hours=9) >= datetime.datetime.now() - datetime.timedelta(
                        hours=18):
                    latest_tweets.append(tweet_cleaner.tweet_cleaner_updated(status.text))
                    # print (users,'sssss',status.text)
    except tweepy.TweepError:  #
        print ('this users throwing an error ', users)  #
        #
    new_df = pd.DataFrame(latest_tweets, columns=['text'])  #
    new_df.to_csv('new_tweet.csv', encoding='utf-8')  #
    csv = 'new_tweet.csv'  #
    return csv  #


##############################################################################################################################
##############tweets plus predicted sentiment into a dictionary################
def tnsa_dict():  #
    i = 0  #
    for entry in new_x:  #
        TSA_dict[entry.lower()] = result[i]  #
        i += 1  #
    return TSA_dict  #


###############################################################################
#######tweets with negative sentiment and security words into dictionary#######
############################takes in tnsa_dict#################################
def minusseclist(tsad):  #
    for key, value in tsad.iteritems():  #
        splited_tweet = key.lower()  #
        splited_tweet = splited_tweet.split()  #
        for word in splited_tweet:  #
            if word in security_words:
                if value == 4:
                    neg_sec_tweet_dict.update({key: value})
    return neg_sec_tweet_dict  #


###############################################################################
def posseclist(tsad):  #
    for key, value in tsad.iteritems():  #
        splited_tweet = key.lower()  #
        splited_tweet = splited_tweet.split()  #
        for word in splited_tweet:  #
            if word in security_words:
                if value == 0:
                    pos_sec_tweet_dict.update({key: value})
    return pos_sec_tweet_dict


###############percent of negative tweets with sec words of total##############
###########is fed in neg_sec_tweet_dict and TSA_dict to do percentage##########
def percentage_of_negsec(x, y):  #
    negsec_tweets = float(len(x))  #
    total_tweets = float(len(y))  #
    return float((negsec_tweets / total_tweets) * 100)  #


###############################################################################
#####making dict of company names and adding there sent values as value########
def comp_sent(tsad):
    for company in company_names:  #
        company_sent_dict[company] = []
    for key, value in tsad.iteritems():  #
        splited_tweet = key.lower()  #
        splited_tweet = splited_tweet.split()
        for word in splited_tweet:  #
            if word in company_names:
                company_sent_dict[word].append(value)
    return company_sent_dict  #


###############################################################################
#####making dict of company names and adding there sent values as value########
def comp_word_sent(tsad):
    for company in company_names:  #
        comp_sec_word_count[company] = defaultdict(list)
    for key, value in tsad.iteritems():  #
        splited_tweet = key.lower()  #
        splited_tweet = splited_tweet.split()
        for word in splited_tweet:  #
            if word in company_names:
                for i in splited_tweet:
                    if i in security_words:
                        comp_sec_word_count[word][i].append(value)
    return comp_sec_word_count  #


###############################################################################
###############################################################################
##########putting company in list and finding if pos or neg tweets are higher##
###and returning percentage of neg or pos sentiment############################
##########taking in comp_sent############################################################
def company_current_sentiment(sent_dict):  #
    sentiment_dict = {}
    for key, value in sent_dict.iteritems():
        positive = []
        negative = []
        for i in value:  #
            if i == 0:  #
                positive.append(i)  #
            elif i == 4:
                negative.append(i)

        if len(positive) > len(negative) and len(positive) > 0:
            sentiment_dict[key] = (float(len(positive)) / float(len(negative) + len(positive))) * 100
        elif len(negative) > len(positive) and len(negative) > 0:
            sentiment_dict[key] = (-(float(len(negative)) / float(len(positive) + len(negative))) * 100)
        else:  #
            sentiment_dict[key] = ("0")  #
            #
    return sentiment_dict  #


#########################################################################################
def overall_pos(tda):
    overall_neg = []
    overall_pos = []
    for key, value in tda.iteritems():
        if value == 4:
            overall_neg.append(1)
        else:
            overall_pos.append(1)

    return len(overall_pos)


#########################################################################################
def overall_neg(tda):
    overall_neg = []
    overall_pos = []
    for key, value in tda.iteritems():
        if value == 4:
            overall_neg.append(1)
        else:
            overall_pos.append(1)

    return len(overall_neg)


###############################################################################
#####total number of tweets that contain company name########
###############################################################################
def total_company_tweets(tsad):
    for company in company_names:  #
        company_total_tweets[company] = 0  # make a dictioanry with keys as company names
    for key, value in tsad.iteritems():
        splited_tweet = key.lower()  # make tweet lower case
        splited_tweet = splited_tweet.split()  # split each word of tweet
        for word in splited_tweet:
            if word in company_names:  # if word is a company name add 1
                company_total_tweets[word] += 1
    return company_total_tweets


###############################################################################
##############make dictionary with negative tweets per company#################
###############################################################################
def comp_overall_neg(tda):
    for company in company_names:  #
        neg_company_sent_dict[company] = []
    for key, value in tda.iteritems():
        for i in value:
            if i == 4:
                neg_company_sent_dict[key] += '4'
    return neg_company_sent_dict


###############################################################################
##############make dictionary with positive tweets per company#################
###############################################################################
def comp_overall_pos(tda):
    for company in company_names:  #
        pos_company_sent_dict[company] = []
    for key, value in tda.iteritems():
        for i in value:
            if i == 0:
                pos_company_sent_dict[key] += '0'
    return pos_company_sent_dict


################################################################################
#######tweets with negative sentiment and security words into dictionary#######
############################takes in tnsa_dict#################################
def comp_minusseclist(tsad):
    for company in company_names:
        min_company_sentsec_dict[company] = []
    for key, value in tsad.iteritems():
        splited_tweet = key.lower()
        splited_tweet = splited_tweet.split()
        for word in splited_tweet:
            if word in company_names:
                for i in splited_tweet:
                    if i in security_words:
                        if value == 4:
                            min_company_sentsec_dict[word] += '4'
    return min_company_sentsec_dict


###############################################################################
def comp_posseclist(tsad):
    for company in company_names:
        pos_company_sentsec_dict[company] = []
    for key, value in tsad.iteritems():
        splited_tweet = key.lower()
        splited_tweet = splited_tweet.split()
        for word in splited_tweet:
            if word in company_names:
                for i in splited_tweet:
                    if i in security_words:
                        if value == 0:
                            pos_company_sentsec_dict[word] += '4'
    return pos_company_sentsec_dict


###############################################################################
def comp_total_seclist(tsad):
    for company in company_names:
        tot_company_sentsec_dict[company] = []
    for key, value in tsad.iteritems():
        splited_tweet = key.lower()
        splited_tweet = splited_tweet.split()
        for word in splited_tweet:
            if word in company_names:
                for i in splited_tweet:
                    if i in security_words:
                        if value == 4 or value == 0:
                            tot_company_sentsec_dict[word] += '1'
    return tot_company_sentsec_dict


################################################################################
def comp_word_sent(tsad):
    for company in company_names:
        comp_sec_word_count[company] = defaultdict(list)

    for key, value in tsad.iteritems():
        splited_tweet = key.lower()
        splited_tweet = splited_tweet.split()
        for word in splited_tweet:
            if word in company_names:
                for i in splited_tweet:
                    if i in security_words:
                        comp_sec_word_count[word][i].append(value)
    return comp_sec_word_count


###################################################################################
#########getting tweets containing company names###################################
###################################################################################
def git_good(splitted_tweet, compname, tweet):
    allready_used_company_name = []
    if compname in company_names:
        # print (tweet)
        for i in splitted_tweet:
            if (i in gen_words or i in original_filter) and compname not in allready_used_company_name:
                comp_tweets_dictionary[compname].append(tweet)
                allready_used_company_name.append(compname)
                break
    return (comp_tweets_dictionary)


###################################################################################
def company_tweetser(tsad):
    for company in company_names:
        comp_tweets_dictionary[company] = []

    for key, value in tsad.iteritems():
        splited_tweet = key.lower()
        splited_tweet = splited_tweet.split()
        for word in splited_tweet:
            git_good(splited_tweet, word, key)

    return comp_tweets_dictionary


###################################################################################
def neg_word_sec_words(dictionary):
    return {k: {k_: sum(x == 4 for x in v_) for k_, v_ in v.items()} for k, v in dictionary.items()}


###################################################################################
def pie_chart_maker(dictionary):
    for k, v in dictionary.iteritems():
        labels = []
        sizes = []
        for k_, v_ in v.items():
            if v_ != 0:
                plt.title(k)
                labels.append(k_)
                sizes.append(v_)

        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.axis('equal')
        plt.show()


####################################################################################


while True:
    latest_df = pd.read_csv(retreive_make_tweets())  # retrieve make tweets returns a csv of all scanned tweets
    # based on the stuff we set, eg accounts etc
    latest_df.dropna(inplace=True)  # drop null entries
    latest_df.reset_index(drop=True, inplace=True)
    new_x = latest_df.text  # set new_x as pandas dataframe containing all tweets scanned
    loaded_model = joblib.load("finalized_model.sav")  # loading classification model for sentiment classification
    result = loaded_model.predict(new_x)  # using classification model for prediction
    minusseclist(tnsa_dict())  # make dictionary of negative tweets,

    fkn_cnt = company_tweetser(tnsa_dict())
    no_value_removed = {k: v for k, v in fkn_cnt.items() if len(v) != 0}
    for key, value in no_value_removed.items():
        dfcomps = pd.DataFrame()
        with open(key + '_tweets.csv', mode='a') as comp_tweets:
            dfcomps["tweet"] = (value)
            dfcomps["date"] = str(time.strftime('%d/%m/%Y'))
            dfcomps["time"] = str(time.strftime('%X'))
            dfcomps.to_csv(comp_tweets, header=False)

    print ("pass")
    try:
        os.remove("new_tweet.csv")
    except:
        print ("new_tweet not there")
    # pie_chart_maker(neg_word_sec_words(comp_word_sent(tnsa_dict())))
    time.sleep(3600)

    with open('live_information.csv', mode='w') as live_tweets:

        for key,value in company_current_sentiment(comp_sent(tnsa_dict())).iteritems():
            df2[str(key)] = [value]

        df2.to_csv("", header=False) # enter path for live sent info file


    with open('live_company_information.csv', mode='w') as company_tweets:

        for key,value in company_current_sentiment(comp_sent(tnsa_dict())).iteritems():
            df3[str(key)] = [value]

        for key, value in total_company_tweets(tnsa_dict()).iteritems():
            df3[str(key + " total tweets")] = value

        for key, value in (comp_overall_neg(comp_sent(tnsa_dict()))).iteritems():
            df3[str(key + "total negative")] = len(value)

        for key, value in (comp_overall_pos(comp_sent(tnsa_dict()))).iteritems():
            df3[str(key + "total positive")] = len(value)

        for key, value in comp_total_seclist(tnsa_dict()).iteritems():
            df3[str(key + "total company with sec words")] = len(value)

        for key, value in comp_minusseclist(tnsa_dict()).iteritems():
            df3[str(key + "neg company with sec words")] = len(value)

        for key, value in comp_posseclist(tnsa_dict()).iteritems():
            df3[str(key + "pos company with sec words")] = len(value)

        for key, value in neg_word_sec_words(comp_word_sent(tnsa_dict())).iteritems():
            df3[str(key + "security words")] = [value]

        for key, value in (comp_word_sent(tnsa_dict())).iteritems():
            df3[str(key + "security words")] = [value]

        df3["date"] = [str(time.strftime('%d/%m/%Y'))]
        df3["time"] = [str(time.strftime('%X'))]

        df3.to_csv("", header=False)  # enter path for company info file




