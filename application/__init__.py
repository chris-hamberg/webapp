from flask import Flask, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user
from application.mvc.model import User
import application.dbhelper
from application.crypt import EncryptedPass

k = ('BuYrfTu/w6RfsOJhHfW9ILFlfQx7zVW6oi2LRXj32ICf8c49VGMLk3sNjO0AhugS8/qH37'
     '+g4v41vUCTQFVCVERQhgFmoCBk13X')

app = Flask(__name__)
app.secret_key = k
login_manager = LoginManager(app)
application.dbhelper.populate()

from application.mvc.controller import control
app.register_blueprint(control)

encrypted = EncryptedPass()

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    passw = request.form.get('passw')
    encrypted_pass = User.password(email)
    if encrypted_pass and encrypted.validate(
            passw, encrypted_pass['salt'], encrypted_pass['hash']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('control.twitter'))
    return redirect(url_for('control.home'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('control.home'))

@login_manager.user_loader
def load_user(email):
    encrypted_pass = User.password(email)
    if encrypted_pass:
        return User(email)
