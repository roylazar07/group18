from flask import Blueprint, render_template, request
from utilities.db.db_manager import dbManager
from db_connector import create_contact

# about blueprint definition
contact = Blueprint(
    'contact',
    __name__,
    static_folder='static',
    static_url_path='/contact',
    template_folder='templates'
)


# Routes
@contact.route('/contact', methods = ['GET','POST'])
def index():
    request_method = request.method
    if request.method == "POST":
        full_name = request.form['full-name']
        phone_number = request.form['phone-number']
        email = request.form['email']
        message = request.form['message']
        create_contact(full_name,phone_number,email,message)
        return render_template('contact.html',
            full_name = full_name,
            phone_number = phone_number,
            email = email,
            message = message)
    else:
        return render_template('contact.html')




