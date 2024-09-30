from flask_socketio import emit
from app import socketio
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

    form = DatabaseForm(request.form)
    
    current_serial = db.session.scalar(select(serialNumber.CurrentSerial))
    form.serial.data = current_serial 

    return render_template('job-setup.html', title='Job Setup', form=form )

def send_serial_update(new_serial):
    socketio.emit('update_serial', {'new_serial': new_serial})

@socketio.on('connect')
def handle_connect():
    current_serial = db.session.scalar(select(serialNumber.CurrentSerial))
    socketio.emit('update_serial', {'new_serial': current_serial})

@socketio.on('request_current_serial')
def handle_request_current_serial():
    current_serial = db.session.scalar(select(serialNumber.CurrentSerial))
    socketio.emit('update_serial', {'new_serial': current_serial})
def update_serial_number(form):
    try:
        qty = form.quantity.data
        adjusted_qty = helpers.calculate_adjusted_quantity(qty, form.two_percent.data, form.seven_percent.data)
        current_serial = db.session.scalar(select(serialNumber.CurrentSerial))
        new_serial = current_serial + adjusted_qty
        
        db.session.execute(update(serialNumber).values(CurrentSerial=new_serial))
        db.session.commit()
        return new_serial
    except Exception as e:
        db.session.rollback()
        print(f"Error updating serial number: {str(e)}")
        return None
    

@app.route('/download', methods=['POST'])
def download():
    form = DatabaseForm(request.form)
    if form.validate():
        new_serial = update_serial_number(form)
        if new_serial:
            send_serial_update(new_serial)
            excel_file = form.generate_excel_file()
            return send_file(
                excel_file, 
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True, 
                download_name= f'{form.UPC.data}-{form.serial.data}-{form.serial.data + form.quantity.data - 1}.xlsx'
            )
        else:
            return jsonify({'success': False, 'errors': ['Error updating serial number']}), 500
    else:
        # Collect all validation errors
        errors = []
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{getattr(form, field).label.text}: {error}")
        return jsonify({'success': False, 'errors': errors}), 400


@app.route('/roll_tracker')
def roll_tracker():
    return render_template('roll-tracker.html', title='Roll Tracker')