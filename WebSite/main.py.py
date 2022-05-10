from flask import Flask, render_template, redirect, request
from data import db_session
from data.Users_table import User
from data.Lesson_table import Lesson

from forms.registration import RegisterForm
from forms.login import LoginForm
from forms.add_lesson import AddingLessonForm
from forms.my_text import MyTextForm

from flask_login import LoginManager, login_required, logout_user, login_user, current_user

from requests import get

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# Менеджер для регистрации и авторизации
login_manager = LoginManager()
login_manager.init_app(app)

# Это для правильной работы менджера регистрации и авторизации
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main_main():
    return render_template('index.html')


@app.route('/info')
def info():
    return render_template('info.html')


# Страница с карточками уроков
@login_required
@app.route('/lessons')
def lessons():
    db_sess = db_session.create_session()
    lessons = db_sess.query(Lesson).filter(Lesson.id != 999, Lesson.id != 998).all()
    return render_template('lessons.html', lessons=lessons)


# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Почта уже используется")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


# Страница авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# Выход из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Страница с информацией об аккаунте
@login_required
@app.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html', user=current_user)


# Страница урока с определённым id
@login_required
@app.route('/lesson/<int:id>', methods=['GET'])
def lesson(id):
    db_sess = db_session.create_session()
    text = db_sess.query(Lesson).filter(Lesson.id == id).first()
    words_list = [list(i + ' ') for i in text.typing_text.split()]
    words_list[-1] = words_list[-1][:-1]
    return render_template('lesson.html', words_list=words_list)


# А это не страница, а адрес, которому передаёт данные js-код для последующего внесения их в бд
@login_required
@app.route('/lesson/<int:id>/done', methods=['GET', 'POST'])
def lesson_done(id):
    # Получение данных из request.data и их конвертирование
    data = str(request.data)[2:-1]
    time, letters_count = data[:4], int(data[5:])
    minutes = int(time[0]) + int(time[2:]) / 60

    # внесение данных сначала в таблицу с уроком, затем в таблицу с пользователем
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.id == id).first()
    lesson.done, lesson.time, lesson.average_speed = True, time, letters_count / minutes

    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.lessons_done = user.lessons_done + 1
    db_sess.commit()
    return '1' # это return нафиг не нужен, потому что ответ тоже нафиг не нужен, важны лишь внесения изменений в бд


# Страница с данными о только что пройденном уроке. По сути, сейчас для этого бд можно и не использовать,
# но я потом сделаю крутую штуку, для которой это надо и которую сейчас написать не успею
@login_required
@app.route('/lesson/<int:id>/info', methods=['GET', 'POST'])
def lesson_info(id):
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.id == id).first()
    return render_template('lesson_info.html', time=lesson.time, average_speed=lesson.average_speed, id=lesson.id)


# Это снова адрес для связки данных клиента (js-код) и сервера, только для загруженного текста
@login_required
@app.route('/lesson/my_text/done', methods=['GET', 'POST'])
def lesson_my_text_done():
    id = 999  # у загруженного текста такой id
    # Получение данных из request.data и их конвертирование
    data = str(request.data)[2:-1]
    time, letters_count = data[:4], int(data[5:])
    minutes = int(time[0]) + int(time[2:]) / 60

    # внесение данных сначала в таблицу с уроком, затем в таблицу с пользователем
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.id == id).first()
    lesson.done, lesson.time, lesson.average_speed = True, time, letters_count / minutes

    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.lessons_done = user.lessons_done + 1
    db_sess.commit()
    return '1' # это return нафиг не нужен, потому что ответ тоже нафиг не нужен, важны лишь внесения изменений в бд

# Информация по уроку с загруженным текстом
@login_required
@app.route('/lesson/my_text/info', methods=['GET', 'POST'])
def lesson_my_textinfo():
    id = 999  # у загруженного текста такой id
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.id == id).first()
    return render_template('lesson_info.html', time=lesson.time, average_speed=lesson.average_speed, id=lesson.id)


# Два ниже - то же самое, что и два выше, но для рандомного (API) текста
@login_required
@app.route('/lesson/random_text/done', methods=['GET', 'POST'])
def lesson_random_text_done():
    id = 998  # у загруженного текста такой id
    # Получение данных из request.data и их конвертирование
    data = str(request.data)[2:-1]
    time, letters_count = data[:4], int(data[5:])
    minutes = int(time[0]) + int(time[2:]) / 60

    # внесение данных сначала в таблицу с уроком, затем в таблицу с пользователем
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.id == id).first()
    lesson.done, lesson.time, lesson.average_speed = True, time, letters_count / minutes

    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user.lessons_done = user.lessons_done + 1
    db_sess.commit()
    return '1' # это return нафиг не нужен, потому что ответ тоже нафиг не нужен, важны лишь внесения изменений в бд


@login_required
@app.route('/lesson/random_text/info', methods=['GET', 'POST'])
def lesson_random_text_tinfo():
    id = 998  # у загруженного текста такой id
    db_sess = db_session.create_session()
    lesson = db_sess.query(Lesson).filter(Lesson.id == id).first()
    return render_template('lesson_info.html', time=lesson.time, average_speed=lesson.average_speed, id=lesson.id)



# Страница с API, где генерируется рандомный текст
@login_required
@app.route('/lesson/random_text', methods=['GET'])
def random_text_lesson():
    answer_json = get('https://fish-text.ru/get?format=json&number=1').json()
    text = answer_json['text']
    # Деление текста на список с добавлением пробелов к какждому слову
    words_list = list(map(lambda x: x + ' ', text.split(' ')))
    # Удаление пробела у последнего слова
    words_list[-1] = words_list[-1][:-1]
    return render_template('lesson.html', words_list=words_list)


# Страница с добавлением урока
@login_required
@app.route('/add_lesson', methods=['GET', 'POST'])
def add_lesson():
    form = AddingLessonForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        lesson = Lesson(
            typing_text = form.text_field.data
        )
        db_sess.add(lesson)
        db_sess.commit()
        return redirect('/')
    return render_template('add_lesson.html', form=form)


# Страница с уроком загруженного текста
@login_required
@app.route('/lesson/my_text', methods=['GET'])
def my_text_lesson():
    with open('user_texts/user_text.txt', 'r', encoding='utf8') as file:
        # замена переносов строки на пробелыи тут же замена двойных (если несколько \n подряд) пробелов на одинарные
        words_list = file.read().replace('\n', ' ').replace('  ', ' ')
        # Деление текста на список с добавлением пробелов к какждому слову
        words_list = list(map(lambda x: x + ' ', words_list.split(' ')))
        # Удаление пробела у последнего слова
        words_list[-1] = words_list[-1][:-1]
    return render_template('lesson.html', words_list=words_list)


@login_required
@app.route('/my_text', methods=['GET', 'POST'])
def my_text():
    form = MyTextForm()
    if request.method == 'GET':
        return render_template('my_text.html', form=form, message='')
    if request.method == 'POST':
        if request.files['file'].content_type == 'text/plain':
            text = request.files['file']
            text.save('user_texts/user_text.txt')
            return redirect('/lesson/my_text')
        return render_template('my_text.html', form=form, message='Загружать можно только .txt файлы')


def main():
    db_session.global_init("DataBases/main_db.db")
    app.run()


if __name__ == '__main__':
    main()
