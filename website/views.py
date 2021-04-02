from flask import Blueprint, render_template, redirect, url_for, session, request

from google.cloud import datastore
import os

# Blueprints are use to organize the different pages on a web app.
# The blueprint is connected in the setup of the init.py file

views = Blueprint('views', __name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'website\static\secret\BCVS_service_account.json'
client = datastore.Client()

@views.route('/', methods = ['GET', 'POST'])
def vote():
    if request.method == 'POST':
        key = client.key('UserCourses', session['userid'])
        entity = datastore.Entity(key=key)
        entity.update({
            'MyClassList': request.form["mylistdata"]
        })
        client.put(entity)
        print(request.form["mylistdata"])
        return redirect(url_for('views.results'))
    else:
        print(session)
        if 'authenticated' in session and session['authenticated']:
            query = client.query(kind="voted")
            results = list(query.fetch())
            print(results)
            return render_template('register.html', userid=session['userid'], fname=session['fname'], lname=session['lname'], email=session['email'])
        else:
            return redirect(url_for('auth.login')) #ERROR or SIGN IN FIRST


@views.route('/results')
def results():
    print(session)
    if 'authenticated' in session and session['authenticated']:
        return render_template('voted.html', userid=session['userid'])
    else:
        return redirect(url_for('auth.login')) #ERROR or SIGN IN FIRST
