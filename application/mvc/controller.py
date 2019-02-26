from application.mvc.model import Category, Subject, Theorem, Plot, dynamic_join
from flask import Blueprint, render_template
from flask_login import login_required
from collections import namedtuple

control = Blueprint('control', __name__)

def namespace(active):
    ''' Dynamic navbar '''
    navbar = ('Home', 'About')
    return [{
        'name':name.title(), 'url':f'{name}'.lower(), 
        'active':name.lower() == active} for name in navbar
        ]

content_tree = {'subject':Subject.query(), 'category':Category.query()}

@control.route('/')
@control.route('/home')
def home():
    return render_template('index.html', 
            content_tree=content_tree, 
            pages=namespace('home'))

@control.route('/about')
def about():
    return render_template('index.html', 
            content_tree=content_tree, 
            pages=namespace('about'))

@control.route('/<stub>')
def dynamic(stub):
    data = dynamic_join(stub)
    return render_template(f'theorem.html', 
            content_tree=content_tree, 
            pages=namespace(f'{stub}'),
            data=data)

@control.route('/twitter')
@login_required
def twitter():
    return "You are logged in!"
