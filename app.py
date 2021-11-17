#resources

#https://www.youtube.com/watch?v=4EJwK56pE1Y&t=534s
#https://www.youtube.com/watch?v=w_VHabMAM1c&t=216s

import os
import boto3
from flask import Flask, g, session
from flask import request
from flask import render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from dotenv import load_dotenv, find_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(find_dotenv())
# read the .env-sample, to load the environment variable.
dotenv_path = os.path.join(os.path.dirname(__file__), ".env-sample")
load_dotenv(dotenv_path)

client = boto3.client("cognito-idp", region_name="us-east-2")

app = Flask(__name__)
app.secret_key = "super secret key"

# landing Page

@app.route('/', methods=['POST', 'GET'])
def login():
    return render_template ('login.html')

# when you click register
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template ('signup.html')


# when you click the contact button after you log in
@app.route('/contact', methods=['POST', 'GET'])
def contact():
    print(session['accesscode'])
    return render_template ('table.html')

# when you click home button after you log in
@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template ('index.html')


# gathers the information from the signup page and sends you to the access code page
@app.route('/accesscode', methods=['POST', 'GET'])
def access():
    session['name'] = request.form.get("comname")
    session['email'] = request.form.get("comemail")
    session['number'] = request.form.get("comphone")
    session['password'] = request.form.get("compassword")

    # Sign up passed to cognito
    signUp(client, str(session['name']), str(session['password']), str(session['email']), str(session['number']))

    return render_template ('accesscode.html')

#this function pulls in the access code and sends you to the login page
@app.route('/login', methods=['POST', 'GET'])
def backtologin():
    session['accesscode'] = request.form.get("accesscode")
    print(session["accesscode"])

    # Verification passed to cognito
    confirmUser(client, str(session['name']), str(session['accesscode']))

    return render_template ('login.html')

#this function checks what you enter when you log in and compares the values to what they entered on signup
@app.route('/index', methods=['POST', 'GET'])
def index():

    # use this one
    # it returns the index page which is the home page



    return render_template ('index.html')

# This function passes relevant info to cognito for user signup
def signUp(client, username, password, email, phoneNumber):
    # The below code, will do the sign-up
    response = client.sign_up(
        ClientId=os.getenv("COGNITO_USER_CLIENT_ID"),
        Username = username,
        Password = password,
        UserAttributes = [{ "Name": "email", "Value": email},{"Name": "phone_number", "Value": phoneNumber}],
        )

# This function passes relevant info to cognito for user confirmation post sign-up
# Confirm code is sent to email adress, must be input through the UI
def confirmUser(client, username, confirm_code):
# Below API sends the confirmation code back to cognito.
    response = client.confirm_sign_up(
        ClientId = os.getenv("COGNITO_USER_CLIENT_ID"),
        Username = username,
        ConfirmationCode = confirm_code,
)

if __name__ == '__main__':
    app.run(debug=True)
