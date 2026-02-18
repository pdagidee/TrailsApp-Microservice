#auth.py
import requests
import secrets


AUTH_URL = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'

# Storing  list of active sessions for authentication
active_sessions = {}

# Validating user credentials from external API (also in Postman)
def validate_user(email, password):
    credentials = {
        'email': email,
        'password': password
    }
    try:
        response = requests.post(AUTH_URL, json=credentials)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) >= 2:
                return data[1] == "True" or data[1] == True
        return False
    except:
        return False

# Creating token based on validated user credentials; using secrets model to create token
def create_token(email):
    token = secrets.token_hex(16)
    active_sessions[token] = email
    return token
    print(f"Created token for {email}: {token}")
    print(f"Active sessions after creation: {active_sessions}")
    return token

def get_email_from_token(token):
    return active_sessions.get(token)
    print(f"Looking up token {token}, found email: {email}")
    print(f"All active sessions: {active_sessions}")
    return email