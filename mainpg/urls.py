from django.urls import path
from . import views

app_name='mainpg'
urlpatterns = [
    path('', views.mainpg, name='mainpg')
]
