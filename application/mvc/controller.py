from application.mvc.model import dynamic_join
from flask import Blueprint, render_template

control = Blueprint('control', __name__)

@control.route('/')
@control.route('/home/')
def home():
    return render_template('home.html', 
            cms=control.cms, 
            navbar=control.navbar('home'))

@control.route('/about/')
def about():
    return render_template('about.html', 
            cms=control.cms, 
            navbar=control.navbar('about'))

@control.route('/<stub>/')
def dynamic(stub):
    data = dynamic_join(stub)
    return render_template('theorem.html', 
            cms=control.cms, 
            navbar=control.navbar(f'{stub}'),
            data=data)
