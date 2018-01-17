from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
import boto3

# Create your views here.
MY_ACCESS_KEY_ID = ''
MY_SECRET_ACCESS_KEY = ''

dynamodb = boto3.resource('dynamodb', aws_access_key_id = MY_ACCESS_KEY_ID, aws_secret_access_key = MY_SECRET_ACCESS_KEY, region_name='us-east-2')

def workingout(request):
    if request.session.has_key('username'):
     template = loader.get_template("FindExercises/exercises.html")
     table = dynamodb.Table('gymdataset')
     response = table.scan()
     exercises = response['Items']
     Abs = []; Legs = []; Back = []; Chest = []; Abdominals = [];
     Shoulders = []; Biceps = []; Triceps = []; Lats = []; Forearm = [];
     Glutes = []; Middleback = []; Lowerback = []; Neck = [];
     Quardiceps = []; Hamstrings = []; Calves = []; Traps=[];
     for i in exercises:
        if i['category'] == "Abs":
            Abs.append(i)
        if i['category'] == "Legs":
            Legs.append(i)
        if i['category'] == "Back":
            Back.append(i)
        if i['category'] == "Chest":
            Chest.append(i)
        if i['category'] == "Abdominals":
            Abdominals.append(i)
        if i['category'] == "Shoulders":
            Shoulders.append(i)
        if i['category'] == "Biceps":
            Biceps.append(i)
        if i['category'] == "Triceps":
            Triceps.append(i)
        if i['category'] == "Lats":
            Lats.append(i)
        if i['category'] == "Forearm":
            Forearm.append(i)
        if i['category'] == "Quardiceps":
            Quardiceps.append(i)
        if i['category'] == "Hamstrings":
            Hamstrings.append(i)
        if i['category'] == "Calves":
            Calves.append(i)
        if i['category'] == "Glutes":
            Glutes.append(i)
        if i['category'] == "Middle Back":
            Middleback.append(i)
        if i['category'] == "Lower Back":
            Lowerback.append(i)
        if i['category'] == "Neck":
            Neck.append(i)
        if i['category'] == "Traps":
            Traps.append(i)

     context = {
        'Abs' : Abs, 'Legs':Legs , 'Back' : Back, 'Chest' : Chest, 'Abdominals' : Abdominals,
     'Shoulders' : Shoulders, 'Biceps' : Biceps, 'Triceps' : Triceps, 'Lats' : Lats, 'Forearm' : Forearm,
     'Glutes' : Glutes, 'Middleback' : Middleback, 'Lowerback' : Lowerback, 'Neck' : Neck,
     'Quardiceps' : Quardiceps, 'Hamstrings' : Hamstrings, 'Calves' : Calves, 'Traps': Traps,
     }
    else:
        template = loader.get_template("front/login.html")
        context={}
    return HttpResponse(template.render(context, request))
