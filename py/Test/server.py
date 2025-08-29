from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
app = Flask(__name__)

app.secret_key = 'q3x4ws4c3qwcum976545c'  # Set your secret key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=True, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref='author', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"


@app.route("/")
@app.route("/home") 
def home():
    return render_template("base.html")



@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "Daniel" and str(password) == "123":
            session["loggedIn"] = True
            return redirect("/memberarea")
        else:
            return render_template("login.html", error="Username or Password incorrect!")
    else:
        return render_template("login.html")
        
    
   
@app.route("/memberarea")
def member():
    if session.get("loggedIn") == True:
        return render_template("memberarea.html")
    else:
        return redirect("/login")
    


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="localhost", port="8090",debug=True)