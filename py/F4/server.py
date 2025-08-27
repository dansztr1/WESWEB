from flask import Flask, render_template
import datetime;

app = Flask(__name__)

@app.route("/user") 
def user():
    return render_template("user.html", message="Ogiltig Sida!")

@app.route("/user/sven") 
def sven():
    return render_template("user.html", message="Hej Sven!")

@app.route("/user/sven/svensson") 
def svensson():
    return render_template("user.html", message="Hej Svensson!")

if __name__ == "__main__":
    app.run(host="localhost", port="8090",debug=True)