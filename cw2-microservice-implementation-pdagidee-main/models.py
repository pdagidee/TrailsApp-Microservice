from datetime import datetime
import pytz
from marshmallow import fields 

from config import db, ma
    

class Activity(db.Model):
    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activity_name = db.Column(db.String(40), nullable=False, unique=True)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    DoB = db.Column(db.Date, nullable=True)
    password = db.Column(db.String(80), nullable=True)
    role = db.Column(db.String(10), default="user", nullable=False)
    measurement_unit = db.Column(db.String(10), default="imperial", nullable=True)
    location = db.Column(db.String(50), nullable=True)
    language = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
        onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )

    favourite_activity = db.relationship(
    "Favourite_Activity",
    backref="users",
    cascade="all, delete-orphan",
) 
    saved_trail = db.relationship(
    "Saved_Trail",
    backref="users",
    cascade="all, delete-orphan",
    single_parent=True
)

class Favourite_Activity(db.Model):
    __tablename__ = "favourite_activity"
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),primary_key=True, nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey("activity.id"), primary_key=True, nullable=False)

class Saved_Trail(db.Model):
   __tablename__ = "saved_trail"
   trail_id = db.Column(db.Integer, primary_key=True, nullable=False)
   user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True, nullable=False)

class Favourite_ActivitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Favourite_Activity
        load_instance=True
        sqla_session = db.session

class ActivitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Activity
        load_instance = True
        sqla_session = db.session

class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'DoB', 'role', 'location', 'language')
        load_instance = True
        sqla_session = db.session
        include_relationships = True


        
class Saved_TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Saved_Trail
        load_instance=True
        sqla_session = db.session


user_schema = UserSchema()
users_schema = UserSchema(many=True) 
activity_schema = ActivitySchema()
favourite_activity_schema = Favourite_ActivitySchema()
savedtrail_schema = Saved_TrailSchema()