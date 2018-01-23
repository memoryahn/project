from django.urls import path
from . import views
from firebase_admin import credentials
import firebase_admin

cred = credentials.Certificate('C:\\Users\\memor\\Documents\\project\\pyServer\\yurina\\pyserver-ahn-firebase.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://pyserver-ahn.firebaseio.com/'
})    

urlpatterns = [
    path('',views.index,name='yurina'),
    path('getgif/',views.getgif,name='getgif')
    
]