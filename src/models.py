from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = relationship("Favorites", back_populates="user")

    #def __repr__(self):
    #    return '<User %r>' % self.username

    def serialize(self):
        favorites = list(map(lambda x: x.serialize(), self.favorites))
        return {
            "id": self.id,
            "email": self.email,
            "favorites": favorites
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id', ondelete='CASCADE'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'), nullable=True)
    user = db.relationship("User", back_populates="favorites")
    planet = db.relationship("Planets", back_populates="favorites")
    character = db.relationship("Characters", back_populates="favorites")

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id,
            'planet_name': self.planet.planet_name if self.planet else None,
            'character_id': self.character_id, 
            'character_name': self.character.character_name if self.character else None
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(250), unique=True, nullable=False)
    rotation_period = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    gravity = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    favorites = db.relationship("Favorites", back_populates="planet")

    def serialize(self):
        return {
            'id': self.id,
            'planet_name': self.planet_name,
            'rotation_period': self.rotation_period,
            'orbital_period': self.orbital_period,
            'gravity': self.gravity,
            'terrain': self.terrain
        }

class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(250), unique=True, nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    birth_year = db.Column(db.String(5))
    skin_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    hair_color = db.Column(db.String(250))
    favorites = db.relationship("Favorites", back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name,
            "height": self.height,
            "weight": self.weight,
            "birth_year": self.birth_year,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color
        }