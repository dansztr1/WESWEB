from my_server import app
from flask import render_template, redirect, url_for, request

  
@app.route('/')
@app.route('/index')
def index():
 	return render_template("index.html")

