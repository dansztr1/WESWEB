from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from datetime import datetime, timezone
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
  pass

app = Flask(__name__)
db = SQLAlchemy(model_class=Base)
app.secret_key = "akdijewidju83ye287"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project2.db"
# initialize the app with the extension
db.init_app(app)




class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]
    image: Mapped[str] = mapped_column(default="default_profile.jpg")

    # optional: backref to posts
    posts = relationship("Posts", back_populates="user")

class Posts(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))  # foreign key to User
    time: Mapped[int]  # UNIX timestamp
    title: Mapped[str]
    content: Mapped[str]
    user = relationship("User", back_populates="posts")  # link to User

    
@app.route("/") 
def home():
    # Get Posts
    posts = Posts.query.order_by(Posts.time.desc()).all()
    
    return render_template("base.html", posts=posts)

@app.template_filter("timestamp_to_datetime")
def timestamp_to_datetime(unix_time):
    return datetime.fromtimestamp(int(unix_time)).strftime('%Y-%m-%d %H:%M')

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



import os
from werkzeug.utils import secure_filename
from flask import current_app

@app.route("/memberarea", methods=["GET", "POST"])
def memberarea():
    if not session.get("loggedIn"):
        return redirect(url_for("login"))

    user = User.query.filter_by(username=session.get("username")).first()

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "post_form":
            # Handle new post creation
            title = request.form.get("title")
            content = request.form.get("content")
            time_now = datetime.now(timezone.utc).timestamp()

            post = Posts(
                user_id=user.id,
                time=time_now,
                content=content,
                title=title
            )
            db.session.add(post)
            db.session.commit()

        elif form_type == "image_form":
            # Handle profile image upload
            file = request.files.get("profile_image")
            if file and file.filename != "":
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.root_path, "static", "images", filename)
                file.save(upload_path)
                user.image = filename
                db.session.commit()

    return render_template("memberarea.html", user=user)

    
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="localhost", port="8090",debug=True)
