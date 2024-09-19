from flask import render_template, flash, redirect, request, url_for
from app import app
from app.forms import DatabaseForm 
from app.models import serialNumber
from sqlalchemy import select, update
from app import db
from io import BytesIO
from flask import send_file
import openpyxl

@app.route('/')
@app.route('/index')
def Home():
    return render_template('index.html', title='Home')


@app.route('/job-setup', methods=['GET', 'POST'])
def job_setup():

    form = DatabaseForm()
    qty = form.quantity.data
    current_serial = db.session.scalar(select(serialNumber.CurrentSerial))
    form.serial.data = current_serial

   

    if form.validate_on_submit():
        if form.two_percent.data:            
            qty += int(qty * 0.02)
        if form.seven_percent.data:
            qty += int(qty * 0.07)

        new_serial = current_serial + qty
        serialNumber.query.update({serialNumber.CurrentSerial: new_serial})
        db.session.commit()

        return redirect(url_for('download'), code=307)
        
    return render_template('job-setup.html', title='Job Setup', form=form )


@app.route('/download', methods=['POST'])
def download():
    form = DatabaseForm(request.form)
    if form.validate():
        excel_file = form.generate_excel_file()  # Remove the 'form' argument here

        return send_file(
            excel_file, 
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True, 
            download_name= f'{form.UPC.data}-{form.serial.data}-{form.serial.data + form.quantity.data - 1}.xlsx'
        )
    else:
        flash('Error in form')
        return redirect(url_for('job_setup'))
