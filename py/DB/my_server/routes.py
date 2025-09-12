from my_server import app
from my_server.database import Posts, User, db

from werkzeug.utils import secure_filename
from datetime import datetime, timezone
from flask import Flask, render_template, redirect, url_for, request, session, current_app, abort
import os

@app.route("/") 
def home():
    posts = Posts.query.order_by(Posts.time.desc()).all()    
    return render_template("index.html", posts=posts)

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
        return abort(401)

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

        
        
    return render_template("memberarea.html", user=user)

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if not session.get("logged_in"):
        return abort(401)

    user = User.query.filter_by(username=session.get("username")).first()

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "change_form":
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")


            if user.password != current_password:
                return render_template("settings.html", user=user, error="Current password is incorrect.")

           
            if new_password != confirm_password:
                return render_template("settings.html", user=user, error="New passwords do not match.")

            user.password = new_password
            db.session.commit()
            return render_template("settings.html", user=user, success="Password updated successfully.")
        elif form_type == "image_form":
            # Handle profile image upload
            file = request.files.get("profile_image")
            if file and file.filename != "":
                filename = secure_filename(file.filename)
                upload_path = os.path.join(current_app.root_path, "static", "images", filename)
                file.save(upload_path)
                user.image = filename
                db.session.commit()
                

    return render_template("settings.html", user=user)
  
