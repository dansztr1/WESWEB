from flask import Flask, render_template, request, session

app = Flask(__name__)
session['loggedIn'] = False

@app.route("/") # @ = Decorator, lägger funktionaliet. "När vi kommer till index så kommer home funktionen köras"
@app.route("/home") 
def home():
    return render_template("base.html")


@app.route("/login")
def loginPage():
    return render_template("login.html")
    
@app.route("/memberarea", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "Daniel" and str(password) == "123":
        session["loggedIn"] = True,
        return render_template("memberarea.html")
    else:
        return render_template("login.html", error="Username or Password incorrect!")
   

if __name__ == "__main__":
    app.run(host="localhost", port="8090",debug=True)