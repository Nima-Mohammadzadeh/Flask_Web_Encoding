from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def Database_generation():
    return render_template('index.html', title='Database Generation')


   
