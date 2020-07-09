from dbInterface import DBInterface
import datetime
# from urllib.parse import quote
# import pandas as pd
# import googlesearch
# import requests
# import argparse
# from urllib.request import Request, urlopen
# import urllib
# from bs4 import BeautifulSoup
from googleapiclient.discovery import build
# import pprint
# import re
from pytrends.request import TrendReq
from searchtweets import ResultStream, gen_rule_payload, load_credentials

class Collector():

    DBInterface.initialize('eotm')

    dbObj = DBInterface.find('ubertrends')

    ubertrends = []
    ubertrends_relTopics = {}

    '''
        from the DB Obj save the ubertrends in one list, and then
        save the related topics in a dict, where the key is the 
        ubertrend, and the related topics are the values
    '''
    for obj in dbObj:
        ubertrends.append(obj['trend'])
        # print(obj.get('related_topics', None))
        # print(obj['related_topics'])
        ubertrends_relTopics[obj['trend']] = obj.get('related_topics', None)


    '''
    #############################################################################
                                   Google Block
    #############################################################################
    '''

    def googleTrends(self, topic, _30days=True, oneDay=True):

        '''
         Use Google Passed Only Proxies if google rate applies: proxies=['https://34.203.233.13:80',] 'https://35.201.123.31:880'
        '''
        pytrend = TrendReq(backoff_factor=0.1, )

        if _30days:

            pytrend.build_payload(kw_list=['+'.join(topic.split())], timeframe='today 1-m', gprop='news')
            # Interest over 30 days
            df = pytrend.interest_over_time()
            results_30Days = {}
            for row in df.itertuples():
                results_30Days[str(row[0].date())] = row[1]

            #print(results_30Days)

        if oneDay:

            pytrend.build_payload(kw_list=['+'.join(topic.split())], timeframe='now 1-d', gprop='news')
            df = pytrend.interest_over_time()
            results_intraDay = {}
            for row in df.itertuples():
                #print(row)
                # TODO check this line at some point, if the conversion to date is correct
                results_intraDay[str(row[0].date())] = row[1]

            #print(results_intraDay)

        if oneDay and _30days:
            return results_30Days, results_intraDay
        elif oneDay:
            return results_intraDay
        elif _30days:
            return results_30Days
        else:
            print('No resutls to return')

    def searchGoogleTrends(self, topics, _30days=True, oneDay=True):

        today = datetime.date.today()
        search_results = {}
        ubertrends_relatedTopics = topics.items()
        if _30days and oneDay:
            for ubertrend, rel_topics in ubertrends_relatedTopics:

                search_results[ubertrend] = {}
                search_results[ubertrend]['monthly'], search_results[ubertrend]['daily'] = self.googleTrends(ubertrend)
                print("collecting information from google on related topics of " + ubertrend)
                search_results[ubertrend]['related_topics'] = {}
                #search_results_intraDay[ubertrend]['related_topics'] = {}
                for topic in rel_topics:
                    search_results[ubertrend]['related_topics'][topic] = {}
                    search_results[ubertrend]['related_topics'][topic]['google'] = {}
                    search_results[ubertrend]['related_topics'][topic]['google']['monthly'] = {}
                    search_results[ubertrend]['related_topics'][topic]['google']['daily'] = {}
                    search_results[ubertrend]['related_topics'][topic]['google']['monthly'], search_results[ubertrend]['related_topics'][topic]['google']['daily'] = self.googleTrends(topic)

                    DBInterface.update_one('ubertrends', {'trend': ubertrend},
                                           {'related_topics.' + topic + '.google.monthly': search_results[ubertrend]['related_topics'][topic]['google']['monthly'],
                                            'related_topics.' + topic + '.google.daily': search_results[ubertrend]['related_topics'][topic]['google']['daily']})

                DBInterface.update_one('ubertrends', {'trend': ubertrend},
                                   {'google.monthly': search_results[ubertrend]['monthly'], "google.daily": search_results[ubertrend]['daily']})
        elif _30days:

            for ubertrend, rel_topics in ubertrends_relatedTopics:

                search_results[ubertrend] = {}
                search_results[ubertrend]['monthly'] = self.googleTrends(ubertrend)
                print("collecting information from google on related topics of " + ubertrend)
                search_results[ubertrend]['related_topics'] = {}
                for topic in rel_topics:
                    search_results[ubertrend]['related_topics'][topic] = {}
                    search_results[ubertrend]['related_topics'][topic]['google'] = {}
                    search_results[ubertrend]['related_topics'][topic]['google']['monthly'] = {}
                    search_results[ubertrend]['related_topics'][topic]['google']['monthly'] = self.googleTrends(topic)

                    DBInterface.update_one('ubertrends', {'trend': ubertrend},
                                           {'related_topics.' + topic + '.google.monthly':
                                                search_results[ubertrend]['related_topics'][topic]['google']['monthly']})

                DBInterface.update_one('ubertrends', {'trend': ubertrend},
                                   {'google.monthly': search_results[ubertrend]['monthly']})

        elif oneDay:


            for ubertrend, rel_topics in ubertrends_relatedTopics:
                search_results[ubertrend] = {}
                search_results[ubertrend]['daily'] = self.googleTrends(ubertrend)
                print("collecting information from google on related topics of " + ubertrend)
                search_results[ubertrend]['related_topics'] = {}
                for topic in rel_topics:
                    search_results[ubertrend]['related_topics'][topic] = {}
                    search_results[ubertrend]['related_topics'][topic]['google'] = {}
                    search_results[ubertrend]['related_topics'][topic]['google']['daily'] = {}
                    search_results[ubertrend]['related_topics'][topic]['google']['daily'] = self.googleTrends(topic)

                    DBInterface.update_one('ubertrends', {'trend': ubertrend},
                                       {'related_topics.' + topic + '.google.daily':
                                            search_results[ubertrend]['related_topics'][topic]['google']['daily']})

                DBInterface.update_one('ubertrends', {'trend': ubertrend},
                                   {'google.daily': search_results[ubertrend]['daily']})

    '''
    #############################################################################
                                   End of Google Block
    #############################################################################
    '''

    '''
    #############################################################################
                                    Twitter Block
    #############################################################################
    '''
    def twitterSearchEngine(self, topic):

        twitter_search_args = load_credentials(filename="secret.yaml",
                                               yaml_key="search_tweets_api",
                                               env_overwrite=False)
        today = datetime.date.today()
        start_date = today + datetime.timedelta(-30)


        rule = gen_rule_payload("#" + ''.join(topic.split()),
                                from_date=str(start_date),
                                to_date=str(today),
                                results_per_call=100, )
        rs = ResultStream(rule_payload=rule,
                          max_results=100,
                          max_pages=100,
                          **twitter_search_args)

        tweets = rs.stream()

        list_tweets = list(tweets)

        '''
        Print a list of found tweets to make sure we are on right track
        '''
        #[print(tweet.all_text, end='\n\n') for tweet in list_tweets[0:5]]
        #[print(tweet) for tweet in list_tweets[0:2]]
        tweets_json = {}
        for tweet in list_tweets:
            tweets_json.update(tweet)

        count = len(list_tweets)

        tweet_text = []
        tweet_date = []
        for tweet in list_tweets:
            tweet_text.append(tweet['text'])
            tweet_date.append(tweet['created_at'])

        #tweetDetails['topic'] = topic
        tweetDetails = {}
        tweetDetails['content'] = tweet_text
        tweetDetails['date'] = tweet_date
        tweetDetails['twitter_count'] = count

        return tweetDetails, tweets_json



    def searchTwitter(self, topics):

        today = datetime.date.today()
        search_results = {}

        '''TODO add a sanity check where type of topics is checked before deciding what to do with it'''
        # if type(topics) is dict:

        ubertrends_relatedTopics = topics.items()

        for ubertrend, rel_topics in ubertrends_relatedTopics:

            search_results[ubertrend] = {}
            search_results[ubertrend], allTweets_ubertrend = self.twitterSearchEngine(ubertrend)
            ubertrend_count = search_results[ubertrend]['twitter_count']
            print('ubertrend '+ubertrend+' twitter count is '+ str(ubertrend_count))
            print("collecting information from twitter on related topics of " + ubertrend)
            DBInterface.update_one('ubertrends', {'trend': ubertrend}, {'twitter.' + str(today): ubertrend_count})
            search_results[ubertrend]['related_topics'] = {}
            for topic in rel_topics:
                search_results[ubertrend]['related_topics'][topic] = {}
                search_results[ubertrend]['related_topics'][topic]['twitter'] = {}
                search_results[ubertrend]['related_topics'][topic]['twitter'], allTweets_topic = self.twitterSearchEngine(topic)
                relatedTopic_count = search_results[ubertrend]['related_topics'][topic]['twitter']['twitter_count']
                DBInterface.update_one('ubertrends', {'trend': ubertrend}, {'related_topics.'+topic+'.twitter.'+str(today): relatedTopic_count})
                print(allTweets_topic)
                if bool(allTweets_topic):
                    DBInterface.insert('rawTweets', allTweets_topic)

            DBInterface.insert_one('tweets_collection', search_results)



        DBInterface.insert_one('rawTweets', allTweets_ubertrend)
        print(search_results)


    '''
    #############################################################################
                                   End of Twitter Block
    #############################################################################
    '''


    '''
    #############################################################################
                                    TechCrunch
    #############################################################################
    '''

    def searchTechCrunch(self, topics, api_key, cse_id, dateRestrict, **kwargs):

        #dateRestrict could be d[number], month[number], year[number]

        today = datetime.date.today()
        search_results = {}
        ubertrends_relatedTopics = topics.items()
        service = build("customsearch", "v1", developerKey=api_key)

        for ubertrend, rel_topics in ubertrends_relatedTopics:

            print("collecting information from techCrunch on related topics of " + ubertrend)
            search_results[ubertrend] = {}
            search_results[ubertrend]['techCrunch'] = service.cse().list(q='"'+'+'.join(ubertrend.split())+ '" site:techcrunch.com', cx=cse_id, dateRestrict=dateRestrict).execute()
            search_results[ubertrend]['related_topics'] = {}

            # if ubertrend=='Distributed Ledger Technology':
            #     DBInterface.update_one('ubertrends', {'trend': ubertrend}, {
            #         'techCrunch.' + str(today - datetime.timedelta(days=1)):
            #             search_results[ubertrend]['techCrunch']['searchInformation'][
            #                 'totalResults']})

            DBInterface.update_one('ubertrends', {'trend': ubertrend}, {
                'techCrunch.'+str(today-datetime.timedelta(days=2)): search_results[ubertrend]['techCrunch']['queries']['request'][0][
                    'totalResults']})
            # search_results_intraDay[ubertrend]['related_topics'] = {}
            for topic in rel_topics:
                search_results[ubertrend]['related_topics'][topic] = {}
                search_results[ubertrend]['related_topics'][topic]['techCrunch'] = service.cse().list(q='"'+'+'.join(topic.split())+ '" site:techcrunch.com', cx=cse_id, dateRestrict=dateRestrict).execute()
                print(search_results[ubertrend]['related_topics'][topic]['techCrunch'])
                DBInterface.update_one('ubertrends', {'trend': ubertrend}, {'related_topics.'+topic+'.techCrunch.'+str(today-datetime.timedelta(days=2)):search_results[ubertrend]['related_topics'][topic]['techCrunch']['searchInformation']['totalResults']})



        DBInterface.insert_one('rawTweets', search_results)

    '''
    #############################################################################
                                    End of TechCrunch
    #############################################################################
    '''

'''
Replace the next two lines with your API Key and Custome Search Engine ID
'''
my_api_key = ""
my_cse_id = ""
testRun= Collector()
#testRun.searchTwitter(testRun.ubertrends_relTopics)
#testRun.searchGoogleTrends(testRun.ubertrends_relTopics)
testRun.searchTechCrunch(testRun.ubertrends_relTopics, my_api_key, my_cse_id, dateRestrict='d30')