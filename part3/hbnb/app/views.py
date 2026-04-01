from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/index')
def index():
    return render_template('index.html')


@views.route('/login')
def login():
    return render_template('login.html')


@views.route('/place')
def place():
    return render_template('place.html')


@views.route('/add_review')
def add_review():
    return render_template('add_review.html')
