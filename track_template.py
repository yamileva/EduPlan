from flask import Blueprint
from flask import render_template, redirect, abort, request
from flask_login import login_required, current_user

from models import db_session
from models.__all_models import *
from forms.__all_forms import *


templ = Blueprint('templ', __name__, template_folder='./templates')


@templ.route("/track_templates")
def show_templates():
    session = db_session.create_session()
    templates = session.query(TrackTemplate)
    return render_template("track_templates.html",
                           tlist=templates)