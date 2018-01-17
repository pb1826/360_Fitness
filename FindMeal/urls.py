from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^meal_home/', views.meal_home, name='meal_home'),
    url('index', views.index, name='index'),
	url('getValues/', views.getValues, name='getValues'),
	url(r'^allmealplans/', views.allmealplans, name='allmealplans'),


]
