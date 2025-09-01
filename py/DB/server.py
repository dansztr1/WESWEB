from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import Integer, String


class Base(DeclarativeBase):
  pass

app = Flask(__name__)
db = SQLAlchemy(model_class=Base)
app.secret_key = "akdijewidju83ye287"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str] 
    
    
@app.route("/") 
def home():
    return render_template("base.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session["loggedIn"] = True
            session["username"] = user.username  # store username in session
            return redirect(url_for("memberarea"))
        else:
            return render_template("login.html", error="Username or Password incorrect!")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"]) 
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing_user:
            error_msg = "Username or email already taken."
            return render_template("signup.html", error=error_msg)
        
        # If no duplicates, create new user
        user = User(
            username=username,
            email=email,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    
    return render_template("signup.html")



@app.route("/memberarea")
def memberarea():
    if not session.get("loggedIn"):
        return redirect(url_for("login"))
    return render_template("memberarea.html")

    
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="localhost", port="8090",debug=True)
