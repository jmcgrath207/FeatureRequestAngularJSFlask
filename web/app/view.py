import random
import string

from flask import render_template, flash, redirect, request,make_response,jsonify
from flask_login import current_user,login_user, logout_user, login_required
from itsdangerous import TimestampSigner
from passlib.hash import bcrypt_sha256

from app import app, db, login_manager
from .config import SECRET_KEY
from .form import LoginForm
from .model import User, Client_View


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    pass

@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def Index():
    """Login portal for clients"""

    if current_user.is_authenticated:
            """If client is authenticated, return them back to their portal case view"""
            return render_template("Client_View.html",title='client_view',
                           Client_id=current_user.Client_id,api_key= current_user.api_key)
    form = LoginForm()
    if (request.method == 'POST') and (form.validate_on_submit()):
        Client_id = form.Client_id.data
        Password = form.Password.data
        user = User.query.filter_by(Client_id=Client_id).first()
        if not user and app.config['NO_PASSWORD'] == True:
            """Allow anyone to create their own account"""
            pass_hash = bcrypt_sha256.encrypt(Password, rounds=12)
            user = User(Client_id= Client_id,Password= pass_hash,api_key='')
            Sample_date = Client_View(client_id = Client_id,
                                         case_name= 'sample case',
                                         priority= '1',
                                         target_date = '10/7/2016',
                                         product_area = 'Engineering',
                                          status = 'In Progress',
                                         description= 'something'
                                         )
            db.session.add(user)
            db.session.commit()
            db.session.add(Sample_date)
            db.session.commit()
        """ If user is a vaild account, proceed with verifying \
        their credentials and provide them the API key"""
        if user:
            if bcrypt_sha256.verify(Password, user.Password) and user.Client_id == Client_id:
                signer = TimestampSigner(SECRET_KEY)
                API_KEY = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(30)])
                user.api_key = signer.sign(API_KEY)
                user.current_login_ip = request.remote_addr
                db.session.commit()
                login_user(user)
                return render_template("Client_View.html",title='client_view',
                                   Client_id=Client_id,api_key= user.api_key)
        if form.errors:
            flash(form.errors, 'danger')
        flash('Incorrect Credentials, please enter the correct Client Id and Password')
        return render_template('Index.html', form=form)
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('Index.html', form=form)


@app.route('/api_key',methods=['POST'])
def api_key():
    """" Request url for API key for Restful API"""

    if request.method == "POST":
        content = request.get_json(silent=True)
        user = User.query.filter_by(Client_id=content['Client_id']).first()
        if not user and app.config['NO_PASSWORD'] == True:
            ##Allow anyone to create their own account
            pass_hash = bcrypt_sha256.encrypt(content['Password'], rounds=12)
            user = User(Client_id= content['Client_id'],Password= pass_hash,api_key='')
            Sample_date = Client_View(client_id = content['Client_id'],
                                         case_name= 'sample case',
                                         priority= '1',
                                         target_date = '10/7/2016',
                                         product_area = 'Engineering',
                                          status = 'In Progress',
                                         description= 'something'
                                         )
            db.session.add(user)
            db.session.commit()
            db.session.add(Sample_date)
            db.session.commit()
        """ If user is a vaild account, proceed with verifying \
        their credentials and provide them the API key"""
        if user:
            if bcrypt_sha256.verify(content['Password'], user.Password) and user.Client_id == content['Client_id']:
                signer = TimestampSigner(SECRET_KEY)
                API_KEY = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(30)])
                user.api_key = signer.sign(API_KEY)
                user.current_login_ip = request.remote_addr
                db.session.commit()
                return make_response(jsonify({'API KEY': user.api_key}), 200)
        return make_response(jsonify({'Failure': 'Incorrect Client id OR Password'}), 400)

@app.route('/logout')
@login_required
def logout():
    """log out url for clients"""

    logout_user()
    flash('You have been logged out successfully')
    return redirect('/')



