from fisher.libs.http_fisher import HTTP
from flask import current_app


class FisherBook:
    pre_page = 15
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&start={}&count={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn)
        ##self.isbn_url 也可以取到isbn_url---链式查找
        result = HTTP.get(url)
        self.__fill_single(result)

    def search_by_keyword(self, keyword, page=1):
        # url = cls.keyword_url.format(keyword, current_app.config['PRE_PAGE'], cls.calculate_start(page))
        url = self.keyword_url.format(keyword, self.calculate_start(page), current_app.config['PRE_PAGE'])
        result = HTTP.get(url)
        self.__fill_collection(result)

    @staticmethod
    def calculate_start(page):
        return (page - 1)*current_app.config['PRE_PAGE']

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    @property
    def first(self):
        return self.books[0] if self.total >= 1 else None
