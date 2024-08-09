# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Villa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    rooms = db.Column(db.Integer, nullable=True)
    heard_about = db.Column(db.String(100))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    photos = db.relationship('Photo', backref='villa', lazy=True)
    link = db.Column(db.String(200))

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    villa_id = db.Column(db.Integer, db.ForeignKey('villa.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    guest_capacity = db.Column(db.Integer, nullable=False)
    room_count = db.Column(db.Integer, nullable=False)
    baths = db.Column(db.Integer, nullable=False)
    great_for = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    highlights = db.Column(db.Text, nullable=True)
    rule = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    cover_photo = db.Column(db.String(100), nullable=False)
    location_description = db.Column(db.Text, nullable=True)
    location_link = db.Column(db.String(500), nullable=True)
    images = db.relationship('PropertyImage', backref='property', cascade="all, delete-orphan", lazy=True)
    amenities = db.relationship('Amenity', backref='property', cascade="all, delete-orphan", lazy=True)
    meals = db.relationship('MealOption', backref='property', cascade="all, delete-orphan", lazy=True)
    rooms = db.relationship('Room', backref='property', cascade="all, delete-orphan", lazy=True)
    faqs = db.relationship('FAQ', backref='property', cascade="all, delete-orphan", lazy=True)
    daily_prices = db.relationship('DailyPrice', cascade="all, delete-orphan", backref='property', lazy=True)
    reviews = db.relationship('Review', backref='property', cascade="all, delete-orphan", lazy=True)

class PropertyImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    image_file = db.Column(db.String(100), nullable=False)

class Amenity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(100), nullable=False)

class MealOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    image_file = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    room_photo = db.Column(db.String(100), nullable=False)
    room_description = db.Column(db.Text, nullable=False)

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

class DailyPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
