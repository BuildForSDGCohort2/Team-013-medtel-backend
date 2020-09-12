from app import sqlalchemy as db
from json import JSONEncoder
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from random import randint

user_role = db.Table(
    "user_role",
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.public_id"),
              primary_key=True),
    db.Column("role_id", db.Integer,
              db.ForeignKey("roles.id"),
              primary_key=True)
)

user_address = db.Table(
    "user_address",
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.public_id"),
              primary_key=True),
    db.Column("address_id", db.Integer,
              db.ForeignKey("addresses.id"),
              primary_key=True)
)



class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    users = db.relationship("User",
                            secondary=user_role,
                            back_populates="roles",
                            lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @property
    def serialize(self):

        return {
            "id": self.id,
            "name": self.name,
            "users": self.users
        }



class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String)
    phone_number = db.Column(db.String(20))
    roles = db.relationship("Role",
                            secondary=user_role,
                            back_populates="users",
                            cascade="all, delete",
                            lazy=True)
    addresses = db.relationship("Address",
                            secondary=user_address,
                            back_populates="users",
                            cascade="all, delete",
                            lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @property
    def serialize(self):
        addresses = Address.query.filter(
                Address.users.any(public_id=self.public_id)).all()
        return {
            "id": self.public_id,
            "name": self.name,
            "email": self.email,
            "addresses": [address.serialize for address in addresses]
        }

class Address(db.Model):
    __tablename__="addresses"
    
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    users = db.relationship("User",
                            secondary=user_address,
                            back_populates="addresses",
                            lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @property
    def serialize(self):
        
        return {
            "id": self.id,
            "city": self.city,
            "state": self.state,
            "country": self.country,
        }
