from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url('home/', views.home, name='home'),
    url(r'^aaa$', views.view_a, name='view_a'),
	url('welcome/', views.welcome, name='welcome'),
    url('profile_view', views.profile_view, name='profile_view'),
    url('register/', views.register, name='register'),
    url('login_check/', views.login_check, name='login_check'),
    url('profile_update/', views.profile_update, name='profile_update'),
    url('logout_view/', views.logout_view, name='logout_view')

]
