from flask import render_template
import flask as fk
import re

app = fk.Flask(__name__, template_folder='templates', static_folder='static')


def valid_user(user):
  try:
    ret = re.search("^[a-zA-z0-9_-]{3,20}$", user).group(0) == user
  except AttributeError:
    ret = False
  return ret


def valid_pass(password):
  try:
    ret = re.search("^.{3,20}$", password).group(0) == password
  except AttributeError:
    ret = False
  return ret


def valid_email(email):
  try:
    ret = re.search("^$|\S+@\S+\.\S+$", email).group(0) == email
  except AttributeError:
    ret = False
  return ret


def pass_match(password, verify):
  return (password == verify)


def write_form(user="",
               email="",
               usernameerror="",
               passworderror="",
               emailerror=""):
  return (fk.render_template("home.html",
                             user=user,
                             email=email,
                             usernameerror=usernameerror,
                             passworderror=passworderror,
                             emailerror=emailerror))


@app.route('/', methods=["GET", "POST"])
def root():
  return write_form(user="",
                    email="",
                    usernameerror="",
                    passworderror="",
                    emailerror="")


@app.route('/formPage', methods=["GET", "POST"])
def form_Handler():

  global username
  username = fk.request.form['username']
  password = fk.request.form['password']
  verify = fk.request.form['verify']
  email = fk.request.form['email']

  usererror = ""
  passworderror = ""
  emailerror = ""

  if not (valid_user(username)):
    usererror = "invalid username"
  if not (valid_pass(password)):
    passworderror = "invalid password"
  if not (pass_match(password, verify)):
    passworderror = "passwords do not match"
  if not (valid_email(email)):
    emailerror = "invalid email"

  if (not valid_email(email) or not valid_user(username)
      or not valid_pass(password) or not pass_match(password, verify)):
    return write_form(username, email, usererror, passworderror, emailerror)
  else:
    return (fk.redirect(fk.url_for("welcome")))


@app.route('/welcome', methods=["GET", "POST"])
def welcome():
  return (fk.render_template("welcome.html", username=username))


app.run(host='0.0.0.0', port='3000')
