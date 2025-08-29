from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = 'q3x4ws4c3qwcum976545c'  # Set your secret key

@app.route("/")
@app.route("/home") 
def home():
    return render_template("base.html")


@app.route("/login")
def loginPage():
    if session.get("loggedIn") == True:
        return render_template("memberarea.html")
    return render_template("login.html")
    
@app.route("/memberarea", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "Daniel" and str(password) == "123":
        session["loggedIn"] = True
        return render_template("memberarea.html")
    else:
        return render_template("login.html", error="Username or Password incorrect!")
   

if __name__ == "__main__":
    app.run(host="localhost", port="8090",debug=True)