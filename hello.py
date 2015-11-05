from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/turn-eye/<int:eye_index>/<int:degree>", methods=['GET'])
def turn_eye(eye_index, degree):
  return "Kaanto %d %d" % (degree, eye_index)

if __name__ == "__main__":
  app.run(host='0.0.0.0')
