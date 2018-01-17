from django.shortcuts import render
from django.template import Template, Context, loader

# Create your views here.

from django.http import HttpResponse


def index(request):
    if request.session.has_key('username'):
        template = loader.get_template('FindGym/location_gym.html')
        username = request.session['username']
        context ={'username':username}
    else:
        template = loader.get_template('front/login.html')
        context={}
    return HttpResponse(template.render(context, request))