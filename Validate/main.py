from os import write
import flask as fl
import random
import logging
import html
def escape_html(s):
   return html.escape(s)

logging.basicConfig(level=logging.DEBUG)

form = """
What is your birthday?<br>
<form method = "post" action = "/formPage">
<label>Month</label><input type="text" name="month" value="%(month)s">
<label>Day</label><input type="text" name="day" value="%(day)s">
<label>Year</label><input type="text" name="year" value="%(year)s"><br><br>
<div style="color: red"> %(error)s </div>  
<input type="submit">
</form>
"""

app = fl.Flask(
	__name__
)

def valid_day(d):
  return (0<d<32)

def valid_month(m):
  months = ["Jan" , "Feb" , "Mar" , "Apr" , "May" , "Jun" , "Jul", "Aug" , "Sep" , "Oct" , "Nov" , "Dec"]
  for x in months:
    if m.startswith(x): return(True)
  return(False)

def valid_year(y):
  return (1900<y<2020)

def valid_date(m,d,y):
  if d.isdigit() and y.isdigit():
    d = int(d)
    y = int(y)
    return (valid_day(d) and valid_month(m) and valid_year(y))
  return (False)

def write_form(error="", month="", day="", year=""):
  return(form % { "month": escape_html(month), "day": escape_html(day), "year": escape_html(year), "error": error})

@app.route('/')
def hello_world():
    return write_form(error="")\

@app.route('/success')
def success_fn():
  logging.debug("in success")
  return ("Thanks! That is a day that exists.")
  
@app.route('/formPage', methods=['POST'])
def form_Handler():
  logging.debug("in form handler")
  month=fl.request.form['month']
  day=fl.request.form['day']
  year=fl.request.form['year']
  if valid_date(month,day,year):
    #return ("Thanks! That is a day that exists.")
    return(fl.redirect(fl.url_for("success_fn")))
  else:
    return (write_form("Invalid date.", month, day, year))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=random.randint(2000, 9000))