from django.shortcuts import render
# Create your views here.
# import firebase_admin
from django.http import HttpResponse
import urllib.request
from bs4 import BeautifulSoup
import json
import firebase_admin
from firebase_admin import db
import re

def index(request):
    # cred = credentials.Certificate('C:\\Users\\memor\\Documents\\project\\pyServer\\yurina\\pyserver-ahn-firebase.json')
    # pyFirebase = firebase_admin.initialize_app(credential=cred, options=None, name='pyServer')    
    # print(pyFirebase.name)  
    # fireapp = firebase.FirebaseApplication('https://pyserver-ahn.firebaseio.com/')
    # result = fireapp.get('name',None)
    # result='a'
    return render(request, 'home.html', {'data': result})
    # return HttpResponse(result)        

def getgif(request):    
    with urllib.request.urlopen('http://mlbpark.donga.com/mp/b.php?p=1&m=search&b=bullpen&query=gif&select=sct&user=') as url:
        content = url.read()
        soup = BeautifulSoup(content, 'html.parser')
    bullpen = soup.find_all('a')
    data = []
    resp = []
    idx = 0    
    for s in bullpen:
        try:
            prop =s.get('class')
            if prop != None and prop[0] == "bullpenbox":
                resp.append(s.get('href'))
                # print(s.get('href'))                             
        except UnicodeEncodeError: 
            print("Errror : %d" % (idx))
        idx += 1   
    linkCount=0
    idx2=0
    # for link in resp:
    # # try:
    #     print(str(idx2))
    #     with urllib.request.urlopen(link) as url:
    #         content = url.read()
    #         soup = BeautifulSoup(content, 'html.parser')    
    #     titles =  soup.find('div',{'class':'titles'})                
    #     gifUrl =  soup.find_all('img')    
    #     artdate =  soup.find_all('em')
    #     srcs = []            
    #     number = 1
    #     for art in artdate:
    #         # print(art.get_text()+'a')
    #         if '2018' in str(art.get_text):
    #             number = art.get_text()
    #             print(number)
    #     for i in gifUrl:
    #         if 'dimg' not in i.get('src') and 'image' not in i.get('src'):
    #             srcs.append(i.get('src'))                                        
    #     data.append({'title':titles.get_text(),'srcs':srcs,'number':number})
    #     idx2 += 1                        

        # if titles.get_text() != None:         
        #     doc[i]={'title':titles.get_text(),'url':}
        # linkCount += 1
        
    # except:
    #     print('error')   
    
    


    pydb = db.reference('getgif/')
    # for d in data:
    #     newkey = pydb.push(d)
    redata = pydb.get()    
    dataTitle=[]
    for f in redata:
        dataTitle.append(redata[f]['title'])
        print(redata[f]['title'])
    last =db.Query.equal_to('기량')
    print(last)
    return render(request, 'home.html', {'data': data,'title':dataTitle})
    # return HttpResponse('a')