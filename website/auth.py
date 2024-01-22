from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Je bent ingelogd!', category='succes')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Wachtwoord onjuist, probeer opnieuw.', category='error')
        else:
            flash('Dit emailadres wordt niet herkend', category='error')        

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Dit emailadres is al in gebruik', category='error')
    
        elif len(email) < 4:
            flash("Emailadres moet minstens 3 karakters bevatten", category='error')
        elif password1 != password2:
            flash("Wachtwoorden komen niet overeen", category='error')
        elif len(password1) <= 7:
            flash("Wachtwoord moet minstens 8 karakters bevatten", category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='pbkdf2:sha1'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account succesvol aangemaakt!", category='succes')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

