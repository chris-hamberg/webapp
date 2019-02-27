from flask import Blueprint, render_template
from flask_login import login_required

applications = Blueprint('applications', __name__)

@applications.route('/reuters/')
def reuters():
    return render_template('reuters.html',
            cms=applications.cms,
            navbar=applications.navbar('reuters'))

@applications.route('/twitter/')
@login_required
def twitter():
    return render_template('twitter.html',
            cms=applications.cms,
            navbar=applications.navbar('twitter'))
