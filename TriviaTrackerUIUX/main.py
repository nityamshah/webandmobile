import flask as fk
import logging
import sqlite3

# connection = sqlite3.connect("questions.db")
# cursor = connection.cursor()
# """
# cursor.execute(
#   "CREATE TABLE IF NOT EXISTS questions (question TEXT NOT NULL, answer TEXT NOT NULL)"
# )
# """
logging.basicConfig(level=logging.DEBUG)

app = fk.Flask(
  __name__,
  static_folder="static",
  template_folder="templates",
)

selectedids = []

def get_connection():
  connection = sqlite3.connect("questions.db")
  connection.row_factory = dict_factory
  return connection

def dict_factory(cursor, row):
  d = {}
  for index, col in enumerate(cursor.description):
   d[col[0]] = row[index]
  return d

def write_add_question(q, a, e):
   return fk.render_template("index.html",question = q, answer = a, error = e)

def renderPage(page):
  return (fk.render_template(page))

@app.route('/', methods=["GET", "POST"])
def root():
  logging.info("***********************************************root")
  with sqlite3.connect("questions.db") as con:
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, answer TEXT, used INTEGER)")
    
  method = fk.request.method
  if method == "GET":
    with get_connection() as con:
      cursor = con.cursor()
      s = cursor.execute("SELECT * FROM questions")
      s = s.fetchall()
      # logging.info("**** TABLE: " + str(s))
      return (fk.render_template("home.html", questions = s))

@app.route('/addQuestion', methods=["GET", "POST"])
def addQuestion():
  method = fk.request.method
  if method == "POST":
    logging.info("**************************************A")
    question = fk.request.form["question"]
    answer = fk.request.form["answer"]
    error = ""
    if(question=="" or answer==""):
      error = "Field cannot be left blank"
      return write_add_question(question, answer, error)
    else:
      with get_connection() as con:
        s = con.cursor()
        insert_post = (question,answer,0)
        s.execute(
      "INSERT INTO questions (question, answer, used) VALUES (?, ?, ?)", insert_post)
        return fk.redirect("/addQuestion")
  else:  
    return write_add_question("", "", "")

@app.route('/selectQuestion', methods=["GET", "POST"])
def selectQuestion():
  if(fk.request.method == "GET"):
    with get_connection() as con:
      cursor = con.cursor()
      s = cursor.execute("SELECT * FROM questions")
      s = s.fetchall()
      logging.info("**** TABLE: " + str(s))
      return (fk.render_template("questions.html",questions = s))

@app.route('/selectQuestion/<id>', methods=["GET", "POST"])
def select(id):
  # make list clear everytime we open form link
  print(str(id))
  if id not in selectedids:
    selectedids.append(id)
  else:
    selectedids.remove(id)
  with get_connection() as con:
    cursor = con.cursor()
    s = cursor.execute("SELECT * FROM questions")
    s = s.fetchall()
    # logging.info("**** TABLE: " + str(s))
    return (fk.render_template("questions.html", questions = s, selected = selectedids))

@app.route('/selected', methods=["GET", "POST"])
def selected():
  #update database with the selected ids as used
  for x in selectedids:
    with sqlite3.connect("questions.db") as con:
      cursor = con.cursor()
      cursor.execute("UPDATE questions SET used = 1 WHERE id = ?", (x))
  return (fk.redirect('/selectQuestion')) # change to redirect

@app.route('/seeUsed', methods=["GET","POST"])
def seeUsed():
  with get_connection() as con:
    cursor = con.cursor()
    s = cursor.execute("SELECT * FROM questions")
    s = s.fetchall()
    return fk.render_template("used_questions.html", questions = s)

@app.route('/useAll', methods=["GET","POST"])
def useAll():
  with sqlite3.connect("questions.db") as con:
    cursor = con.cursor()
    cursor.execute("UPDATE questions SET used = 0")
  return (fk.redirect('/seeUsed'))


app.run(host='0.0.0.0', port='3000')
