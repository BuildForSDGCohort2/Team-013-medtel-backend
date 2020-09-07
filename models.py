from app import sqlalchemy as db
from json import JSONEncoder
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from random import randint

# Generate a public id to prevent exposure of user id in database
default_public_id = randint(100, 100000)

user_role = db.Table(
    "user_role",
    db.Column("user_id", db.Integer,
              db.ForeignKey("users.id"),
              primary_key=True),
    db.Column("role_id", db.Integer,
              db.ForeignKey("roles.id"),

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
    public_id = db.Column(db.String(20), unique=True, default=default_public_id)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(20))
    roles = db.relationship("Role",
                            secondary=user_role,
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
        role = Role.query.filter(Role.users.any(id=self.id)).first()
        return {
            "id": self.public_id,
            "name": self.name,
            "email": self.email,
            "role": role.name if role else 'No role assigned'
        }
