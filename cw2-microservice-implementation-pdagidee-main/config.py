
# config.py

import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from schema import metadata
from auth import validate_user

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc:///?odbc_connect="
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=dist-6-505.uopnet.plymouth.ac.uk;"
    "DATABASE=COMP2001_pagidee;"
    "UID=pagidee;"
    "PWD=Rayesuzanne0908;"
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Overriding config settings to prevent JSON from being ordered alphabetically for viewing ease
app.config["JSON_SORT_KEYS"] = False

db = SQLAlchemy(app, metadata=metadata)
ma = Marshmallow(app)

def bearer_auth(token):
    """Connexion calls this to validate bearer tokens"""
    from auth import get_email_from_token
    email = get_email_from_token(token)
    if email:
        return {'sub': email}  # Valid token
    return None