from flask import Blueprint
from flask import render_template, redirect, url_for, request
from utilities.db.db_manager import dbManager
from db_connector import create_user
from db_connector import Does_User_Exist
from db_connector import sign_in
from flask import session
from flask import flash


# homepage blueprint definition
signin = Blueprint(
    'signin',
    __name__,
    static_folder='static',
    static_url_path='/signin',
    template_folder='templates'
)

# Routes
@signin.route('/signin', methods = ['GET','POST'])
def index():
    message = ""
    session['Logged_in'] = False # Init Logged in var in session, False before a user is logged in
    request_method = request.method
    if request.method == "POST":
        email = request.form['email']
        phone_number = request.form['phone-number']
        if sign_in(phone_number, email):
            return redirect(url_for('homepage.index'))
        else:
            return render_template('signin.html',message = "This user doesn't exists or your details are invalid")
    else:
        return render_template('signin.html',message = message)


