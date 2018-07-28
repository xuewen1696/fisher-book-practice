from flask import jsonify, request, flash, render_template

from fisher.models.gift import Gift
from fisher.models.wish import Wish
from fisher.spider.fisher_book import FisherBook
from fisher.libs.helper import is_isbn_or_key
from fisher.view_models.book import BookViewModel, BookCollection
from . import web
from fisher.models.book import Book
from fisher.forms.book import SearchForm
import json


@web.route('/book/search/')
def search():
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        # q = request.args['q']
        # page = request.args['page']   #immitableDict: 不可变字典
        # # a = request.args.to_dict()  #将不可变字典转换为原生字典
        # #request 是LocalProxy代理对象，只有通过HTTP请求走视图函数，request对象内才有与请求相关的数据（request必须在请求与响应上下文环境中使用）
        isbn_or_key = is_isbn_or_key(q)
        fisher_book = FisherBook()

        if isbn_or_key == 'isbn':
            fisher_book.search_by_isbn(q)
        else:
            fisher_book.search_by_keyword(q, page)

        books.fill(fisher_book, q)
        # return json.dumps(result), 200, {'conten-type': 'application/json'}
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books)


@web.route('/kkk')
def time_line():
    return '666'


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    fisher_book = FisherBook()
    fisher_book.search_by_isbn(isbn)
    book = BookViewModel(fisher_book.first)

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()
    return render_template('book_detail.html', book=book, wishes=[], gifts=[])
