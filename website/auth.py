from flask import Blueprint, render_template, request, url_for, redirect, session
import json
from oauth2client import client
from google.cloud import datastore
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'website/static/secret/BCVS_service_account.json'
#Blueprints are use to organize the different pages on a web app.
#The blueprint is connected in the setup of the init.py file

auth = Blueprint('auth', __name__)

#GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

@auth.route('/login') #Page Route -- A prefix if any is listed in the init.py file
def login():
    if 'authenticated' in session and session['authenticated']:
        return redirect(url_for('views.vote'))
    else:
        print('onlogin')
        return render_template('login.html')

@auth.route('/login/callback', methods = ['POST'])
def login_callback():
    if not request.headers.get('X-Requested-With'):
        return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}

    content_type = request.headers.get("Content-Type")
    auth_code = request.stream if content_type == "application/octet-stream" else request.get_data()
    CLIENT_SECRET_FILE = 'website/static/secret/BCVS_client_secret.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['profile', 'email'],
        auth_code)
    print(credentials.id_token)

    # Get profile info from ID token
    session['authenticated'] = True
    session['userid'] = credentials.id_token['sub']
    session['fname'] = credentials.id_token['given_name']
    session['lname'] = credentials.id_token['family_name']
    session['email'] = credentials.id_token['email']
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}



@auth.route('/logout') #Page Route -- A prefix if any is listed in the init.py file
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


