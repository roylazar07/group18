from flask import Blueprint, render_template, request, redirect, url_for
from utilities.db.db_manager import dbManager
from utilities.db.db_manager import cluster
from db_connector import create_workout
from flask import session
from db_connector import find_workouts
from db_connector import del_workout
from db_connector import isBooked
from db_connector import update_workout
from db_connector import count_workouts
from db_connector import del_past_workouts
from datetime import datetime
from datetime import date





# catalog blueprint definition
catalog = Blueprint('catalog', __name__, static_folder='static', static_url_path='/catalog', template_folder='templates')
catalog_cancel = Blueprint('catalog_cancel', __name__, static_folder='static', static_url_path='/catalog_cancel', template_folder='templates')
catalog_update = Blueprint('catalog_update', __name__, static_folder='static', static_url_path='/catalog_update', template_folder='templates')

#
mydb  = cluster["trainings"]




# Routes
@catalog.route('/catalog',methods=['GET','POST'])
def index():
    workouts = []
    if session["Logged_in"]:
        user_workouts = find_workouts()
        workouts = list(user_workouts)
        for workout in workouts:
            # Counts people signed up in DB (MUST BE FIRST)
            workout['people'] = count_workouts(workout['training_type'],workout['training_time'],workout['training_date'])
            # Deletes workouts that have happened already
            del_past_workouts(workout['training_type'],workout['training_time'],workout['training_date'])
            # Reverses date for presenting
            workout['training_date'] = datetime.strptime(workout['training_date'], "%Y-%m-%d").strftime("%d-%m-%Y")


    request_method = request.method
    if request.method == "POST" and session["Logged_in"]==False:
        training_type = request.form['training-type']
        training_date = request.form['training-date']
        training_time = request.form['training-time']
        return render_template('catalog.html',request_method = request_method,training_type = training_type,training_date = training_date,
            training_time = training_time,workouts = workouts,message = "Please sign in or create an account")

    #request_method = request.method
    if request.method == "POST" and session["Logged_in"]:
        training_type = request.form['training-type']
        training_date = request.form['training-date']
        training_time = request.form['training-time']
        for workout in workouts:
            # Counts people signed up in DB (MUST BE FIRST)
            workout['people'] = count_workouts(workout['training_type'],workout['training_time'],workout['training_date'])
            # Reverses date for presenting
            #workout['training_date'] = datetime.strptime(workout['training_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
        if count_workouts(training_type,training_time,training_date) >= 30:
            return render_template('catalog.html',request_method = request_method,training_type = training_type,training_date = training_date,
            training_time = training_time,workouts = workouts,message = "We are fully booked for this time and date, please select a different time")
        if isBooked(training_time,training_date) == False:
            create_workout(training_type,training_date,training_time)
            user_workouts = find_workouts()
            workouts = list(user_workouts)
            for workout in workouts:
                # Counts people signed up in DB (MUST BE FIRST)
                workout['people'] = count_workouts(workout['training_type'],workout['training_time'],workout['training_date'])
                # Reverses date for presenting
                workout['training_date'] = datetime.strptime(workout['training_date'], "%Y-%m-%d").strftime("%d-%m-%Y")
            return render_template('catalog.html',request_method = request_method,training_type = training_type,training_date = training_date,
            training_time = training_time,workouts = workouts)
        else:
            user_workouts = find_workouts()
            workouts = list(user_workouts)
            for workout in workouts:
                # Counts people signed up in DB (MUST BE FIRST)
                workout['people'] = count_workouts(workout['training_type'],workout['training_time'],workout['training_date'])
                # Reverses date for presenting
                workout['training_date'] = datetime.strptime(workout['training_date'], "%Y-%m-%d").strftime("%d-%m-%Y")

            return render_template('catalog.html',request_method = request_method,training_type = training_type,training_date = training_date,
            training_time = training_time,workouts = workouts,message = "You are already booked for a workout during this date and time")
    return render_template('catalog.html',workouts = workouts)

@catalog_cancel.route('/catalog_cancel',methods=['GET','POST'])
def index():
    request_method = request.method
    workouts = []
    if session["Logged_in"]:
        user_workouts = find_workouts()


    training_type = request.form['training-type']
    training_date = request.form['training-date']
    ## Reverses date back for search
    training_date = datetime.strptime(training_date, "%d-%m-%Y").strftime("%Y-%m-%d")
    training_time = request.form['training-time']
    del_workout(training_type,training_date,training_time)
    return redirect(url_for('catalog.index'))

@catalog_update.route('/catalog_update',methods=['GET','POST'])
def index():
    if session["Logged_in"]:
        user_workouts = find_workouts()
        workouts = list(user_workouts)
        for workout in workouts:
            # Counts people signed up in DB (MUST BE FIRST)
            workout['people'] = count_workouts(workout['training_type'],workout['training_time'],workout['training_date'])
            # Reverses date for presenting
            workout['training_date'] = datetime.strptime(workout['training_date'], "%Y-%m-%d").strftime("%d-%m-%Y")

    request_method = request.method
    training_type = request.form['training-type']
    training_date = request.form['training-date']
    training_time = request.form['training-time']
    training_date_new = request.form['training-date-new']
    training_time_new = request.form['training-time-new']

    ## Reverses date back for search
    training_date = datetime.strptime(training_date, "%d-%m-%Y").strftime("%Y-%m-%d")

    ## Checking if there is space in the workout
    if count_workouts(training_type,training_time_new,training_date_new) >= 30:
            return render_template('catalog.html',request_method = request_method,training_type = training_type,training_date = training_date,
            training_time = training_time,workouts = workouts,message = "We are fully booked for this time and date, please select a different time")

    ## Checking if a workout already exists in this date and time
    if isBooked(training_time_new,training_date_new):
            return render_template('catalog.html',request_method = request_method,training_type = training_type,training_date = training_date,
            training_time = training_time,workouts = workouts,message = "You are already booked for a workout during this date and time")

    update_workout(training_type,training_date,training_time,training_time_new,training_date_new)
    return redirect(url_for('catalog.index'))
