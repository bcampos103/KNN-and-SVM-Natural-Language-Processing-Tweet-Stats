import tweepy
from textblob import TextBlob as tb
import csv
import numpy as np
import matplotlib.pyplot as plt


class twiAPI:  # this class would take care of the analysis process
    def __init__(self, mode):
        conKey = '#######'
        conSec = '######'  # constructor only accounts for operation mode

        if mode == 'user':
            accsTok = '#########'
            accsSec = '#######'

            auth = tweepy.OAuthHandler(conKey, conSec)
            auth.set_access_token(accsTok, accsSec)

        if mode == 'app':
            self.auth = tweepy.AppAuthHandler(conKey, conSec)  # main mode used since it retrieve the most tweets

        self.mode = mode
        self.API = tweepy.API(self.auth)

    def getTweets(self, hashTg):  # function retrieves tweets from the desired hashtag or query inputted
        tweetList = tweepy.Cursor(self.API.search, q=hashTg, count=100, result_type='recent', include_entities=True).items()  # current API restricts to a max of 100 tweets per page.

        self.prepareCSV(hashTg)

        for twt in tweetList:  # grabs raw data and processes it through the TextBlob natural language processing
            print(twt.text)  # and processes tokenizes string along with giving weight
            analyze = tb(twt.text)
            print(analyze.sentiment)
            self.appendCSV(analyze, hashTg)

    def prepareCSV(self, hashTg):
        filename = hashTg + '.csv'

        with open(filename, "w") as dataBFile:
            fileWriter = csv.writer(dataBFile)
            fileWriter.writerow(['Tags', 'polarity', 'subjectivity', 'PolClass', 'SubjClass'])

        dataBFile.close()

    def appendCSV(self, textBlobData, hashTg):
        fileName = hashTg + '.csv'
        tagCounter = 0
        twtPol = textBlobData.polarity
        twtSub = textBlobData.subjectivity
        twtPlClass = 0
        twtSbClass = 0

        if twtPol < 0:
            twtPlClass = 0

        else:
            twtPlClass = 1

        if twtSub < .5:
            twtSbClass = 0
        else:
            twtSbClass = 1

        for tags in textBlobData.tags:
            tagCounter += 1

        with open(fileName, "a") as dataBFile:
            fileWriter = csv.writer(dataBFile)
            fileWriter.writerow([tagCounter, twtPol, twtSub, twtPlClass, twtSbClass])

        dataBFile.close()




app = twiAPI('app')

app.getTweets('microtransactions')
