# See the finished product here: https://Blog-1.alexyang4.repl.co
import flask as fk
import logging

def write_site(message=""):
    return fk.render_template('main.html', message=message)

app = fk.Flask(
    __name__,
    static_folder="stylesheets"
)

@app.route('/', methods=["GET"])
def root():
    # Get the requst from flask
    method = fk.request.method
    # Is ita a get method
    if method=="GET":
        msg = ""
        # Get the number of visits from the request's cookie
        visits = fk.request.cookies.get("visits")
        
        # If the request does not include "visits" or visits is not a digit, set visits to 0
        if visits is None or not visits.isdigit(): visits = 0
        # Otherwise update the server count of visits
        else: visits = int(visits)
        visits += 1
        
        # if this is the 10000th vistor congratulate them
        if visits == 10000: msg = "Congrats! You are our 10,000th customer!"
        else: msg = "Visits: %i" % visits
        print(msg)
        
        # make the response with call to write_site
        resp = fk.make_response(write_site(msg))
        #set the cookie to visits and the current count of visits
        resp.set_cookie("visits", str(visits))
        # return the response
        return(resp)

app.run(host='0.0.0.0', port='3000')
