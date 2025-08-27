from flask import Flask, render_template
import datetime;

app = Flask(__name__)

@app.route("/minakompisar") 
def home():
    return render_template("friends.html", users=["Daniel", "Andreas"])

if __name__ == "__main__":
    app.run(host="localhost", port="8090",debug=True)