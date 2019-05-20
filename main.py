# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
import requests
import os
import json

# [START imports]
from flask import Flask, render_template, request, redirect
# from urlparse import urlparse
# from uuid import uuid4
# from urllib import urlencode
# import urllib
# import httplib
# [END imports]

# Constants
CLIENT_ID = "183048715948-mlej4766rra4liina1pct9ei1ll8cks0.apps.googleusercontent.com"
STATE = "mNWCUc-h4Igc7ryHx2q6hJXj"
PREFIX = "https://accounts.google.com/o/oauth2/v2/auth"
POST_PREFIX = "https://www.googleapis.com/oauth2/v4/token"
REDIRECT_URI = "http://localhost:5000/submitted"
DYNAMIC_PARAM = "555"

# [START create_app]
app = Flask(__name__)
# app = Flask(name)
# [END create_app]


@app.route("/")
def hello():
    # return "Hello Gato"
    return render_template('index.html')

'''
https://accounts.google.com/o/oauth2/v2/auth
?response_type=code
&client_id=107461084371-0vr1hjlgafvltftq307ceq0pcjrk2ad4.apps.googleusercontent.com
&redirect_uri=https://osu-cs496-demo.appspot.com/oauth
&scope=email
&state=SuperSecret9000
'''
'''
https://accounts.google.com/o/oauth2/v2/auth
?response_type=code
&client_id=107461084371-0vr1hjlgafvltftq307ceq0pcjrk2ad4.apps.googleusercontent.com
&redirect_uri=https://osu-cs496-demo.appspot.com/oauth
&scope=email
&state=SuperSecret9000
'''


@app.route('/redirect_auth', methods=['GET'])
def redirect_auth():
    getAuthURL = PREFIX + "?" + "response_type=" + "code" + "&" + "client_id=" + CLIENT_ID + "&" + "redirect_uri=" + REDIRECT_URI + "&" + "scope=" + "profile email" + "&" + "state=" + STATE
    r = requests.get(getAuthURL)
    # print("BEFORE r.url is: ", r.url)
    # print("\n")
    # print("BEFORE r.content is: ", r.content)
    # print("\n")
    # print("BEFORE r.json is: ", r.json)
    # print("\n")
    # print("BEFORE r.text is: ", r.text)

    return redirect(getAuthURL)
    # return flask.redirect(getAuthURL)



    return('',200)
# [START form]
@app.route('/form'+DYNAMIC_PARAM)
def form():
    # return flask.redirect(authorization_url) NEED THIS SOMEWHERE LATER
    return render_template('form.html')
# [END form]



# [START submitted]
# @app.route('/submitted', methods=['POST'])
@app.route('/submitted', methods=['GET'])
def submitted_form():
    # Get the access code
    print("\nTRACE STATEMENTS")
    authcode = request.args.get('code')
    print("authcode", authcode)

    # POST using the access code
    payload = {'code': authcode, 'client_id': CLIENT_ID, 'client_secret': STATE, 'redirect_uri':REDIRECT_URI, 'grant_type': 'authorization_code'}
    r = requests.post(POST_PREFIX, data=payload)
    print("r.text: ", r.text)
    print("\n")
    print("type of r.text: ", type(r.text))
    # print ("r.text.access_token is:", r.text.access_token)
    # JSONify the access token and data
    jsonData = json.loads(r.text)
    print("\n")
    print("type of jsonData is: ", type(jsonData))
    print("\n")
    print("jsonData is: ", jsonData)
    print("\n")
    print("access_token is: ", jsonData['access_token'])
    print("\n")
    print("tyep of access_token is: ", type(jsonData['access_token']))

    token = jsonData['access_token']
    print("\n")
    # GET to people api using bearer token
    peopleURL = "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses"
    headers = {'Authorization': "Bearer " + token}
    peopleResponse = requests.get(peopleURL, headers=headers)
    print("peopleResponse.text is:", peopleResponse.text)
    print("type of peopleResponse.text is:", type(peopleResponse.text))

    # [START render_template]
    return render_template('submitted_form.html')
    # return render_template(
    #     'submitted_form.html',
    #     name=name,
    #     email=email,
    #     site=site,
    #     comments=comments)
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]
