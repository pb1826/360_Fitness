from __future__ import print_function
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
import boto3
import webbrowser
MY_ACCESS_KEY_ID = ''
MY_SECRET_ACCESS_KEY = ''

dynamodb = boto3.resource('dynamodb', aws_access_key_id = MY_ACCESS_KEY_ID, aws_secret_access_key = MY_SECRET_ACCESS_KEY, region_name='us-east-2')


def buddysearch(request):
    if request.session.has_key('username'):
        template = loader.get_template('FindBuddy/buddy.html')
        username = request.session['username']
        context ={'username':username}
    else:
        template = loader.get_template('front/login.html')
        context={}
    return HttpResponse(template.render(context, request))


def chatwithbuddy(request):
    if request.session.has_key('username'):
        return redirect("url")
    else:
        template = loader.get_template('front/login.html')
        context={}
    return HttpResponse(template.render(context, request))

def buddyinfo(request):
    if request.session.has_key('username'):
     template = loader.get_template('FindBuddy/buddyinfo.html')
     table = dynamodb.Table('users')
     response = table.scan()
     users = response['Items']
     buddy = []
     friends ={}
     for i in users:
        friends['userid'] = str(i['userid'])
        try:
            friends['height'] = str(i['height'])
            friends['weight'] = str(i['weight'])
            friends['likes'] = str(i['likes'])
        except KeyError:
            pass
        buddy.append(friends.copy())
     print(buddy)
     context = {
        "buddy": buddy,
     }
    else:
       template = loader.get_template('front/login.html')
       context ={}
    return HttpResponse(template.render(context, request))
