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

# [START imports]
from flask import Flask, render_template, request, redirect
# [END imports]

# Constants
CLIENT_ID = "183048715948-mlej4766rra4liina1pct9ei1ll8cks0.apps.googleusercontent.com"
STATE = "mNWCUc-h4Igc7ryHx2q6hJXj"
PREFIX = "https://accounts.google.com/o/oauth2/v2/auth"
REDIRECT_URI = "http://localhost:5000/submitted"
DYNAMIC_PARAM = "555"

# [START create_app]
app = Flask(__name__)
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
    getAuthURL = PREFIX + "?" + "response_type=" + "code" + "&" + "client_id=" + CLIENT_ID + "&" + "redirect_uri=" + REDIRECT_URI + "&" + "scope=" + "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email" + "&" + "state=" + STATE
    r = requests.get(getAuthURL)
    print("r.url is: ", r.url)
    print("\n")
    print("r.content is: ", r.content)
    print("\n")
    print("r.json is: ", r.json)
    print("\n")
    print("r.text is: ", r.text)

    return redirect(getAuthURL)

    # return redirect("http://www.sfgate.com")


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
    # name = request.form['name']
    # email = request.form['email']
    # site = request.form['site_url']
    # comments = request.form['comments']

    # [END submitted]
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
