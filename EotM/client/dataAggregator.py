import sys
sys.path.append('/Users/vaheh/Downloads/Thesis/myinalyze/EotM/server/backend/')
from dbInterface import DBInterface


class DataAggregator:

    DBInterface.initialize('eotm')

    dbObj = DBInterface.find('ubertrends')

    ubertrends = []
    temp ={}

    for obj in dbObj:
        #print(obj)
        for key, value in obj.items():
            #print(key)
            #print(value)
            if key not in ['_id', 'source', 'ranking', 'url']:
                if value:
                    temp[key]=value
                    #print(temp)
                else:
                    temp[key]= {}
        #     print(temp)

        ubertrends.append((temp.copy()))

    def indexer(self, date_filter='2020-06-25', google_weight= 0.4, twitter_weight= 0.1, techCrunch_weight=0.5):

        techCrunch_max_ubetrend, techCrunch_min_ubertrend, techCrunch_max_trend, techCrunch_min_trend = self.normalizer(date_filter)

        trends_indexed = []


        for trend in self.ubertrends:
            trend_indexed = {}
            #if trend['trend'] in ['AI', 'Automation']:
                #print(trend)

            #TODO fix the twitter part
            trend_indexed[trend['trend']] = techCrunch_weight*(float(trend['techCrunch'].get(date_filter, 0))-techCrunch_min_ubertrend)*100/\
                                            (techCrunch_max_ubetrend-techCrunch_min_ubertrend)+\
                                            google_weight*float(trend['google']['daily'].get(date_filter,0))+\
                                            twitter_weight*float(trend['twitter'].get(date_filter,0))

            trend_indexed['related_topics']={}
            #print(trend_indexed)
            for rel_topic in trend['related_topics']:


                # if trend['related_topics'][rel_topic]['techCrunch'][date_filter]:
                #     if trend['related_topics'][rel_topic]['google']['daily'][date_filter]:
                #         if trend['related_topics'][rel_topic]['twitter'][date_filter]:


                trend_indexed['related_topics'][rel_topic] = techCrunch_weight*(float(trend['related_topics'][rel_topic]['techCrunch'].get(date_filter, 0))-techCrunch_min_trend)*100/\
                                                             (techCrunch_max_trend-techCrunch_min_trend)\
                                                                 +google_weight*float(trend['related_topics'][rel_topic]['google']['daily'].get(date_filter, 0))\
                                                                 +twitter_weight*float(trend['related_topics'][rel_topic]['twitter'].get(date_filter, 0))

            #print(trend_indexed)
            trends_indexed.append(trend_indexed.copy())

        print(trends_indexed)
        return trends_indexed


    def normalizer(self, date='2020-06-25'):

        techCrunch_max_ubertrend = 0.0
        techCrunch_min_ubertrend = 5000.0

        techCrunch_max_trend = 0.0
        techCrunch_min_trend = 5000.0

        twitter_max_ubertrend = 0.0
        twitter_min_ubertrend = 100.0

        twitter_max_trend = 0.0
        twitter_min_trend = 100.0

        google_max_ubertrend = 0.0
        google_min_ubertrend = 100.0

        google_max_trend = 0.0
        google_min_trend = 100.0


        for ubertrend in self.ubertrends:
            print(ubertrend)

            if float(ubertrend['twitter'][date]) > twitter_max_ubertrend:
                twitter_max_ubertrend = float(ubertrend['twitter'][date])

            if float(ubertrend['google']['daily'][date]) > google_max_ubertrend:
                google_max_ubertrend = float(ubertrend['google']['daily'][date])

            if float(ubertrend['techCrunch'][date]) > techCrunch_max_ubertrend:
                techCrunch_max_ubertrend = float(ubertrend['techCrunch'][date])

            if float(ubertrend['twitter'][date]) < twitter_min_ubertrend:
                twitter_min_ubertrend = float(ubertrend['twitter'][date])

            if float(ubertrend['google']['daily'][date]) < google_min_ubertrend:
                google_min_ubertrend = float(ubertrend['google']['daily'][date])

            if float(ubertrend['techCrunch'][date]) < techCrunch_min_ubertrend:
                techCrunch_min_ubertrend = float(ubertrend['techCrunch'][date])



            for trend in ubertrend['related_topics']:


                if float(ubertrend['related_topics'][trend]['twitter'].get(date,0)) > twitter_max_trend:
                    twitter_max_trend = float(ubertrend['related_topics'][trend]['twitter'].get(date,0))

                if float(ubertrend['related_topics'][trend]['google']['daily'].get(date,0)) > google_max_trend:
                    google_max_trend = float(ubertrend['related_topics'][trend]['google']['daily'].get(date,0))

                if float(ubertrend['related_topics'][trend]['techCrunch'].get(date,0)) > techCrunch_max_trend:
                    techCrunch_max_trend = float(ubertrend['related_topics'][trend]['techCrunch'].get(date,0))

                if float(ubertrend['related_topics'][trend]['twitter'].get(date,0)) < twitter_min_trend:
                    twitter_min_trend = float(ubertrend['related_topics'][trend]['twitter'].get(date,0))

                if float(ubertrend['related_topics'][trend]['google']['daily'].get(date,0)) < google_min_trend:
                    google_min_trend = float(ubertrend['related_topics'][trend]['google']['daily'].get(date,0))

                if float(ubertrend['related_topics'][trend]['techCrunch'].get(date,0)) < techCrunch_min_trend:
                    techCrunch_min_trend = float(ubertrend['related_topics'][trend]['techCrunch'].get(date,0))


        return techCrunch_max_ubertrend, techCrunch_min_ubertrend, techCrunch_max_trend, techCrunch_min_trend\

            # , \
            #    google_max_ubertrend, google_min_ubertrend, google_max_trend, google_min_trend,twitter_max_ubertrend, \
            # twitter_min_ubertrend, twitter_max_trend, twitter_min_trend



test = DataAggregator()
test.indexer()






