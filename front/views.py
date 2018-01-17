from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import Template, Context, loader
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_protect
import json
import boto3
import hashlib
import requests
import decimal
from decimal import *
from botocore.exceptions import ClientError
from django.contrib.auth import logout
import boto3


MY_ACCESS_KEY_ID = ''
MY_SECRET_ACCESS_KEY = ''


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


dynamodb = boto3.resource('dynamodb', aws_access_key_id=MY_ACCESS_KEY_ID, aws_secret_access_key=MY_SECRET_ACCESS_KEY,
                          region_name='us-east-2')
table = dynamodb.Table('users')

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request, "front/login.html")


def welcome(request):
    username = request.GET.get('username')
    request.session['username'] = username
    data = {
        'checks': "yes"
    }
    return JsonResponse(data)


def home(request):
    if request.session.has_key('username'):
        template = loader.get_template('front/index.html')
        username = request.session['username']
        context ={'username':username}
    else:
        template = loader.get_template('front/login.html')
        context={}
    return HttpResponse(template.render(context, request))


def view_a(request):
    return render(request, "front/register.html")


def profile_view(request):
    return render(request, "front/profile.html")


@csrf_protect
def register(request):
    userid = str(request.GET.get('username'))
    givenname = str(request.GET.get('givenname'))
    email = str(request.GET.get('email'))
    password = str(request.GET.get('password'))
    phonenumber = str(request.GET.get('phonenumber'))

    url2 = str(request.GET.get('url2'))
    print(url2)

    try:

        hash_object = hashlib.sha256(password.encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        response = table.put_item(
            Item={
                'userid': userid,
                'email': email,
                'givenname': givenname,
                'password': hex_dig,
                'phonenumber': phonenumber
            }
        )
        print("Added " + str(userid))
        data = {
            'user_id': "pass"
        }
        url2 = str(url2) + str(phonenumber)
        session = requests.Session()
        session.trust_env = False
        response1 = session.get(url2)
    except:

        pass

    return JsonResponse(data)


@csrf_protect
def login_check(request):
    user = str(request.GET.get('user'))
    # request.session['user']=user
    password = str(request.GET.get('password'))

    try:
        response = table.get_item(
            Key={
                'userid': user
            }
        )
    except:
        print("User Id doesn't exist")
        data = {
            'user_id': "not"
        }

    else:
        try:
            item = response['Item']
            print("GetItem succeeded:")
            print(json.dumps(item, indent=4, cls=DecimalEncoder))
            print(str(item['userid']) + str(item['password']))
            hash_object = hashlib.sha256(str(password).encode('utf-8'))
            hex_dig = hash_object.hexdigest()

            if hex_dig == item['password'] and user == item['userid']:
                print("successful")  # do something here...............................
                data = {
                    'user_id': user
                }
            else:
                print("Login Failed")
                data = {
                    'user_id': "not"
                }

        except:
            print("User Id Invalid, Please Check")
            data = {
                'user_id': "not"
            }

    return JsonResponse(data)


def profile_update(request):
    if request.session.has_key('username'):
     height = request.GET.get('height')
     weight = request.GET.get('weight')
     likes = request.GET.get('likes')
     goal = request.GET.get('goal')
     userid = request.session['username']
     print(userid)
     try:
        usertable = dynamodb.Table('users')
     except ClientError as e:
        return e.response['Error']['Message']
     else:
        response = usertable.update_item(
            Key={
                'userid': userid
            },
            UpdateExpression="set height = :a, weight = :b, likes = :c, goal = :d",
            ExpressionAttributeValues={
                ':a': decimal.Decimal(str(height)),
                ':b': decimal.Decimal(str(weight)),
                ':c': str(likes),
                ':d': str(goal),

            }
        )

     data = {
        'height': height,
        'weight': weight,
        'likes': likes,
        'goal': goal,
        'userid': userid,

     }
    else:
        data = {}
    return JsonResponse(data)

def logout_view(request):
    logout(request)
    return render(request, "front/login.html")
