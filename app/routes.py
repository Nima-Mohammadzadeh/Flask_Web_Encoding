from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import DatabaseForm

@app.route('/')
@app.route('/index')
def Home():
    return render_template('index.html', title='Home')


@app.route('/job-setup', methods=['GET', 'POST'])
def job_setup():
    form = DatabaseForm()
    if form.validate_on_submit():
        flash('Databse Requested')

        return redirect(url_for('Home'))

    return render_template('job-setup.html', title='Job Setup', form=form )


   
