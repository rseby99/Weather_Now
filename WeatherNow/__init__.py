from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b867cf8704988f0363c0a4b92ae45bef'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['API_KEY'] = 'b9ac356800mshf0da663a66d341bp12b8e4jsn145828c1f17e'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from WeatherNow import routes