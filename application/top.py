# Robin og Emil
from typing import Tuple
from datetime import date
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flask import current_app
from .db import get_top_users

bp = Blueprint("top", __name__)

def check_interval(interval: str) -> Tuple[str, str]:
    if interval == 'year':
        date_from = date.today().replace(day=1, month=1)
        date_to = date.today()

    elif interval == 'month':
        date_from = date.today().replace(day=1)
        date_to = date.today()
    
    return date_from, date_to

@bp.route("/top/")
@bp.route("/top/<interval>")
def top_index(interval='year'):
    
    date_from, date_to = check_interval(interval)
    top_users = get_top_users(date_from, date_to)
    
    top_users_year = get_top_users(date.today().replace(day=1, month=1), date.today())
    top_users_month = get_top_users(date.today().replace(day=1), date.today())
    # TODO: Finn ut hvordan en finner første dato i inneverende uke
    top_users_week = get_top_users(date.today().replace(day=1), date.today())


    return render_template('top.html', **locals())
