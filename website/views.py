from flask import Blueprint, render_template, redirect, url_for, session, request

from google.cloud import datastore
import os

# Blueprints are use to organize the different pages on a web app.
# The blueprint is connected in the setup of the init.py file

views = Blueprint('views', __name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'website\static\secret\BCVS_service_account.json'
client = datastore.Client()
client_mempool = datastore.Client()

@views.route('/', methods = ['GET', 'POST'])
def vote():
    if request.method == 'POST':
        key = client.key('voted')
        entity = datastore.Entity(key=key)
        entity.update({
            'GID': session['userid']
        })
        client.put(entity)
        choice = findChecked(request.form)
        print(request.form)
        if choice == 'Other':
            choice = request.form.get('other_text')
        data = {"vote": [choice], "user": [session['userid'], session['fname'], session['lname'], session['email'], request.form["age"]]}
        key = client_mempool.key('mempool')
        entity = datastore.Entity(key=key)
        entity.update({
            'Data': data,
            'Fee': 0,
            'workedOn': False
        })
        client.put(entity)
        print(session['userid'])
        return redirect(url_for('views.results'))
    else:
        print(session)
        if 'authenticated' in session and session['authenticated']:
            query = client.query(kind="voted")
            query.add_filter("GID", "=", session['userid'])
            results = list(query.fetch())
            if not results:
                return render_template('register.html', userid=session['userid'], fname=session['fname'],
                                       lname=session['lname'], email=session['email'])
            else:
                return redirect(url_for('views.results')) #ERROR or SIGN IN FIRST

        else:
            return redirect(url_for('auth.login'))


@views.route('/results')
def results():
    print(session)
    if 'authenticated' in session and session['authenticated']: #and voted then render
        return render_template('voted.html', userid=session['userid'])
    else:
        return redirect(url_for('auth.login')) #ERROR or SIGN IN FIRST

def findChecked(data):
    if data.get('eric'):
        return 'Eric C.'
    elif data.get('mike'):
        return 'Mike S.'
    elif data.get('sanjay'):
        return 'Sanjay S.'
    else:
        return 'Other'