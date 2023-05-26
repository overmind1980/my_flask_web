from flask import Flask,render_template,request,redirect,session
import traceback
from db import pool
from config import app
from user.user_manager import app_user

app.register_blueprint(app_user)

@app.route('/')
def hello():
    return """<a href="./user/">user_manager</a>"""

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port="3012")
