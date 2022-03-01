# More info at: https://vald-phoenix.github.io/pylint-errors/
# pylint: disable=C0114
# pylint: disable=C0116
from datetime import datetime
import pytest

from go_over.goodreads import Book, BookRead, Bookshelf

# pylint: disable=C0301
# Line too long
BOOKS = [
    {"Book Id": "00", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "", "My Rating": "3","Bookshelves with positions": "to-read (#16)"},
    {"Book Id": "01", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2019/11/23", "My Rating": "3", "Bookshelves with positions": "to-read (#1)"},
    {"Book Id": "10", "Title": "Book 2", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2020/11/23", "My Rating": "3"},
]

# Last read

def test_book_with_position_on_known_bookshelf():
    book = Book(**BOOKS[0])
    assert book.to_read_position == 16

def test_book_with_position_on_unknown_bookshelf():
    book = Book(**BOOKS[1])
    assert book.to_read_position == 1

def test_book_without_position():
    book = Book(**BOOKS[2])
    assert book.to_read_position == 0