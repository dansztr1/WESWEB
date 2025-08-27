from flask import Flask, render_template
import datetime;

app = Flask(__name__)

@app.route("/") # @ = Decorator, lägger funktionaliet. "När vi kommer till index så kommer home funktionen köras"
@app.route("/index") 
def home():
    return render_template("index.html", users=["Daniel", "Andreas"])

@app.route("/hej") 
def hej():
    return render_template("hej.html", user="Daniel")

@app.route("/date") 
def date():
    return render_template("date.html", date=datetime.datetime.now().date())

if __name__ == "__main__":
    app.run(host="localhost", port="8090",debug=True)