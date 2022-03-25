import os
from flask_login import LoginManager, login_user
from flask import Flask, render_template, redirect
from data import db_session
from data.user import User
from login import LoginForm
from reg import RegForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route("/session_test")
def session_test():
    visits_count = db_session.get('visits_count', 0)
    db_session['visits_count'] = visits_count + 1
    return db_session(
        f"Вы пришли на эту страницу {visits_count + 1} раз")

@app.route('/autorize_image')
def promotion():
    return 'Авторизация успешна'


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect("/autorize_image")
        return render_template('autorize.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('autorize.html', title='Авторизация', form=form)




@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.email = form.email.data
        user.password = form.password.data
        db_sess.add(user)
        db_sess.commit()
        return redirect("/")

    return render_template('registration.html', title='Авторизация', form=form)


if __name__ == '__main__':
    db_session.global_init(os.path.join(os.getcwd(), 'app.db'))
    app.run(port=8080, host='127.0.0.1')
