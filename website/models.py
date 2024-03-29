from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    reservations = db.relationship('Reservation', backref='user', lazy=True)

class Bungalow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(255), unique=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('bungalowtype.id'), nullable=False)
    fotopath = db.Column(db.String)
    reservations = db.relationship('Reservation', backref='bungalow', lazy=True)

class Bungalowtype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aantal_personen = db.Column(db.Integer, unique=True, nullable=False)
    weekprijs = db.Column(db.Float, nullable=False)
    bungalows = db.relationship('Bungalow', backref='type', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bungalow_id = db.Column(db.Integer, db.ForeignKey('bungalow.id'), nullable=False)
    week = db.Column(db.String(10), nullable=False)


predefined_bungalowtypes = [
    {'aantal_personen': 4, 'weekprijs': 1600},
    {'aantal_personen': 6, 'weekprijs': 2000},
    {'aantal_personen': 8, 'weekprijs': 2400},
]

predefined_bungalows = [
    {'naam': 'Duif', 'type_id': 1, 'fotopath': 'duif'},
    {'naam': 'Pauw', 'type_id': 1, 'fotopath': 'pauw'},
    {'naam': 'Kip', 'type_id': 1, 'fotopath': 'kip'},
    {'naam': 'Kalkoen', 'type_id': 1, 'fotopath': 'kalkoen'},
    {'naam': 'Kraai', 'type_id': 2, 'fotopath': 'kraai'},
    {'naam': 'Ekster', 'type_id': 2, 'fotopath': 'ekster'},
    {'naam': 'Kauw', 'type_id': 2, 'fotopath': 'kauw'},
    {'naam': 'Kievit', 'type_id': 2, 'fotopath': 'kievit'},
    {'naam': 'Zwaan', 'type_id': 3, 'fotopath': 'zwaan'},
    {'naam': 'Flamingo', 'type_id': 3, 'fotopath': 'flamingo'},
    {'naam': 'Pinguin', 'type_id': 3, 'fotopath': 'pinguin'},
    {'naam': 'Struisvogel', 'type_id': 3, 'fotopath': 'struisvogel'},
]

def add_bungalowTypes():
    for bungalowtype_data in predefined_bungalowtypes:
        existing_bungalowtype = Bungalowtype.query.filter_by(aantal_personen=bungalowtype_data['aantal_personen']).first()

        if not existing_bungalowtype:
            new_bungalowtype = Bungalowtype(aantal_personen=bungalowtype_data['aantal_personen'], weekprijs=bungalowtype_data['weekprijs'])
            db.session.add(new_bungalowtype)
    
    db.session.commit()

def add_bungalows():
    for bungalow_data in predefined_bungalows:
        existing_bungalow = Bungalow.query.filter_by(naam=bungalow_data['naam']).first()

        if not existing_bungalow:
            new_bungalow = Bungalow(naam=bungalow_data['naam'], type_id=bungalow_data['type_id'], fotopath=bungalow_data['fotopath'])
            db.session.add(new_bungalow)
    
    db.session.commit()

def initialize_database():
    add_bungalowTypes()
    add_bungalows()