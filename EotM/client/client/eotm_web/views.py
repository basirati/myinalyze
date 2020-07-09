from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import sys
sys.path.append('/Users/vaheh/Downloads/Thesis/myinalyze/EotM/client/')
from dataAggregator import DataAggregator


getData = DataAggregator()
trends = getData.indexer()
# trends_dict = {}
#
# j=0
# for trend in trends:
#     trends_dict[j] = trend
#     j+=1

#print(trends_dict)
ubertrends={}

for obj in trends:
    for key, value in obj.items():
        if key not in ['related_topics']:
            ubertrends[key] = value

print('this is ubertrends', ubertrends)


def index(request):
    template = loader.get_template('eotm-web/index.html')
    return HttpResponse(template.render())

def webview(request):
    template = loader.get_template('eotm-web/trends.html')
    context = {'trends_list': ubertrends,}
    return render(request, 'eotm-web/trends.html', context)

def trend(request, trend):
    get_relatedTopicsOfTrend={}

    for obj in trends:
        for key, values in obj.items():
            if key==trend:
                for key, value in obj['related_topics'].items():
                    get_relatedTopicsOfTrend[key] = value

    print(get_relatedTopicsOfTrend)

    template = loader.get_template('eotm-web/trends.html')
    context = {'trends_list': get_relatedTopicsOfTrend, }

    return render(request, 'eotm-web/trends.html', context)

# Create your views here.
