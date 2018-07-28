class BookViewModel:
    ##将鱼书API得到的数据进行统一
    def __init__(self, book):
        self.title = book['title'],
        self.publisher = book['publisher'],
        self.author = '、'.join(book['author']),
        self.pages = book['pages'] or '',
        self.price = book['price'],
        self.summary = book['summary'] or '',
        self.image = book['image']
        self.isbn = book['isbn']
        self.pubdate = book['pubdate']
        self.binding = book['binding']


class BookCollection:
    def __init__(self):
        self.books = []
        self.total = 0
        self.keyword = ''

    def fill(self, books, keyword):
        self.total = books.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in books.books]


class __BookViewModel:
    # 描述特征 （类变量， 实例变量）
    # 行为 （方法）

    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = cls.__cut_book_data(data)
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = len(data['total'])
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'author': '、'.join(data['author']),
            'pages': data['pages'] or '',
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']
        }
        return book
