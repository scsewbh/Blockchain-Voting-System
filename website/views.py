from flask import Blueprint, render_template, redirect, url_for, session, request
from collections import Counter
from google.cloud import datastore
import os
from operator import itemgetter

# Blueprints are use to organize the different pages on a web app.
# The blueprint is connected in the setup of the init.py file

views = Blueprint('views', __name__)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'website/static/secret/BCVS_service_account.json'
client = datastore.Client()
client_mempool = datastore.Client()
client_candidates = datastore.Client()

@views.route('/', methods = ['GET', 'POST'])
def vote():
    if request.method == 'POST':
        list_form_data = list((request.form).items())
        choice = findChecked(list_form_data)
        print(request.form)

        key = client.key('voted')
        entity = datastore.Entity(key=key)
        entity.update({
            'GID': session['userid']
        })
        client.put(entity)

        data = {"vote": [choice], "user": [session['userid'], session['fname'], session['lname'], session['email'], request.form["age"]]}
        key = client_mempool.key('mempool')
        entity = datastore.Entity(key=key)
        entity.update({
            'Data': data,
            'Fee': 0,
            'workedOn': False
        })
        client.put(entity)
        return redirect(url_for('views.results'))
    else:
        print(session)
        if 'authenticated' in session and session['authenticated']:
            query = client.query(kind="voted")
            query.add_filter("GID", "=", session['userid'])
            results = list(query.fetch())
            query = client_candidates.query(kind="candidates")
            candidates = list(query.fetch())

            candidate_array = []

            for candidate in candidates:
                candidate_array.append(candidate['Name'])

            if not results:
                return render_template('register.html', userid=session['userid'], fname=session['fname'],
                                       lname=session['lname'], email=session['email'], candidates=candidate_array)
            else:
                return redirect(url_for('views.results')) #ERROR or SIGN IN FIRST

        else:
            return redirect(url_for('auth.login'))


@views.route('/results')
def results():
    print(session)
    if 'authenticated' in session and session['authenticated']:
        query = client.query(kind="blockchain")
        bc_data = list(query.fetch())
        chart_data = bcResult(bc_data)
        blockchain_data = blockchain_table(bc_data)
        return render_template('voted.html', userid=session['userid'], chart_data=chart_data, blockchain_data=blockchain_data)
    else:
        return redirect(url_for('auth.login')) #ERROR or SIGN IN FIRST

def findChecked(data):
    if data[-1][1] != '' and data[-2][0] == 'other':
        return data[-1][1]
    else:
        if data[-2][0] == 'age':
            return 'Empty'
        return data[-2][0].replace("_", " ")

def bcResult(data):
    votes_array = []
    chart_array = [["Candidates", "Number of Votes"]]
    print(data)

    for entity in data:
        if bool(entity["Data"]):
            votes_array.append(entity["Data"]["vote"])

    results = Counter(votes_array)
    for candidate in results:
        chart_array.append([candidate, results[candidate]])
    return chart_array

def blockchain_table(data):
    block_array = []

    for entity in data:
        block_array.append([entity['Block_Number'], entity['Hash'], entity['Previous_Hash'], entity['Fee']])
    block_array = sorted(block_array, key=itemgetter(0))
    return block_array