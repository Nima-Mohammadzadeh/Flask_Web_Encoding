from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import DatabaseForm
from app.models import serialNumber
from sqlalchemy import select, update
from app import db

@app.route('/')
@app.route('/index')
def Home():
    return render_template('index.html', title='Home')


@app.route('/job-setup', methods=['GET', 'POST'])
def job_setup():

    form = DatabaseForm()

    current_serial = db.session.scalar(select(serialNumber.CurrentSerial))
    form.serial.data = current_serial


   

    if form.validate_on_submit():
        flash('Databse Requested')
        new_serial = current_serial + form.quantity.data
        serialNumber.query.update({serialNumber.CurrentSerial: new_serial})
        db.session.commit()

        return redirect(url_for('job_setup'))

    return render_template('job-setup.html', title='Job Setup', form=form )


   
