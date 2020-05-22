import googlesearch
import requests
import re
from dbInterface import DBInterface

class RelatedTopics():

    DBInterface.initialize('eotm')
    ubertrends = DBInterface.find('ubertrends')

    # if 'related topics' in DBInterface.find_one('ubertrends', {'trend':'AI'}):
    #     print('has duplicates')
    # else: print('will write to db')

    trends = []
    for item in ubertrends:
        trends.append(item['trend'])


    print(trends)

    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"

    def get_section_id(self, title):
        """ get the section id of any page 
        """
        params_Section_id = {
            'action': "parse",
            'page': title,
            'prop': 'sections',
            'format': "json"
        }
        res = self.S.get(url=self.URL, params=params_Section_id)
        data = res.json()
        list_sections = data['parse']['sections']
        section_id = next(item for item in list_sections if item['anchor']=='See_also')['index']

        return section_id


    def get_relevant_topics(self, title):

        section_id = self.get_section_id(title=title)

        params_Section = {

            'action': "parse",
            'page': title,
            'prop': 'wikitext',
            'section': section_id,
            'format': "json"

        }

        res = self.S.get(url=self.URL, params=params_Section)
        data = res.json()
        sections = data['parse']['wikitext']['*']
        formated_sections = sections.split('\n')
        #print(formated_sections)
        formated_sections = [x for x in formated_sections if '*' in x]

        '''here we remove special characters from related topics'''
        formated_sections = [re.sub('[^A-Za-z0-9\s]+', '', x) for x in formated_sections]
        related_topics = [x.strip() for x in formated_sections]
        return related_topics



    def initiateSearch(self):

        for ubertrend in self.trends:
            url = list(googlesearch.search(query=ubertrend + ' wikipedia', lang='en', num=1, stop=1, tld='com'))[0]
            title = url.split('/')[-1]
            related_keywords = self.get_relevant_topics(title=title)
            if 'related topics' in DBInterface.find_one('ubertrends', {'trend': ubertrend}):
                print('related topics already exist.')
                pass
            else:
                print('found the related topics to trend '+ ubertrend + ', now writing the results to DB')
                DBInterface.update_one('ubertrends', {'trend': ubertrend}, {'related_topics': related_keywords})

        print('done writing the related topics!')



relatedTopics = RelatedTopics()
relatedTopics.initiateSearch()
