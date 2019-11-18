from server.models.auth.schema import User
from server.models.auth.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required, current_user
from flask import redirect, url_for, flash, render_template
from flask import Blueprint
from server import login_manager, db

auth_mold = Blueprint("auth", __name__)

def login_simple(username):
    user = User.query.filter_by(username=username).first()
    login_user(user)
    return "{} is now logged in".format(username)

@auth_mold.route('/login', methods=['GET', 'POST'])
def login():
    print('current_user: ', current_user)
    print('current_user.is_authenticated: ', current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect('/home')
    form = LoginForm()
    print('>>>form: ', form)
    print('form.validate_on_submit(): ', form.validate_on_submit())

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print('>>>user: ', user)
        print(">>>?>: form.password.data", form.password.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            print('>>>user is none')
            return redirect(url_for('auth.login'))
        print('>>>user is not none. Attempting login user')
        login_user(user, remember=form.remember_me.data)
        print('>>>somehow logined user')
        return redirect('../home')
    else:
        print('>>> redirecting ot login page')
        return render_template('login.html', title='Sign In', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_required
def logout():
    logout_user()
    print('>>> log out user')
    return redirect(url_for('index'))


@auth_mold.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('../home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.DATABASE.session.add(user)
        db.DATABASE.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)

@login_required
def exampleUser():
    return "the current auth is {}".format(current_user.username)
