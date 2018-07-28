from fisher.models.gift import Gift
from . import web
from fisher.view_models.book import BookViewModel
from flask import render_template

__author__ = '七月'


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)


@web.route('/personal')
def personal_center():
    pass
