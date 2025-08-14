# See the finished product here: https://Cookies-2.alexyang4.repl.co
import flask as fk
import logging
import hashlib   #import the python hash function library
import hmac

def write_site(message=""):
    return fk.render_template('main.html', message=message)

def hash_str(s): 
  #return the hashdigest created by hashlib's md5 hash of str(s).encode("utf-8")
  #return hashlib.md5(str(s).encode("utf-8")).hexdigest()
  SECRET='imsosecret'
  return hmac.new(SECRET.encode("utf-8"),s.encode("utf-8"), hashlib.md5).hexdigest()


def make_secure_val(s):
    # return string that is a concatenation of s + '|' + hash_str(s))) - '+' symbols represent a concatenation operations.
  return str(s) + "|" + hash_str(s)

# Take the string with  visits and the hash and return the confirmed results.
def check_secure_val(h):
    h_arr = h.split("|")
    s = h_arr[0]
    hash = h_arr[1]
    if (hash_str(s) == hash):
      return s
    else:
      return None
    # return s if the hash_str(s) equals hash, otherwise return None

app = fk.Flask(
    __name__,
    static_folder="stylesheets"
)

def get_msg(visits):
    msg = "Visits: %i" % visits
    if visits == 10000: msg = "Congrats! You are our 10,000th customer!"
    return msg

@app.route('/', methods=["GET"])
def root():
    method = fk.request.method
    if method == "GET":
        msg = ""
        # Get the number of visits from the request's cookie
        hash_visits = fk.request.cookies.get('visits')
        if hash_visits:
            # Get the confirmed number of visits in hash_visits by calling check_secure_val 
            visits = check_secure_val(hash_visits)
            if visits:
                visits = int(visits) + 1
                msg = get_msg(visits)
                #update the visits count
            else:
                # Warn the user "Don't mess with my cookie!"
                msg="Don't mess with my cookie!"
        else:
            visits = 1
            msg=get_msg(visits)
        # Prepare the response object
        resp = fk.make_response(write_site(msg))
        # Set the response's cookie with 'visits', by making a _secure_val
        resp.set_cookie("visits", make_secure_val(str(visits)))
        return(resp)

app.run(host='0.0.0.0', port='3000')