from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import DatabaseForm
from app.models import serialNumber
from sqlalchemy import select
from app import db

@app.route('/')
@app.route('/index')
def Home():
    return render_template('index.html', title='Home')


@app.route('/job-setup', methods=['GET', 'POST'])
def job_setup():

    form = DatabaseForm()

    query = select(serialNumber.CurrentSerial)
    query_result = db.session.execute(query)
    serial = query_result.scalar_one_or_none()


   

    if form.validate_on_submit():
        flash('Databse Requested')


        return redirect(url_for('Home'))

    return render_template('job-setup.html', title='Job Setup', form=form )


   
