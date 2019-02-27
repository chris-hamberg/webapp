import application.dbhelper
application.dbhelper.populate()

from flask_login import LoginManager, login_user, logout_user
from flask import Flask, redirect, url_for, request
from application.navigation import navbar, cms
from application.crypt import EncryptedPass
from application.mvc.model import User
from flask import send_from_directory

k = ('BuYrfTu/w6RfsOJhHfW9ILFlfQx7zVW6oi2LRXj32ICf8c49VGMLk3sNjO0AhugS8/qH37'
     '+g4v41vUCTQFVCVERQhgFmoCBk13X')

app = Flask(__name__)
app.config['CUSTOM_STATIC_PATH'] = 'data'
app.secret_key = k
login_manager = LoginManager(app)

from application.mvc.controller import control
from application.mvc.apps import applications
app.register_blueprint(control)
app.register_blueprint(applications)

applications.navbar = navbar
control.navbar = navbar
applications.cms = cms
control.cms = cms

encrypted = EncryptedPass()

@app.route('/application/data/<path:filename>')
def data(filename):
    '''
    REF
    https://stackoverflow.com/questions/9513072/more-than-one-static-path-in-local-flask-instance
    '''
    return send_from_directory(app.config['CUSTOM_STATIC_PATH'], filename)

@app.route('/login/', methods=['POST', 'GET'])
def login():
    email = request.form.get('email')
    passw = request.form.get('passw')
    encrypted_pass = User.password(email)
    if encrypted_pass and encrypted.validate(
            passw, encrypted_pass['salt'], encrypted_pass['hash']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('applications.twitter'))
    return redirect(url_for('control.home'))

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('control.home'))

@login_manager.user_loader
def load_user(email):
    encrypted_pass = User.password(email)
    if encrypted_pass:
        return User(email)
