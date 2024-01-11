from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user
from website.models import db, User, Bungalow, Bungalowtype, Reservation
from flask_sqlalchemy import SQLAlchemy
from random import shuffle

views = Blueprint('views', __name__)

@views.route('/')
def home():
    user = current_user if current_user.is_authenticated else None

    if user:
        number_of_reservations = len(Reservation.query.filter_by(user_id=current_user.id).all())
        return render_template('home.html', user=current_user, number_of_reservations=number_of_reservations)
    
    return render_template('home.html', user=current_user)

@views.route('/booking/<int:id>')
@login_required
def booking(id):
    bungalow = Bungalow.query.get(id)
    number_of_reservations = len(Reservation.query.filter_by(user_id=current_user.id).all())
    if bungalow:
        return render_template('booking.html', user=current_user, bungalow=bungalow, number_of_reservations=number_of_reservations)
    else:
        abort(404, description="Bungalow not found")

@views.route('/booking/<int:id>', methods=['POST'])
@login_required
def create_reservation(id):
    existing_reservation = Reservation.query.filter_by(bungalow_id=id, week=request.form.get('week')).first()
    if existing_reservation:
        flash('This bungalow is already reservered for this week', category='error')
    else:
        reservation = Reservation(user_id=current_user.id, bungalow_id=id, week=request.form.get('week'))
        db.session.add(reservation)
        db.session.commit()
        flash('Reservation created successfully.', category='succes')

    return redirect(url_for('views.booking', id=id))

@views.route('/reservations/')
@login_required
def reservations():
    user_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    bungalows = Bungalow.query.all()
    number_of_reservations = len(Reservation.query.filter_by(user_id=current_user.id).all())
    if not user_reservations: 
        message = 'Je hebt nog geen reserveringen'
        return render_template('reservations.html', user=current_user, message=message, bungalows=bungalows, number_of_reservations=number_of_reservations)
    else:
        return render_template('reservations.html', user=current_user, reservations=user_reservations, bungalows=bungalows, number_of_reservations=number_of_reservations)

@views.route('/change_week/<int:reservation_id>', methods=['POST'])
@login_required
def change_week(reservation_id):
    existing_reservation = Reservation.query.filter_by(user_id=current_user.id, id=reservation_id).first()

    if existing_reservation:
        existing_reservation.week = request.form.get('week')
        db.session.commit()
        flash('Reservation changed successfully.', category='success')
    else:
        flash('Reservation not found.', category='error')

    return redirect(url_for('views.reservations'))

@views.route('/change_bungalow/<int:reservation_id>', methods=['POST'])
@login_required
def change_bungalow(reservation_id):
    existing_reservation = Reservation.query.filter_by(user_id=current_user.id, id=reservation_id).first()

    if existing_reservation:
        existing_reservation.bungalow_id = request.form.get('bungalow')
        db.session.commit()
        flash('Reservation changed successfully.', category='success')
    else:
        flash('Reservation not found.', category='error')

    return redirect(url_for('views.reservations'))

@views.route('/delete_reservation/<int:reservation_id>', methods=['GET'])
@login_required
def delete_reservation(reservation_id):
    reservation= Reservation.query.get(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Your reservation was succesfully deleted!', category='succes')
    return redirect(url_for('views.reservations'))


@views.route('/bungalows')
def beschikbare_bungalows():
    bungalows = Bungalow.query.all()
    shuffle(bungalows)
    user = current_user if current_user.is_authenticated else None

    if user:
        number_of_reservations = len(Reservation.query.filter_by(user_id=current_user.id).all())
        return render_template('bungalows.html', user=current_user, bungalows=bungalows, number_of_reservations=number_of_reservations)
    
    return render_template("bungalows.html", user=current_user, bungalows=bungalows)
    
