# Lab instructions on BLEND

import flask as fk
#  # ** YOUR CODE HERE ** -> import .....
import html
import logging
import re

logging.basicConfig(level=logging.DEBUG)


def valid_user(user):
  try:
    ret = re.search("^[a-zA-z0-9_-]{3,20}$", user).group(0) == user
  except AttributeError:
    ret = False
  return ret


def valid_pass(password):
  # YOUR CODE HERE
  try:
    ret = re.search("^.{3,20}$", password).group(0) == password
  except AttributeError:
    ret = False
  return ret


def valid_email(email):
  # ** YOUR CODE HERE **
  #r'(\S)*@(\S)*\.(\S)*
  try:
    ret = re.search("^$|\S+@\S+\.\S+$", email).group(0) == email
  except AttributeError:
    ret = False
  return ret


def pass_match(password, verify):
  # ** YOUR CODE HERE **
  return (password == verify)


success = """
<!DOCTYPE HTML>
<html>	
  <head>
    <style>
      img{height:300px;}
    </style>
  </head>
  <body>
    <h1>Welcome, %(username)s!<h1>
    <img src="https://cdn.europosters.eu/image/750/art-photo/cute-giraffe-i96090.jpg">
  </body>
</html>
"""

form = """
<!DOCTYPE HTML>
<html>
  <head>
    <style>
      h1{color: red;}
      label{
        display: block;
        float: left;
        width : 120px;    
        color: blue;
      }
    </style>
  </head>
  <body>
    <h1>Signup</h1>
    <form method = "post" action="/formPage">
    <table>
      <tr>
        <td><label>Username</label></td>
        <td><input type="text" name="username" value="%(user)s"}></td>
        <td><span style="color: red"> %(usernameerror)s </span><br></td>
      </tr>

      <tr>
        <td><label>Password</label></td>
        <td><input type="password" name="password"></td>
        <td><span style="color: red"> %(passworderror)s </span><br></td>
      </tr>

      <tr>
        <td><label>Verify Password</label></td>
        <td><input type="password" name="verify"><br></td>
      </tr>

      <tr>
        <td><label>Email (optional)</label></td>
        <td><input type="text" name="email" value=%(email)s></td>
        <td><span style="color: red"> %(emailerror)s </span><br></td>
      </tr>

      <tr>
        <td><input type="submit"></td>
      </tr>
    </table>
    </form>
  </body>
</html>
"""


def write_form(user="",
               email="",
               usernameerror="",
               passworderror="",
               emailerror=""):
  return (form % {
      "user": user,
      "email": email,
      "usernameerror": usernameerror,
      "passworderror": passworderror,
      "emailerror": emailerror
  })


app = fk.Flask(__name__, static_folder="stylesheets")


@app.route('/', methods=["GET", "POST"])
def root():
  logging.debug("in main page")
  return write_form(usernameerror="", passworderror="", emailerror="")


@app.route('/formPage', methods=["GET", "POST"])
def form_Handler():
  logging.debug("in form handler")

  global username
  username = fk.request.form['username']
  password = fk.request.form['password']
  verify = fk.request.form['verify']
  email = fk.request.form['email']

  #logging.debug(username, password, verify, email)

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
    logging.debug("error")
    return write_form(username, email, usererror, passworderror, emailerror)
  else:
    logging.debug("no error")
    return (fk.redirect(fk.url_for("welcome")))


@app.route('/welcome', methods=["GET", "POST"])
def welcome():
  logging.debug("in welcome")
  #username = fk.request.form['username']
  return (success % {"username": username})


app.run(host='0.0.0.0', port='3000')
