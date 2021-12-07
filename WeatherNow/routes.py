from WeatherNow.models import User
from flask import render_template, request, flash, redirect, url_for
from WeatherNow.forms import RegistrationForm, LoginForm
from WeatherNow import app
from WeatherNow import bcrypt
from WeatherNow import db
from flask_login import login_user







# @app.route('/', methods=['GET', 'POST'])
# def landing_page():

#     return render_template("landing_page.html")
    


@app.route('/', methods=['GET', 'POST'])
def home():
    # if request.method == 'POST':
    #     city = request.form['city']
    #     country = request.form['country']

    #     url = "https://community-open-weather-map.p.rapidapi.com/weather"
    #     headers = {
    #         'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
    #         'x-rapidapi-key': "b9ac356800mshf0da663a66d341bp12b8e4jsn145828c1f17e"
    #     }

    #     querystring = {"q": f"{city},{country}"}

    #     weather_url = requests.request("GET", url, headers=headers, params=querystring).json()
    #     temp = weather_url['main']["temp"]
    #     humidity = weather_url["main"]["humidity"]
    #     wind_speed = weather_url["wind"]["speed"]
    #     print(weather_url)

    #     return render_template("result.html", city=city, temp=temp, humidity=humidity, wind_speed=wind_speed)

    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
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
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password !', 'danger')
            
    return render_template('login.html', title='Login', form=form)