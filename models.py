from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(255), nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.username)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.username)


class Murmure(db.Model):
    __tablename__ = 'murmures'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    subtext = db.Column(db.Text, nullable=False)
    publishdate = db.Column(db.Date, unique=True)
