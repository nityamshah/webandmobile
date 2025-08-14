import flask as fk
import logging
import sqlite3
import time

connection = sqlite3.connect("blogbosts.db")
cursor = connection.cursor()
cursor.execute(
  "CREATE TABLE IF NOT EXISTS Art (title TEXT NOT NULL, art TEXT NOT NULL, created REAL NOT NULL)"
)

logging.basicConfig(level=logging.DEBUG)


def render_ascii(title="", art="", error=""):
  logging.info("in render ascii")
  connection = sqlite3.connect('blogbosts.db')
  cursor = connection.cursor()
  s = cursor.execute("SELECT * FROM Art ORDER BY created DESC")
  s = s.fetchall()
  logging.info(s)
  return (fk.render_template('home.html',
                             title=title,
                             art=art,
                             error=error,
                             arts=s))


app = fk.Flask(
  __name__,
  static_folder="static",
  template_folder="templates",
)


@app.route('/', methods=["GET", "POST"])
def root():
  method = fk.request.method
  if method == "GET":
    logging.info("********** root GET **********")
    return (render_ascii())


@app.route('/formPage', methods=["GET", "POST"])
def form_Handler():
  logging.info("in form handler")
  title = fk.request.form['title']
  art = fk.request.form['art']
  if (title == "" or art == ""):
    return (render_ascii(title=title,
                         art=art,
                         error="Need both a title and artwork!!"))

  else:
    created = time.time()
    logging.debug(title)
    logging.debug(art)
    logging.debug(created)
    connection = sqlite3.connect("blogbosts.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Art (title, art, created) VALUES (?, ?, ?)",
                   (title, art, created))
    connection.commit()
    return render_ascii()


app.run(host='0.0.0.0', port='3000')
