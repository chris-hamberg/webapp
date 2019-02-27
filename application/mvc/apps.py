from flask import Blueprint, render_template
from flask_login import login_required
import sys

sys.path.append('application/data/Applications')
from application.data.Applications.reuters import Reuters

applications = Blueprint('applications', __name__)

@applications.route('/reuters/')
def reuters():
    return render_template('reuters.html',
            cms=applications.cms,
            navbar=applications.navbar('reuters'),
            reuters=Reuters())

@applications.route('/twitter/')
@login_required
def twitter():
    return render_template('twitter.html',
            cms=applications.cms,
            navbar=applications.navbar('twitter'))
