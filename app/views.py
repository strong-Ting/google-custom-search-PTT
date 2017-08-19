from flask import render_template
from flask import send_from_directory

from app import app

@app.route('/')
@app.route('/index')
def index():
    
    return render_template('index.html')

