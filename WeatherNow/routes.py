from math import e
from flask_login.utils import login_required
from WeatherNow.models import User
from flask import render_template, request, flash, redirect, url_for
from WeatherNow.forms import RegistrationForm, LoginForm, UserSettingsForm, GetWeatherForm
from WeatherNow import app
from WeatherNow import bcrypt
from WeatherNow import db
from flask_login import login_user, current_user, logout_user
from WeatherNow.get_data import get_data, get_data_7days

  


@app.route('/', methods=['GET', 'POST'])
def home():
    
    form = GetWeatherForm()

    if current_user.is_authenticated:
        unit = current_user.measurement_unit
    else:
        unit = 'metric'

    if form.validate_on_submit():
        if form.get_current_weather.data:
            return redirect(url_for('results',city=form.city.data, country=form.country.data, unit=unit))
        elif form.get_weather_7days.data:
            return redirect(url_for('results_7_days',city=form.city.data, country=form.country.data, unit=unit))
               
    elif request.method == 'GET' and current_user.is_authenticated:
        form.city.data = current_user.city
        form.country.data = current_user.country
        return render_template("home.html", form=form)
    else:
        return render_template("home.html", form=form)


@app.route('/results',methods=['GET'])
def results():
    try:
        if current_user.is_authenticated:
            weather = get_data(request.args.get('city'),request.args.get('country'),request.args.get('unit'))
            return render_template('result.html', weather=weather, unit=request.args.get('unit'))
        else:
            weather = get_data(request.args.get('city'),request.args.get('country'),'metric')
            return render_template('result.html', weather=weather, unit='metric')

    except KeyError:
        flash('The city or country you entered is not valid !', 'danger')
        return redirect(url_for('home'))
    except e:
        return e


@app.route('/results7days', methods=['GET'])
@login_required
def results_7_days():
    try:
        weather_data = get_data_7days(request.args.get('city'),request.args.get('country'),request.args.get('unit'))
        return render_template('result_7days.html', weather_data=weather_data, unit=request.args.get('unit'))
    except KeyError:
        flash('The city or country you entered is not valid !', 'danger')
        return redirect(url_for('home'))
    except e:
        return e

    

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password, first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password !', 'danger')
            
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UserSettingsForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.city  = form.city.data
        current_user.country = form.country.data
        current_user.measurement_unit = form.unit.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.city.data = current_user.city
        form.country.data = current_user.country
        form.unit.data = current_user.measurement_unit

    return render_template('account.html', title='Account', form=form)