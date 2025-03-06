import os
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import session
from flask import flash
from datetime import datetime
from datetime import date

# get your uri from .env file
uri = os.environ.get('mongodb+srv://barakeyal100:sOcTBmPZ7lCAdBx0@web-project-cluster.uiphk.mongodb.net/')

# create cluster
cluster = MongoClient('mongodb+srv://barakeyal100:sOcTBmPZ7lCAdBx0@web-project-cluster.uiphk.mongodb.net/', server_api=ServerApi('1'))

# get all dbs and collestions that needed
mydatabase = cluster['mydatabase']

####################################### Users Cluster
user_col = mydatabase['users']


### Create users
def create_user(first_name,last_name,nickname,email,phone_number,birth_day,birth_month, birth_year):
    my_dict = {"First_Name":first_name,"Last_Name":last_name,"Nickname":nickname,"Email":email,"Phone_Number": phone_number,
            "Birth_Day":birth_day,"Birth_Month":birth_month,"Birth_Year":birth_year}
    user_col.insert_one(my_dict)
    session["Logged_in"] = True
    session["Email"] = email

### Log in
def sign_in(phone_number_in,email_in):
    user = mydatabase.collection.find_one({"phone_number": phone_number_in})
    User_list = user_col.find({'Email': email_in})
    User_list = list(User_list)
    if len(User_list) > 0 and User_list[0]["Phone_Number"] == phone_number_in:      
        # If the user exists this function returns True
        session["Logged_in"] = True
        session["Email"] = email_in
        return True
    return False

## Sign Out
def sign_out_user():
    session["Logged_in"] = False
    session.pop("Email", None)



### Check for existing user
def Does_User_Exist(Email_in):
    User_list = user_col.find({'Email': Email_in})
    print(User_list)
    if len(list(User_list)) > 0:
        return True
    else:
        return False


####################################### Contacts Cluster
contact_col = mydatabase['contacts']

### Create contact
def create_contact(full_name,phone_number,email,message):
    my_dict = {'Full_Name':full_name,'Phone_Number': phone_number, 'Email': email,'Message':message}
    contact_col.insert_one(my_dict)



####################################### Workouts Cluster
workouts_col = mydatabase['workouts']

### Create workouts
def create_workout(training_type,training_date,training_time):
    my_dict = {"Email":session.get('Email'),
        "training_type": training_type,
        "training_date": training_date,
        "training_time": training_time}
    workouts_col.insert_one(my_dict)


## Find Workouts
def find_workouts():
    return  workouts_col.find({'Email': session["Email"]})

## Delete Workouts
def del_workout(Wtype,Wdate,Wtime):
    workouts_col.delete_one({'Email': session["Email"],'training_type':Wtype,
        'training_date':Wdate,'training_time':Wtime})

## Update Workout
def update_workout(Wtype,Wdate,Wtime,newTime,newDate):
    workouts_col.update_one({'Email': session["Email"],'training_type':Wtype,
        'training_date':Wdate,'training_time':Wtime},
        {'$set' : {'training_date':newDate,'training_time':newTime}}
        )

## Checking if a workout is already booked
def isBooked(Wtime,Wdate):
    workout = workouts_col.find({'Email': session["Email"],'training_date':Wdate,'training_time':Wtime})
    if len(list(workout))>0:
        return True
    else:
        return False

## Counts how many people signed up for one specific workout
def count_workouts(Wtype,Wtime,Wdate):
    return workouts_col.count_documents({'training_type':Wtype,'training_date':Wdate,'training_time':Wtime})

## Deletes Past Workouts
def del_past_workouts(Wtype,Wtime,Wdate):
    date_format = '%Y-%m-%d'
    now = str(datetime.today().date())
    today = datetime.strptime(str(now), date_format) 

    if today >= datetime.strptime(Wdate, date_format):
        workouts_col.delete_one({'Email': session["Email"],'training_type':Wtype,
        'training_date':Wdate,'training_time':Wtime})


##################### Prints all collections for Analyze.py

def print_all(): ## Prints contacts

    print("Contacts collections: ")
    contacts_list = list(contact_col.find())
    for contact in contacts_list:
        print(contact)
    
    print("Users collections: ") ## Prints users
    users_list = list(user_col.find())
    for user in users_list:
        print(user)
    
    print("Workouts collections: ") ## Prints workouts
    workouts_list = list(workouts_col.find())
    for workout in workouts_list :
        print(workout)










