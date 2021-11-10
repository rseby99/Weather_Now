import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def landing_page():

    return render_template("landing_page.html")



@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city = request.form['city']
        country = request.form['country']

        url = "https://community-open-weather-map.p.rapidapi.com/weather"
        headers = {
            'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
            'x-rapidapi-key': "b9ac356800mshf0da663a66d341bp12b8e4jsn145828c1f17e"
        }

        querystring = {"q": f"{city},{country}"}

        weather_url = requests.request("GET", url, headers=headers, params=querystring).json()
        temp = weather_url['main']["temp"]
        humidity = weather_url["main"]["humidity"]
        wind_speed = weather_url["wind"]["speed"]
        print(weather_url)

        return render_template("result.html", city=city, temp=temp, humidity=humidity, wind_speed=wind_speed)

    return render_template("home.html")


if __name__ == '__main__':
    app.run(debug=True)