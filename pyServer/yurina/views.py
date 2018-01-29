from django.shortcuts import render
from django.http import HttpResponse
import urllib.request
from bs4 import BeautifulSoup
from firebase_admin import db


def getgif(request):
    return HttpResponse('gg')        

def index(request):    
    with urllib.request.urlopen('http://mlbpark.donga.com/mp/b.php?p=1&m=search&b=bullpen&query=gif&select=sct&user=') as url:
        content = url.read()
        soup = BeautifulSoup(content, 'html.parser')
    bullpen = soup.find_all('a')
    data = []
    resp = []
    idx = 0
    pydb = db.reference('getgif')

    # for d in data:
    #     newkey = pydb.child(d['number']).update(d)
    # vv = pydb.order_by_value()
    redata = pydb.order_by_key().limit_to_last(15).get()
    dataTitle=[]
    if redata != None:
        for f in redata:
            sr=[]
            try:
                for ss in redata[f]['srcs']:
                    sr.append(ss)
            except:
                print('error')
            dataTitle.append({'title':redata[f]['title'],'srcs':sr,'number':redata[f]['number']})
            # print(redata[f]['title'])
    dataTitle.reverse()
    return render(request, 'home.html', {'data': data,'title':dataTitle})