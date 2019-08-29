
from flask import Flask, redirect, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

import flask

import google.oauth2.credentials
import google_auth_oauthlib.flow

import datetime
import json


#scopes list determines which data we get from the user
oauth_scopes = [
"openid",
"https://www.googleapis.com/auth/userinfo.email", #gets google profile
"https://www.googleapis.com/auth/userinfo.profile", #gets google email adress
]

def email_to_school(email):
    print email
    special_indexes = []
    for x in range(0, len(email)):
        if email[x] == "." or email[x] == "@":
            special_indexes.append(x)
    print special_indexes
    return email[special_indexes[-2]+1:special_indexes[-1]]

def is_valid_school(email):
    if(("org" in email) or ("edu" in email) or ("k12" in email)):
        return True
    return False


def credentials_to_dict(credentials):
    return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


app = Flask(__name__,template_folder="templates")
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#configurates SQLAlchemy

#ReshwapItems is the database model for reshwap_items
from models import *

@app.route('/')
def index():
    if('credentials' in flask.session):
        found_user = db.session.query(ReshwapUsers).filter(ReshwapUsers.email == flask.session["user_info"]["email"]).all()
        found_user[0].last_login = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        db.session.commit()
        return render_template("home.html",
                               user = flask.session['user_info']['email'],
                               current_host= flask.request.url_root,
                               accessKeyId = os.environ["ACCESS_KEY_ID"],
                               secretKey = os.environ["SECRET_KEY"],
                               school = (email_to_school(flask.session["user_info"]['email'])).upper())

    return render_template("index.html")


@app.route('/no')
def no():
    return redirect(url_for('index'))

@app.route('/items/i')
def myitems():
    if(flask.session["user_info"]["email"]):
        myitems = db.session.query(ReshwapItems).filter(ReshwapItems.uploader == flask.session["user_info"]["email"]).filter(ReshwapItems.is_completed == False).all()
        myitems_list = []
        for item in myitems:
            print item
            dict = vars(item)
            dict.pop('_sa_instance_state')
            myitems_list.append(dict)

        return jsonify(myitems_list)
    else:
        return '"Hey! What are you doing?" -Harry Flaherty'

@app.route('/allitems')
def allitems():
    if(flask.session["user_info"]["email"] == "acanberk21@lawrenceville.org"):
        myitems = db.session.query(ReshwapItems).filter(ReshwapItems.is_completed == False).all()
        myitems_list = []
        for item in myitems:
            print item
            dict = vars(item)
            dict.pop('_sa_instance_state')
            myitems_list.append(dict)

        return jsonify(myitems_list)

@app.route('/complete',methods=["POST"])
def complete():
    print "hi"
    id = request.args.get('id')
    complete_item = db.session.query(ReshwapItems).filter(ReshwapItems.id == id).first()
    print("Hey")
    if(flask.session["user_info"]["email"] == "acanberk21@lawrenceville.org" or complete_item.uploader == flask.session["user_info"]["email"]):
        complete_item.is_completed = True
        db.session.commit()
        print("an item is completed")
    return "ok"

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json
    print(request.json)
    images = ["","","",""]
    for x in range(0, len(data["imageUrls"])):
        images[x] = data["imageUrls"][x]
    newItem = ReshwapItems(data["uploader"], data["title"], data["details"],
                           data["category"], data["department"], data["money"],
                           data["exchange"], images[0], images[1], images[2],
                           images[3], datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"), False, email_to_school(flask.session["user_info"]["email"]))
    db.session.add(newItem)
    db.session.commit()
    return "ok"

@app.route('/items', methods=['GET'])
def items(category=None):
    all_items = db.session.query(ReshwapItems).filter(ReshwapItems.is_completed == False).filter(ReshwapItems.school == email_to_school(flask.session["user_info"]["email"]))
    uploaders = request.args.get('uploaders')
    category = request.args.get('category')
    department = request.args.get('department')

    if uploaders:
        all_items = all_items.filter(ReshwapItems.uploader == uploaders)
    if category:
        all_items = all_items.filter(ReshwapItems.category == category)
    if department:
        all_items = all_items.filter(ReshwapItems.department == department)

    all_items = all_items.all()
    items = []
    for item in all_items:
        dict = vars(item)
        dict.pop('_sa_instance_state')
        items.append(dict)

    return jsonify(items)

@app.route('/auth/google')
def auth():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow stepsself.
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
      json.loads(os.environ['CLIENT_SECRET']),
      scopes=oauth_scopes,
      redirect_uri= flask.request.url_root + 'oauth2callback'
    )

    authorization_url, state = flow.authorization_url(
      prompt='consent',
      include_granted_scopes='true')

    flask.session['state'] = state

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_config(json.loads(os.environ['CLIENT_SECRET']), scopes=oauth_scopes, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    print(credentials_to_dict(credentials))
    flask.session['credentials'] = credentials_to_dict(credentials)

    if flask.session['credentials']['refresh_token'] == None:
        print(">>>>")
        # flow.credentials.token = "1/NWvP0mjD4Vp3xs22FkvdqWHw-_7VUyC2VN7zcsthHcw"
        flask.session['credentials']['refresh_token'] = "1/NWvP0mjD4Vp3xs22FkvdqWHw-_7VUyC2VN7zcsthHcw"

    session = flow.authorized_session()
    user_info = session.get('https://www.googleapis.com/userinfo/v2/me').json()

    flask.session["user_info"] = user_info

    if(is_valid_school(flask.session["user_info"]["email"])):
        found_user = db.session.query(ReshwapUsers).filter(ReshwapUsers.email == flask.session["user_info"]["email"]).all()
        print found_user
        print "User creation process initializing..."

        if(not found_user):
            user_info = flask.session["user_info"]
            newUser = ReshwapUsers(user_info["name"],
                                   user_info["picture"],
                                   user_info["email"],
                                   datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
                                   datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
                                   )
            db.session.add(newUser)
            db.session.commit()
            print "NEW USER CREATED \n\n\n\n"
        else:
            print("Someone is signing in again...")
            found_user[0].last_login = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
            db.session.commit()
        return redirect("/")
    return redirect("no")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    flask.session.pop('credentials', None)
    flask.session.pop('state', None)
    flask.session.pop('user_info', None)
    flask.session.pop('school', None)


    return redirect('/')

@app.route('/.well-known/acme-challenge/FyDKFWwE3CUmNIUO5Jj-JPyaKUBg5ApUk17iPXOJdj0')
def certificate():
    return 'FyDKFWwE3CUmNIUO5Jj-JPyaKUBg5ApUk17iPXOJdj0.XJCCq-TzDG6P7Y2xlbxIwndc_G2BCn7oYQESoqR_wvg'

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 1
    app.run(port=os.environ['PORT'])
