from django.shortcuts import render
# Create your views here.
# import firebase_admin
from firebase import firebase
from django.http import HttpResponse


def index(request):
    # cred = credentials.Certificate('C:\\Users\\memor\\Documents\\project\\pyServer\\yurina\\pyserver-ahn-firebase.json')
    # pyFirebase = firebase_admin.initialize_app(credential=cred, options=None, name='pyServer')    
    # print(pyFirebase.name)  
    fireapp = firebase.FirebaseApplication('https://pyserver-ahn.firebaseio.com/')
    result = fireapp.get('name',None)
    # result='a'
    return render(request, 'home.html', {'data': result})
    # return HttpResponse(result)        