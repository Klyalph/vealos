# Elias og Kaseper
from datetime import date, datetime
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_manager, login_user, logout_user, login_required, LoginManager, UserMixin, current_user
from werkzeug.exceptions import abort
from flask import current_app
from application.db import get_db
from .auth import User

bp = Blueprint("user", __name__)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@bp.route("/user/<int:userId>")
@bp.route("/user/")
def index(userId=None):  
    db = get_db()

    if userId is None:
        return redirect(url_for('index.index'))

    user = db.execute('SELECT * FROM users WHERE id = ?', (str(userId))).fetchone()
    tours = db.execute('SELECT * FROM tours WHERE user_id = ?', (str(userId))).fetchall()

    # Sjekk om de samme variablene går i **locals()
    totalTours = len(tours)
    toursThisYear = 0
    currentYear = str(datetime.now().year)
    toursThisYear = len([tour for tour in tours 
                         if datetime.strftime(tour['tour_date'], 'Y%') == currentYear])
   
    return render_template("user/user.html", **locals())

@bp.route("/edit-user/<int:userId>")
def edit(userId=None):
    userId = str(userId)
    db = get_db()
    if current_user.is_authenticated:
        try:
            user = db.execute('SELECT * FROM users WHERE id = ?', (userId)).fetchone()
        except Exception as e:
            print(e)
            return redirect('/')

        return render_template("user/edit-user.html", **locals())

    return redirect('/')

@bp.route("/update-user/<int:userId>", methods=["POST"])
def update(userId=None):
    userId = str(userId)
    db = get_db()
    
    if current_user.is_authenticated:
        updatedUsername = request.form['updated_username']
        updatedEmail = request.form['updated_email']
        db.execute('''
                UPDATE users 
                SET username = ?, 
                email = ? 
                WHERE id = ?''',
                (updatedUsername, updatedEmail, userId)
                )
        db.commit()

    return redirect(url_for('user.index', userId=userId))
