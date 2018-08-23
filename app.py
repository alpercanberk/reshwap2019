
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
"https://www.googleapis.com/auth/userinfo.email", #gets google profile
"https://www.googleapis.com/auth/userinfo.profile", #gets google email adress
]

app = Flask(__name__,template_folder="templates")
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#configurates SQLAlchemy

#ReshwapItems is the database model for reshwap_items
class ReshwapItems(db.Model):
    __tablename__ = 'reshwap_items'

    id = db.Column(db.Integer, primary_key=True)
    uploader = db.Column(db.String())
    title = db.Column(db.String())
    details = db.Column(db.String())
    category = db.Column(db.String())
    department = db.Column(db.String())
    money = db.Column(db.String())
    exchange = db.Column(db.String())
    image_one = db.Column(db.String())
    image_two = db.Column(db.String())
    image_three = db.Column(db.String())
    image_four = db.Column(db.String())
    date = db.Column(db.String())
    is_completed = db.Column(db.Boolean())


    def __init__(self, uploader, title, details, category, department, money, exchange, image_one, image_two, image_three, image_four, date, is_completed):
        self.uploader = uploader
        self.title = title
        self.details = details
        self.category = category
        self.department = department
        self.money = money
        self.exchange = exchange
        self.image_one = image_one
        self.image_two = image_two
        self.image_three = image_three
        self.image_four = image_four
        self.date = date
        self.is_completed = is_completed

    def createSession(self):
        Session = sessionmaker()
        self.session = Session.configure(bind=self.engine)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ReshwapUsers(db.Model):
    __tablename__ = 'reshwap_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    profile_pic = db.Column(db.String())
    email = db.Column(db.String())
    signup_date = db.Column(db.String())
    last_login = db.Column(db.String())

    def __init__(self, name, profile_pic, email, signup_date, last_login):
        self.name = name
        self.profile_pic = profile_pic
        self.email = email
        self.signup_date = signup_date
        self.last_login = last_login


    def createSession(self):
        Session = sessionmaker()
        self.session = Session.configure(bind=self.engine)

    def __repr__(self):
        return '<id {}>'.format(self.id)


@app.route('/')
def index():

    if('credentials' in flask.session):
        found_user = db.session.query(ReshwapUsers).filter(ReshwapUsers.email == flask.session["user_info"]["email"]).all()
        found_user[0].last_login = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        db.session.commit()
        return render_template("home.html",
                               user = flask.session['user_info']['email'],
                               current_host= flask.request.url_root,
                               accessKeyId = os.environ["ACCESS_KEY_ID"])
    return render_template("index.html")


@app.route('/no')
def no():
    return redirect("https://www.reshwap.com")

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

@app.route('/complete',methods=["DELETE"])
def complete():
    id = request.args.get('id')
    complete_item = db.session.query(ReshwapItems).filter(ReshwapItems.id == id).first()
    print("Hey")
    if(complete_item.uploader == flask.session["user_info"]["email"]):
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
                           images[3], datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"), False)
    db.session.add(newItem)
    db.session.commit()
    return "ok"

@app.route('/items', methods=['GET'])
def items(category=None):
    all_items = db.session.query(ReshwapItems).filter(ReshwapItems.is_completed == False)
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


def credentials_to_dict(credentials):
    return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

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

    if("@lawrenceville.org" in flask.session["user_info"]["email"]):

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
            print("someone is signing in again...")
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

    return redirect('/')

@app.route('/.well-known/acme-challenge/D7KL4EsRSqpkfbtUnHmbyimH9D_k-DfYJp3Lezpn6M0')
def certificate():
    return 'D7KL4EsRSqpkfbtUnHmbyimH9D_k-DfYJp3Lezpn6M0.XJCCq-TzDG6P7Y2xlbxIwndc_G2BCn7oYQESoqR_wvg'

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=os.environ['PORT'])
