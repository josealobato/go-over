# More info at: https://vald-phoenix.github.io/pylint-errors/
# pylint: disable=C0114
# pylint: disable=C0116
from datetime import datetime
import pytest

from go_over.goodreads import Book, BookRead

# pylint: disable=C0301
# Line too long
BOOKS = [
    {"Book Id": "01", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2019/11/23", "My Rating": "3"},
]

# Last read

def test_unread_book_date():
    # create a bookread
    # prepare
    book = Book(**BOOKS[0])
    # execute
    bookread = BookRead(book, datetime(2020, 10, 24))
    # verify
    read = bookread.exportable_dictionary
    assert read["id"] == "01"
    assert read["date"] == "2020-10-24"
    assert read["read_number"] == "1"