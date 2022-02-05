from datetime import date
from flask import Blueprint
# Tor Erik og Johnny
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flask import current_app

bp = Blueprint("page", __name__)

@bp.route("/page/personvern")
def privacy():  
    return render_template("personvern.html")

@bp.route("/page/om-oss")
def about():  
    return render_template("om_oss.html")
