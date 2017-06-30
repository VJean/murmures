import os, sys
import pushover
from flask import Flask
from flask import flash, render_template, redirect, url_for, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from datetime import date

from forms import LoginForm, MurmureForm
from util import require_username, is_safe_url
from models import db, Murmure, User


if not os.path.isfile("./config.py"):
    print('Please copy default_config.py to config.py and fill it with your own data.')
    sys.exit()

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

bcrypt = Bcrypt(app)
lm = LoginManager(app)

db.app = app
db.init_app(app)
db.create_all()

lm.login_view = 'login'

pushover_client = pushover.Client(app.config['PUSHOVER_USER_KEY'], api_token=app.config['PUSHOVER_API_KEY'])


def notify_few_remaining(message):
    pushover_client.send_message(message, title="Murmures", url=url_for(add), url_title="Ajouter un murmure")


@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)

                next = request.args.get('next')
                # is_safe_url should check if the url is safe for redirects.
                # See http://flask.pocoo.org/snippets/62/ for an example.
                if not is_safe_url(next):
                    return abort(400)

                return redirect(next or url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    murmure = Murmure.query.filter(Murmure.publishdate == date.today()).first()
    if murmure is None:
        murmure = Murmure.query.filter(Murmure.publishdate == None).order_by(Murmure.id).first()
        if murmure is not None and current_user.username == 'alexia':
            murmure.publishdate = date.today()
            db.session.commit()
            left = Murmure.query.filter(Murmure.publishdate == None).all()
            nleft = len(left)
            if nleft == 1:
                notify_few_remaining("Il ne reste plus qu'un murmure à voir.")
            elif nleft == 0:
                notify_few_remaining("Le dernier murmure a été vu.")
    return render_template('index.html', murmure=murmure)


@app.route('/add', methods=['GET', 'POST'])
@require_username('jean', 'index')
def add():
    form = MurmureForm()
    new_murmure = Murmure()
    if form.validate_on_submit():
        form.populate_obj(new_murmure)
        db.session.add(new_murmure)
        db.session.commit()
        return redirect(url_for('add'))

    murmures = Murmure.query.order_by(Murmure.id.desc()).all()
    return render_template('add.html', form=form, murmures=murmures)


@app.route('/edit/<int:mid>', methods=['GET', 'POST'])
@require_username('jean', 'index')
def edit(mid):
    form = MurmureForm()
    m = Murmure.query.get(mid)

    if m is None:
        flash('The requested item does not exist.')
        return redirect(url_for('index'))
    elif m.publishdate is not None:
        flash('Cannot edit an item that has alreay been displayed.')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        m.content = form.content.data
        m.subtext = form.subtext.data
        db.session.commit()
        return redirect(url_for('index'))

    form.content.data = m.content
    form.subtext.data = m.subtext

    return render_template('edit.html', form=form)


if __name__ == '__main__':
    app.run()
