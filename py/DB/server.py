from flask import Flask, render_template, redirect, url_for, request, session, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from datetime import datetime, timezone
from sqlalchemy import ForeignKey
import os
from werkzeug.utils import secure_filename

class Base(DeclarativeBase):
  pass

app = Flask(__name__)
db = SQLAlchemy(model_class=Base)
app.secret_key = "akdijewidju83ye287"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project2.db"
db.init_app(app)




class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]
    image: Mapped[str] = mapped_column(default="default_profile.jpg")
    posts = relationship("Posts", back_populates="user")

class Posts(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    time: Mapped[int]  # UNIX
    title: Mapped[str]
    content: Mapped[str]
    user = relationship("User", back_populates="posts") 

    
@app.route("/") 
def home():
    posts = Posts.query.order_by(Posts.time.desc()).all()    
    return render_template("index.html", posts=posts)

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
            session["logged_in"] = True
            session["username"] = user.username  
            return redirect(url_for("memberarea"))
        else:
            return render_template("login.html", error="Username or Password incorrect!")

    return render_template("login.html")

@app.route("/logout") 
def logout():
    session["logged_in"] = False
    return redirect(url_for("home"))


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
    
        user = User(
            username=username,
            email=email,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    
    return render_template("signup.html")




@app.route("/memberarea", methods=["GET", "POST"])
def memberarea():
    if not session.get("logged_in"):
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
