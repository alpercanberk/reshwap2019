from . import routes

from flask import Flask, redirect, render_template, request, jsonify, url_for
from flask import render_template
import flask

import google.oauth2.credentials
import google_auth_oauthlib.flow

import datetime
import json

import os

#scopes list determines which data we get from the user
# oauth_scopes = [
# "openid",
# "https://www.googleapis.com/auth/userinfo.email", #gets google profile
# "https://www.googleapis.com/auth/userinfo.profile", #gets google email adress
# ]
#
#
# def credentials_to_dict(credentials):
#     return {'token': credentials.token,
#           'refresh_token': credentials.refresh_token,
#           'token_uri': credentials.token_uri,
#           'client_id': credentials.client_id,
#           'client_secret': credentials.client_secret,
#           'scopes': credentials.scopes}
#
#
# @routes.route('/auth/google')
# def auth():
#     print(">>>> Authentication initiated >>>")
#     # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow stepsself.
#     flow = google_auth_oauthlib.flow.Flow.from_client_config(
#       json.loads(os.environ['CLIENT_SECRET']),
#       scopes=oauth_scopes,
#       redirect_uri= flask.request.url_root + 'oauth2callback'
#     )
#
#     authorization_url, state = flow.authorization_url(
#       prompt='consent',
#       include_granted_scopes='true')
#
#     flask.session['state'] = state
#
#     return redirect(authorization_url)
#
# @routes.route('/oauth2callback')
# def oauth2callback():
#     print("oauth2 callabck activated")
#     state = flask.session['state']
#
#     flow = google_auth_oauthlib.flow.Flow.from_client_config(json.loads(os.environ['CLIENT_SECRET']), scopes=oauth_scopes, state=state)
#     flow.redirect_uri = flask.url_for('routes.oauth2callback', _external=True)
#
#     authorization_response = flask.request.url
#     flow.fetch_token(authorization_response=authorization_response)
#
#     credentials = flow.credentials
#     flask.session['credentials'] = credentials_to_dict(credentials)
#
#     if flask.session['credentials']['refresh_token'] == None:
#         # flow.credentials.token = "1/NWvP0mjD4Vp3xs22FkvdqWHw-_7VUyC2VN7zcsthHcw"
#         flask.session['credentials']['refresh_token'] = "1/NWvP0mjD4Vp3xs22FkvdqWHw-_7VUyC2VN7zcsthHcw"
#
#     session = flow.authorized_session()
#     user_info = session.get('https://www.googleapis.com/userinfo/v2/me').json()
#
#     print(">>>> Checking email >>>>>")
#     if("@lawrenceville.org" in user_info["email"]):
#         flask.session["user_info"] = user_info
#         print(">>>> AUTHENTICATED")
#         print(flask.session["user_info"])
#         print(">>>>")
#         if("@" in flask.session["user_info"]["email"]):
#             found_user = db.session.query(ReshwapUsers).filter(ReshwapUsers.email == flask.session["user_info"]["email"]).all()
#
#             if(not found_user):
#                 user_info = flask.session["user_info"]
#                 newUser = ReshwapUsers(user_info["name"],
#                                        user_info["picture"],
#                                        user_info["email"],
#                                        datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
#                                        datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
#                                        )
#                 db.session.add(newUser)
#                 db.session.commit()
#             else:
#                 print("Someone is signing in again...")
#                 found_user[0].last_login = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
#                 db.session.commit()
#             return redirect("/")
#     else:
#         return redirect("invalid_account")
#
# @routes.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     flask.session.pop('credentials', None)
#     flask.session.pop('state', None)
#     flask.session.pop('user_info', None)
#
#     return redirect('/')
