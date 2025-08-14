import random
import flask as fl
import logging

logging.basicConfig(filename='serverlog.txt', level=logging.DEBUG)

app = fl.Flask(
	__name__,
	template_folder='templates',
	static_folder='static'
)

form = "<form method = 'post' action='/testform'><input type='text' name='q'><input type='submit'></form>"

@app.route('/')
def base_page():
    return(form)

@app.route('/testform', methods=['POST'])
def testform():
  q=fl.request.form['q']
  logging.info(f"Form submitted: {q}")
  logging.info(f"Form processing result: {q}")
  logging.info(f"Form submitted successfully with {q}")
  return (form)


if __name__ == "__main__":
	app.run(
		host='0.0.0.0',
		port=random.randint(2000, 9000)
    )
  