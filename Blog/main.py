# Lab: BLOG-1
import flask as fk
import re
import logging
import sqlite3
from datetime import datetime
from dateutil import tz
import pytz
from pytz import timezone


def write_posts(posts):
  return fk.render_template("posts.html", posts=posts)


def write_perma_post(post=[]):
  post = post[0]
  return fk.render_template("post.html", post=post)


def write_new_post(subject="", content="", error=""):
  return (fk.render_template('newpost.html',
                             ph_subject=subject,
                             ph_content=content,
                             ph_error=error))


def get_connection():
  connection = sqlite3.connect("blogbosts.db")
  connection.row_factory = dict_factory
  return connection


def to_cst(time):
  format1 = "%Y-%m-%d %H:%M:%S.%f"
  format2 = "%A %B %d, %Y %H:%M:%S"
  time = datetime.strptime(time, format1)
  time = time.astimezone(pytz.timezone('US/Central'))
  return (time.strftime(format2))


app = fk.Flask(__name__,
               template_folder='templates',
               static_folder='stylesheets')


def dict_factory(cursor, row):
  d = {}
  for index, col in enumerate(cursor.description):
    d[col[0]] = row[index]
  return d


def get_posts():
  connection = get_connection()
  cursor = connection.cursor()
  p = cursor.execute("SELECT * FROM posts ORDER BY create_date DESC limit 10")
  p = p.fetchall()
  return p


def get_fav():
  return ("hello!")


@app.route('/', methods=["GET", "POST"])
def root():
  #return (fk.render_template("base_post.html"))
  return fk.redirect('/blog/')


#... ('/', m...)
#... ('/blog', m...,strict_slashes=False)
@app.route('/blog', methods=["GET"], strict_slashes=False)
def blog():
  con = get_connection()
  cursor = con.cursor()
  cursor.execute(
      "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, create_date TEXT, subject TEXT, content TEXT)"
  )
  s = cursor.execute("SELECT * FROM posts ORDER BY create_date DESC")
  print([x for x in s])
  return (write_posts(get_posts()))


@app.route('/blog/newpost', methods=["GET", "POST"], strict_slashes=False)
def new_post():
  method = fk.request.method
  if method == "GET":
    return (write_new_post("", "", ""))

  if method == "POST":
    subject = fk.request.form['subject']
    content = fk.request.form['content']
    print(subject, content)
    if (subject == "" or content == ""):
      return write_new_post(subject, content,
                            "Please provide both a subject and content")
    else:
      created = to_cst(str(datetime.now()))
      connection = get_connection()
      cursor = connection.cursor()
      cursor.execute(
          "INSERT INTO posts (create_date, subject, content) VALUES (?, ?, ?)",
          (created, subject, content))
      id = cursor.execute("SELECT id FROM posts ORDER BY id DESC limit 1")
      id = id.fetchall()
      connection.commit()
      id = id[0]['id']
      return fk.redirect('/blog/' + str(id))


@app.route('/blog/<post_id>', methods=["GET"])
def permapost(post_id):
  connection = get_connection()
  cursor = connection.cursor()
  post = cursor.execute("SELECT * FROM posts WHERE id=?", (post_id, ))
  post = post.fetchall()
  print(post)
  return (write_perma_post(post))


app.run(host='0.0.0.0', port='3000')
