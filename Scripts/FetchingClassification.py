import tweepy
from textblob import TextBlob as tb
import matplotlib.pyplot as plt
from matplotlib import style
import csv
import numpy as np
from sklearn import model_selection, neighbors, svm
from sklearn.cluster import KMeans
import pandas as pd
style.use('ggplot')


class twiAPI:  # this class would take care of the analysis process
    def __init__(self, mode):
        conKey = '3YgEqBdrAUtf1lszmlRSyqocG'
        conSec = 'oFPFB80qZezRKND6RAuocKIISgVXEXkxULRJ3g9S2IN7QeH69N'  # constructor only accounts for operation mode

        if mode == 'user':
            accsTok = '805601647460286464-aWCEoOD3Rx760e2WFl8tAizPniLGgZu'
            accsSec = 'qSs7Xta7zYHKuIkddjushfMRJPJJ5K0hgwd91a6pLgwQZ'

            auth = tweepy.OAuthHandler(conKey, conSec)
            auth.set_access_token(accsTok, accsSec)

        if mode == 'app':
            self.auth = tweepy.AppAuthHandler(conKey, conSec)  # main mode used since it retrieve the most tweets

        self.mode = mode
        self.API = tweepy.API(self.auth)
        self.Tag = ''

    def getTweets(self, hashTg):  # function retrieves tweets from the desired hashtag or query inputted
        tweetList = tweepy.Cursor(self.API.search, q=hashTg, count=100, result_type='recent', include_entities=True).items(3000)  # current API restricts to a max of 100 tweets per page.

        self.prepareCSV(hashTg)

        self.Tag = hashTg

        for twt in tweetList:  # grabs raw data and processes it through the TextBlob natural language processing
            print(twt.text)  # and processes tokenizes string along with giving weight
            analyze = tb(twt.text)
            print(analyze.sentiment)
            self.appendCSV(analyze, hashTg)

        self.classification()

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

        if twtSub < 0:
            twtSbClass = 0
        else:
            twtSbClass = 1

        for tags in textBlobData.tags:
            tagCounter += 1

        with open(fileName, "a") as dataBFile:
            fileWriter = csv.writer(dataBFile)
            fileWriter.writerow([tagCounter, twtPol, twtSub, twtPlClass, twtSbClass])

        dataBFile.close()

    def classification(self):
        dbName = self.Tag

        dataFrame = pd.read_csv(dbName + '.csv')

        dataFrame.drop(['SubjClass'], 1, inplace=True)

        X = np.array(dataFrame.drop(['PolClass'], 1))
        Y = np.array(dataFrame['PolClass'])

        X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=0.2)

        clfK = neighbors.KNeighborsClassifier()
        clfK.fit(X_train, Y_train)

        accuracy = clfK.score(X_test, Y_test)
        print(accuracy)

        clfS = svm.SVC()
        clfS.fit(X_train, Y_train)

        accuracy = clfS.score(X_test, Y_test)
        print(accuracy)


htQuery = raw_input('Please enter your desired hashtag.')

app = twiAPI('app')

app.getTweets(htQuery)
