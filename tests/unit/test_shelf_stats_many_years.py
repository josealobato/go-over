# More info at: https://vald-phoenix.github.io/pylint-errors/
# pylint: disable=C0114
# pylint: disable=C0116
import pytest

from go_over.goodreads import Book, Bookshelf

# pylint: disable=C0301
# Line too long
# from 0 to 4 are 2019, 4 read 1 unread, 2 EN, 1 FR
# from 5 to 9 are 2020, 4 read 1 unread, 2 FR, 1 EN
BOOKS_MIX = [
    {"Book Id": "00", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2019/11/23", "My Rating": "3"},
    {"Book Id": "01", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2019/11/23", "My Rating": "3"},
    {"Book Id": "01", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2019/11/23", "My Rating": "3"},
    {"Book Id": "03", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2019/11/23", "My Rating": "3"},
    {"Book Id": "04", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "currently-reading", "Date Read": "", "My Rating": "3"},
    {"Book Id": "10", "Title": "Book 2", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2020/11/23", "My Rating": "3"},
    {"Book Id": "11", "Title": "Book 2", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2020/11/23", "My Rating": "3"},
    {"Book Id": "12", "Title": "Book 3", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2020/11/23", "My Rating": "3"},
    {"Book Id": "13", "Title": "Book 4", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2020/11/23", "My Rating": "3"},
    {"Book Id": "14", "Title": "Book 1", "Author": "Cervantes", "Exclusive Shelf": "currently-reading", "Date Read": "", "My Rating": "3"}
]

# Read books a year

def test_load_books():
    shelf = Bookshelf()
    shelf.books = [Book(**b) for b in BOOKS_MIX]
    shelf.books[3].language = "FR"
    shelf.books[5].language = "FR"
    shelf.books[6].language = "FR"
    # assert shelf is not None
    assert len(shelf.books) == 10
    stats = shelf.statistics
    assert stats["2019"]["read"] == 4
    assert stats["2020"]["read"] == 4
