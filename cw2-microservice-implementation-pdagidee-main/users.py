# users.py
from flask import make_response, abort, request, jsonify
from config import db
from models import User, users_schema, user_schema
from auth import validate_user, create_token, get_email_from_token

# Login function to authenticate user credentials (POST request)
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        abort(400, "Email and password required")
    
    if validate_user(email, password):
        token = create_token(email)
        return jsonify({'token': token}), 200
    
    abort(401, "Invalid credentials")

# ADMIN - Function to return all users (GET request)
def read_all():
    print("=== READ_ALL CALLED ===")
    auth_header = request.headers.get('Authorization')
    print(f"Auth header: {auth_header}")

    if not auth_header:
        abort(401, "No token provided")
    
    token = auth_header.replace('Bearer ', '').strip()
    email = get_email_from_token(token)
    
    if not email:
        abort(401, "Invalid token")

    auth_user = User.query.filter(User.email == email).one_or_none()
    print(f"User found: {auth_user}")

    if auth_user: 
        print(f"User email: {auth_user.email}")
        print(f"User role: {auth_user.role}")

    if not auth_user or auth_user.role !="admin":
        abort(403, "Admin access required")

    users = User.query.all()
    return users_schema.dump(users), 200


def read_one(email):

    auth_header = request.headers.get("Authorization")
    print(f"Auth header: {auth_header}")

    if not auth_header:
        abort(401, "No token provided")

    token = auth_header.replace('Bearer ', '').strip()
    logged_in_email = get_email_from_token(token)

    if not logged_in_email:
        abort(401, "Invalid token")

    auth_user = User.query.filter(User.email ==logged_in_email).one_or_none()
    print(f"Auth_user found: {auth_user}")

    print(f"Looking for email: {repr(logged_in_email)}")
    all_users = User.query.all()
    print(f"All emails in DB: {[repr(u.email) for u in all_users]}")

    if not auth_user:
        abort(404, "Logged in user not found")

    if auth_user.role != "admin" and auth_user.email != email:
        abort(403, "Access Forbidden: You can only access your own profile")
             
        
    user = User.query.filter(User.email == email).one_or_none()
    if user is not None:
            return user_schema.dump(user), 200
    else: 
        abort(404, f"User with email {email} not found")

    
def create(user):

    email = user.get("email")
    existing_user = User.query.filter(User.email == email).one_or_none()

    if existing_user is None:
        new_user = user_schema.load(user, session=db.session)
        db.session.add(new_user)  
        db.session.commit()
        return user_schema.dump(new_user), 201
    else:
        abort(406, f"User with email {email} already exists")


def update(email, user):

    auth_header = request.headers.get("Authorization")
    print(f"Auth header: {auth_header}")

    if not auth_header:
        abort(401, "No token provided")

    token = auth_header.replace('Bearer ', '').strip()
    logged_in_email = get_email_from_token(token)

    if not logged_in_email:
        abort(401, "Invalid token")

    auth_user = User.query.filter(User.email == logged_in_email).one_or_none()
    
    if not auth_user:
        abort(404, "Logged in user could not be found")
    
    if auth_user.role!= "admin" and auth_user.email != email:
        abort(403, "Access Forbidden: You do not have permission for this")
   

    existing_user = User.query.filter(User.email == email).one_or_none()

    if existing_user:
        update_user = user_schema.load(user, session=db.session)
        existing_user.username = update_user.username
        existing_user.location = update_user.location
        existing_user.language = update_user.language
        existing_user.role = update_user.role
        db.session.commit()

        return user_schema.dump(existing_user), 200
    else:
        abort(404, f"User with email {email} not found")

# Method to delete user - (DELETE request)
def delete(email): 

    auth_header = request.headers.get("Authorization")
    print(f"Auth header: {auth_header}")

    if not auth_header:
        abort(401, "No token provided")

    token = auth_header.replace('Bearer ', '').strip()
    print(f"Token extracted: {token}")
    logged_in_email = get_email_from_token(token)
    print(f"Email from token: {logged_in_email}")

    if not logged_in_email:
        abort(401, "Invalid token")

    from auth import active_sessions
    print(f"Active sessions: {active_sessions}")

    auth_user = User.query.filter(User.email == logged_in_email).one_or_none()
    print(f"Auth user found: {auth_user}")

    if not auth_user:
        abort(404, "Logged in user could not be found")

    if auth_user.role != "admin" and auth_user.email != email:
     abort(403, "Access Forbidden: You can only delete your own profile")

 
    existing_user = User.query.filter(User.email == email).one_or_none()

    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
        return make_response(f"User {email} successfully deleted", 200)
    else:
        abort(404, f"User with email {email} not found")