from django.urls import path
from . import views
from firebase_admin import credentials
import firebase_admin
import os
from django.views.generic import TemplateView

cred = credentials.Certificate(os.environ['firebaseToken'])
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://pyserver-ahn.firebaseio.com/'
})    

urlpatterns = [
    path('',TemplateView.as_view(template_name='index.html'), name='index'),
    path('getgif/',views.getgif,name='getgif')
    
]