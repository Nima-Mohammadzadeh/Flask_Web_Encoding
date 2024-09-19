from flask import render_template, flash, redirect, request, url_for
from app import app
from app.forms import DatabaseForm 
from app.models import serialNumber
from sqlalchemy import select, update
from app import db
from io import BytesIO
from flask import send_file
import openpyxl
from utils import helpers


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
        if form.submit.data:

            qty = form.quantity.data           
            adjusted_qty = helpers.calculate_adjusted_quantity(qty, form.two_percent.data, form.seven_percent.data)
            

            new_serial = current_serial + adjusted_qty
            serialNumber.query.update({serialNumber.CurrentSerial: new_serial})
            db.session.commit()

            return redirect(url_for('download'), code=307)
        
        

    return render_template('job-setup.html', title='Job Setup', form=form )



@app.route('/download', methods=['POST'])
def download():
    form = DatabaseForm(request.form)
    if form.validate():
        excel_file = form.generate_excel_file()
        return send_file(
            excel_file, 
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True, 
            download_name= f'{form.UPC.data}-{form.serial.data}-{form.serial.data + form.quantity.data - 1}.xlsx'
        )
    else:
        flash('Error in form')
        return redirect(url_for('job_setup'))
    


@app.route('/roll_tracker')
def roll_tracker():
    return render_template('roll-tracker.html', title='Roll Tracker')