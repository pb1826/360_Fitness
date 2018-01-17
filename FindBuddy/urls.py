from django.conf.urls import url
from . import views

urlpatterns = [
    url('buddysearch/', views.buddysearch, name='buddysearch'),
    url('chatwithbuddy/', views.chatwithbuddy, name='chatwithbuddy'),
    url('buddyinfo/', views.buddyinfo, name='buddyinfo')


]