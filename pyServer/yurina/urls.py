from django.urls import path
from . import views
from firebase_admin import credentials
import firebase_admin
import os

cred = credentials.Certificate(os.environ['firebaseToken'])
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://pyserver-ahn.firebaseio.com/'
})    

urlpatterns = [
    path('',views.index,name='yurina'),
    path('getgif/',views.getgif,name='getgif')
    
]