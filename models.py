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
              primary_key=True),
)

doctor_special = db.Table(
    "doctor_special",
    db.Column("doctor_id", db.Integer,
              db.ForeignKey("doctors.id"),
              primary_key=True),
    db.Column("special_id", db.Integer,
              db.ForeignKey("specializations.id"),
              primary_key=True),
    db.Column("id", db.Integer, primary_key=True)
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
        }


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    profile_image = db.Column(db.String())
    password_hash = db.Column(db.String())
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
        role = Role.query.filter(
            Role.users.any(public_id=self.public_id)).first()
        return {
            "id": self.public_id,
            "name": self.name,
            "email": self.email,
            "addresses": [address.serialize for address in addresses],
            "role": role.name
        }


class Address(db.Model):
    __tablename__ = "addresses"

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

class Doctor(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    overview = db.Column(db.String(4000))
    practicing_from = db.Column(db.DateTime())
    password_hash = db.Column(db.String())
    email = db.Column(db.String(120), index=True, unique=True)
    profile_image = db.Column(db.String())

    specializations = db.relationship("Specialization",
                            secondary=doctor_special,
                            back_populates="doctors",
                            cascade="all, delete",
                            lazy=True)

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

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "overview": self.overview,
            "practicing_from": self.practicing_from,
            "email": self.email,
            "profile_image": self.profile_image
        }


class Specialization(db.Model):
    __tablename__ = "specializations"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    doctors = db.relationship("Doctor",
                            secondary=doctor_special,
                            back_populates="specilizations",
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
            "name": self.name
        }

class Qualification(db.Model):
    __tablename__ = "qualifications"
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    name = db.Column(db.String(200))
    institute = db.Column(db.String(200))
    procurement_year = db.Column(db.DateTime())

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
            "doctor_id": self.doctor_id,
            "name": self.name,
            "institute": self.institute,
            "procurement_year": self.procurement_year
        }


class HospitalAffiliate(db.Model):
    __tablename__ = "hospital_affiliate"
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))
    hospital_name = db.Column(db.String(200))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    start_date = db.Column(db.DateTime())
    end_date = db.Column(db.DateTime())

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
            "doctor_id": self.doctor_id,
            "hospital": self.hospital_name,
            "city": self.city,
            "country": self.country,
            "start_date": self.start_date,
            "end_date": self.end_date
        }
