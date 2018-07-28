from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship

from fisher.models.base import Base, db
from fisher.models.wish import Wish

from fisher.spider.fisher_book import FisherBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False, unique=True)
    launched = Column(Boolean, default=False)

    @classmethod
    def recent(cls):
        #链式调用
        #主体：Query()对象
        #子函数,子函数返回的均是Query对象
        #触发函数（all(), first()）
        recent_gift = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift

    @property
    def book(self):
        fisher_book = FisherBook()
        fisher_book.search_by_isbn(self.isbn)
        return fisher_book.first

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == False,
                                      Wish.isbn.in_(isbn_list),
                                      Wish.status == 1).group_by(
            Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn':w[1]} for w in count_list]
        return count_list
