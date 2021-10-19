# Victor og Pelle
from datetime import date
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
from werkzeug.security import generate_password_hash, check_password_hash
from .db import close_db, get_user, get_user_by_email
from application import login_manager

class User(UserMixin):
    @staticmethod
    def get(user_id):
        user = User()
        user_row = get_user(user_id)
        user.id = user_row['id']
        return user


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

bp = Blueprint("auth", __name__)

@bp.route("/register", methods =["GET", "POST"])
def register():
    ready = False
    if request.method == 'POST':
        user_name = request.form.get("user_name")
        user_email = request.form.get("user_mail")
        user_password = request.form.get("user_pass")
        user_type = request.form.get("user_type")
        db = get_db()

        if user_name == None or user_email == None or user_password == None:
            ready = False
            flash("Du må fylle inn alle rutene")
        else:
            ready = True

        if user_type == 'yes':
            user_visible = 0
        else:
            user_visible = 1

        if ready == True:
            db.execute("INSERT INTO users(username, email, password, visible) VALUES(?, ?, ?, ?)", (user_name, user_email, generate_password_hash(user_password), user_visible))
            db.commit()
            flash("Du har registrert en bruker")
            return redirect(url_for('index.index'))
    return render_template("registrer_bruker.html")


@bp.route("/auth/", methods =["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    if request.method == 'POST':
        user_email = request.form.get("email")
        user_password = request.form.get("password_l")
        correct_email = 0
        correct_password = 0
        db = get_db()
        user_row = get_user_by_email(user_email)
        #user_id = db.execute("SELECT id FROM users WHERE email = ?", (user_email,)).fetchone()['id']
        #user_info = db.execute("SELECT * FROM users WHERE email = ?", (user_email,)).fetchone()
        user = User.get(user_row['id'])
        if not user:
            correct_email = 0
            correct_password = 0
        else:
            correct_email = 1
        if not user:
            correct_password = 0
        elif check_password_hash(user_row['password'], user_password):
            correct_password = 1

        if (correct_email == 1) and (correct_password == 1):
            flash('Du er logget inn')
            login_user(user, remember=True)
            return redirect(url_for('index.index'))
        else:
            flash('Du skrevet feil passord eller email')

    return render_template("auth.html")


@bp.route("/forgot_password", methods =["GET", "POST"])
def forgot_password():
    if request.method == 'POST':
        user_email = request.form.get('email_f')
        pass_code = request.form.get('pass_code')
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (user_email,)).fetchone()
        if not user:
            flash('Denne mailen er ikke registert på en bruker')
        else:
            flash('Vi sender deg en mail med en kode du skriver inn under')
    return render_template("glemt_passord.html")

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index.index"))



