from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b867cf8704988f0363c0a4b92ae45bef'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from WeatherNow import routespip