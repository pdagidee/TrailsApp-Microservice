# build_database.py

from datetime import date
from config import app, db
import traceback
from sqlalchemy import MetaData
from models import User, Activity, Favourite_Activity, Saved_Trail

# populating the databases with sample data provided in coursework spec
try:
    with app.app_context():

        db.drop_all()
        print('Tables successfully deleted')

        db.create_all()
        # Create reference data
        hiking = Activity(activity_name="Hiking")    
        rugby = Activity(activity_name="Rugby")
        running = Activity(activity_name="Running")
        
        db.session.add(hiking)
        db.session.add(rugby)
        db.session.add(running)
        db.session.commit()
        
        #Create 
        grace = User(
            username="Grace Hopper",
            email="grace@plymouth.ac.uk",
            DoB=date(2000, 7, 30),
            password="ISAD123!",
            role="admin",
            measurement_unit="imperial",
            location="Plymouth",
            language="English"
        )
        tim = User(
            username="Tim Berners-Lee",
            email="tim@plymouth.ac.uk",
            DoB=date(2005, 4, 8),
            password="COMP2001!",
            role="user",
            measurement_unit="imperial",
            location="Rome",
            language="English"
        )
        
        ada = User(
            username="Ada Lovelace",
            email="ada@plymouth.ac.uk",
            DoB=date(2006, 5, 15),
            password="insecurePassword",
            role="user",
            measurement_unit="metric",
            location="Plymouth",
            language="German"
        )
        db.session.add(grace)
        db.session.add(tim)
        db.session.add(ada)
        db.session.commit()
        
        # Create relationships
        fav1 = Favourite_Activity(user_id=grace.id, activity_id=hiking.id)
        trail1 = Saved_Trail(trail_id=1, user_id=grace.id)
        fav2 = Favourite_Activity(user_id=tim.id, activity_id=rugby.id)
        trail2 = Saved_Trail(trail_id=2, user_id=tim.id)
        fav3 = Favourite_Activity(user_id=ada.id, activity_id=running.id)
        trail3 = Saved_Trail(trail_id=3, user_id=ada.id)
        
        db.session.add_all([fav1, trail1])
        db.session.add_all([fav2, trail2]) 
        db.session.add_all([fav3, trail3])
        db.session.commit()
        print("Database created!")

    
    
except Exception as e:
    print(f"Error occurred: {e}")
    
    traceback.print_exc()