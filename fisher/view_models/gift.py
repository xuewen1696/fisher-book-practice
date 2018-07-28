
from collections import namedtuple

from fisher.view_models.book import BookViewModel

# MyGift = namedtuple('MyGift', ['id', 'book', 'count'])


class MyGifts:
    def __init__(self, wish_count_list, gifts_of_mine):
        self.gifts = []
        self.__wish_count_list = wish_count_list
        self.__gifts_of_mine = gifts_of_mine

        self.gifts = self.__parse()

    def __parse(self):
        temp_gifts = []
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count.isbn:
                count = wish_count['count']
        r = {
            'id': gift.id,
            'book': BookViewModel(gift.book),
            'count': count
        }
        my_gift = r
        return my_gift
