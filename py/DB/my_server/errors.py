from my_server import app
from flask import render_template


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error="404",desc="The page you're looking for doesn't exist."), 404

@app.errorhandler(401)
def page_not_found(e):
    return render_template('error.html',  error="401",desc="Unauthorized"), 401
