CloudProject - 360 Fitness

In this fast paced world, you don’t want to have multiple applications for multiple services related to a single task. 360 Fitness, will give you access to everything related to workout/ gym just by a single click.

https://www.youtube.com/watch?v=1ZcpszaKIbU

A user will get access to below services of our platform:
Find Gym:

Finds location of gyms in the vicinity of your selected radius
Search is based on user IP using Google API and various callback methods
Providing reverse geocoding, goelocation, autocomplete search, searchbox, place autocomplete, markers and direction features

Find Buddy:

Chat with your Buddy using our custom Social Media Platform and see who’s available for a workout
Using 'Let's Chat' application to provide real time chat features for all users in the application database
Hosted on Ec2 instance (Ubuntu AMI) using nodejs to run the server and mongodb as database

Find Exercise:

Exhaustive list of exercises based on categories to choose from
Dataset of exercises stored in DynamoDB

Find Meals:

Exhaustive list of meals/food description and portion along with calorie, fat, protein and carbohydrate count
Dataset of food items stored in DynamoDB
Displays recommended food intake for a user based on their BMI

Additional Feature:

SMS sent to new user confirming application registration
Python script triggers API Gateway which in turn triggers lambda function that makes rest call to Twilio API, which sends
message to user's registred number

AWS Lex to interact with either Twilio for offline information about all the exercises and how to do them or online by integrating
Lex with Facebook Messenger app.
