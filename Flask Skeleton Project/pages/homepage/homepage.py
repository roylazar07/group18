from flask import Blueprint
from flask import render_template, redirect, url_for
from db_connector import sign_out_user


# homepage blueprint definition
homepage = Blueprint(
    'homepage',
    __name__,
    static_folder='static',
    static_url_path='/homepage',
    template_folder='templates'
)

sign_out = Blueprint(
    'sign_out',
    __name__,
    static_folder='static',
    static_url_path='/sign_out',
    template_folder='templates'
)

# Routes
@homepage.route('/', methods = ['GET','POST'])
def index():
    return render_template('homepage.html')


@homepage.route('/homepage',methods = ['GET','POST'])
@homepage.route('/home')
def redirect_homepage():
    # print('I am in /Homepage route!')
    return redirect(url_for('homepage.index'))


@sign_out.route('/sign_out', methods = ['GET','POST'])
def index():
    sign_out_user()
    return redirect(url_for('homepage.index'))