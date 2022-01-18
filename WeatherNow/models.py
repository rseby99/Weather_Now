from sqlalchemy.orm import defaultload
from WeatherNow import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), default='', nullable=False)
    country = db.Column(db.String(50), default='', nullable=False)
    measurement_unit = db.Column(db.String(50), default='metric', nullable=False)

    def __repr__(self):
        return f"User('{self.id}' ,{self.email}', '{self.password}','{self.first_name}','{self.first_name}','{self.last_name}','{self.country}','{self.city}','{self.measurement_unit}')"