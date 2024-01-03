from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user
views = Blueprint('views', __name__)
from website.models import db, User, Bungalow, Bungalowtype, Reservation
from flask_sqlalchemy import SQLAlchemy

@views.route('/')
@login_required
def home():
    bungalows = Bungalow.query.all()
    return render_template("home.html", user=current_user, bungalows=bungalows)

@views.route('/booking/<int:id>')
@login_required
def booking(id):
    bungalow = Bungalow.query.get(id)

    if bungalow:
        return render_template('booking.html', user=current_user, bungalow=bungalow)
    else:
        abort(404, description="Bungalow not found")

@views.route('/booking/<int:id>', methods=['POST'])
@login_required
def create_reservation(id):
    existing_reservation = Reservation.query.filter_by(user_id=current_user.id, bungalow_id=id, week=request.form.get('week')).first()
    if existing_reservation:
        flash('You have already made a reservation for this bungalow.', category='error')
    else:
        reservation = Reservation(user_id=current_user.id, bungalow_id=id, week=request.form.get('week'))
        db.session.add(reservation)
        db.session.commit()
        flash('Reservation created successfully.', category='succes')

    return redirect(url_for('views.booking', id=id))

@views.route('/reservations/')
#TODO /reservation/ werkt, maar kan niet vanaf deze pagina uitloggen. 
@login_required
def reservations():
    user_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    if user_reservations == None:
        #TODO Implementeer onderstaande
        return 'Je hebt nog geen reserveringen'
    else:
        return render_template('reservations.html', user=current_user, reservations=user_reservations)

@views.route('/change_week/<int:reservation_id>', methods=['POST'])
@login_required
def change_week():
    pass

@views.route('/change_bungalow/<int:reservation_id>', methods=['POST'])
@login_required
def change_bungalow():
    pass

@views.route('/delete_reservation/<int:reservation_id>', methods=['GET'])
def delete_reservation(reservation_id):
    reservation= Reservation.query.get(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Your reservation was succesfully deleted!', category='succes')
    return redirect(url_for('views.reservations'))