from ensurepip import bootstrap
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Edwin is the best'
bootstrap = Bootstrap(app)
moment = Moment(app)

class InfoForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    # add email and u of t to validators
    email = EmailField('What is your UofT email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    isUofT = 'utoronto' in session.get('email')
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), uoftEmail=isUofT)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500