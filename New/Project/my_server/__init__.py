from flask import Flask 

app = Flask(__name__)
app.secret_key = 'sehu2he98'


from my_server import routes