from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import Template , Context, loader
from django.shortcuts import render_to_response, render
import boto3
import json
import decimal
from operator import itemgetter
from botocore.exceptions import ClientError

MY_ACCESS_KEY_ID = ''
MY_SECRET_ACCESS_KEY = ''

dynamodb = boto3.resource('dynamodb', aws_access_key_id = MY_ACCESS_KEY_ID, aws_secret_access_key = MY_SECRET_ACCESS_KEY, region_name='us-east-2')

# Create your views here.

def meal_home(request):
    if request.session.has_key('username'):
        template = loader.get_template('FindMeal/meal.html')
        username = request.session['username']
        context ={'username':username}
    else:
        template = loader.get_template('front/login.html')
        context={}
    return HttpResponse(template.render(context, request))


def get_list_of_foods(request):
    try:
        table = dynamodb.Table('fooddata')
    except ClientError as e:
        return e.response['Error']['Message']
    else:
        response = table.scan()
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            try:
                data = response['Items']
                returnlist = []
                bmi = request['stat']
                if bmi == "underweight":
                    newlist = sorted(data, key=itemgetter('protein'), reverse=True)
                    for i in newlist:
                        for k, v in i.items():
                            if k == "food_desc_portion":
                                if (
                                    "DUCK" in v) or "TURKEY" in v or "CHICKEN" in v or "BEEF" in v or "PORK" in v or "EGG" in v:
                                    returnlist.append(i)


                elif bmi == "normal":
                    newlist = sorted(data, key=itemgetter('protein'), reverse=True)
                    for i in newlist:
                        for k, v in i.items():
                            if k == "food_desc_portion":
                                if "CHICKEN" in v or "VEGETABLES" in v or "CORN" in v or "CABBAGE" in v or "BREAD" in v or "APPLES" in v:
                                    returnlist.append(i)

                elif bmi == "overweight":
                    newlist = sorted(data, key=itemgetter('protein'), reverse=True)
                    for i in newlist:
                        for k, v in i.items():
                            if k == "food_desc_portion":
                                if "YOGURT" in v or "BROCCOLI" in v or "LETTUCE" in v or "BEAN" in v or "ORANGES" in v or "VEGETABLE" in v:
                                    returnlist.append(i)

                elif bmi == "obese":
                    newlist = sorted(data, key=itemgetter('protein'), reverse=True)
                    for i in newlist:
                        for k, v in i.items():
                            if k == "food_desc_portion":
                                if "CUCUMBER" in v or "BROCCOLI" in v or "LETTUCE" in v or "BEAN" in v or "BEETS" in v or "VEGETABLE" in v:
                                    returnlist.append(i)
            except KeyError:
                return None

            return returnlist


def retrieve_bmi_parameters(request):
    userid = request.session['username']
    print(userid)
    #userid=request.session['user']
    usertable = dynamodb.Table('users')
    response = usertable.get_item(
        Key={
            'userid': userid,
        }
    )
    params = {}
    print(response)
    params['ht'] = response['Item']['height']
    params['wt'] = response['Item']['weight']
    params['type'] = "html"
    return params


def getValues(request):
    params = {}
    ht = float(request.GET.get('height'))
    wt = float(request.GET.get('weight'))
    userid = request.session['username']
    try:
        usertable = dynamodb.Table('users')
    except ClientError as e:
        return e.response['Error']['Message']
    else:
        response = usertable.update_item(
            Key={
                'userid': userid
            },
            UpdateExpression="set height = :r, weight=:p",
            ExpressionAttributeValues={
                ':r': decimal.Decimal(str(ht)),
                ':p': decimal.Decimal(str(wt))
            }
        )
    params['ht'] = ht
    params['wt'] = wt
    params['type'] = "json"
    return calculate_bmi(params)


def calculate_bmi(request):
    ht = request['ht']
    wt = request['wt']
    bmi_value = wt / (ht * ht)
    bmi_value = float(round(bmi_value, 2))
    if bmi_value < 18.5:
        bmi_stat = "underweight"
    elif bmi_value > 18.5 and bmi_value <= 25:
        bmi_stat = "normal"
    elif bmi_value > 25 and bmi_value <= 30:
        bmi_stat = "overweight"
    elif bmi_value > 30:
        bmi_stat = "obese"

    if request['type'] == "json":
        data = {
            'new_bmi': bmi_stat,
            'bmi_value': bmi_value,
        }
        return JsonResponse(data)
    bmi = {}
    bmi['value'] = bmi_value
    bmi['stat'] = bmi_stat
    return bmi


def allmealplans(request):
    if request.session.has_key('username'):
     template = loader.get_template('FindMeal/allmealplan.html')
     try:
        table = dynamodb.Table('fooddata')
     except ClientError as e:
        return e.response['Error']['Message']
     else:
        response = table.scan()
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            try:
                foods = response['Items']
                context = {
                    'foods': foods
                }
            except KeyError:
                return None
    else:
       template = loader.get_template('front/login.html')
       context ={}
    return HttpResponse(template.render(context, request))


def index(request):
    if request.session.has_key('username'):
     template = loader.get_template('FindMeal/whattoeat.html')
     params = retrieve_bmi_parameters(request)
     bmi = calculate_bmi(params)
     foods = get_list_of_foods(bmi)
     context = {
        'bmi': bmi,
        'params': params,
        'foods': foods
     }
    else:
        template = loader.get_template('front/login.html')
        context = {}
    return HttpResponse(template.render(context, request))
