# More info at: https://vald-phoenix.github.io/pylint-errors/
# pylint: disable=C0114
# pylint: disable=C0116
import pytest

from go_over.goodreads import Book, Bookshelf

# pylint: disable=C0301
# Line too long
BOOKS_MIX = [
    {"Book Id": "09", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2019/11/23", "My Rating": "3"},
    {"Book Id": "10", "Title": "Book 1", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2021/11/23", "My Rating": "3"},
    {"Book Id": "11", "Title": "Book 2", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2021/11/23", "My Rating": "3"},
    {"Book Id": "12", "Title": "Book 3", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2022/11/23", "My Rating": "3"},
    {"Book Id": "13", "Title": "Book 4", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2022/11/23", "My Rating": "3"}
]

# Read books a year

BOOKS_2021_READ_UNREAD_MIX = [
    {"Book Id": "09", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2021/11/23", "My Rating": "3"},
    {"Book Id": "10", "Title": "Book 1", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2021/11/23", "My Rating": "3"},
    {"Book Id": "11", "Title": "Book 2", "Author": "Cervantes", "Exclusive Shelf": "currently-reading", "Date Read": "", "My Rating": "3"}
]

def test_load_books():
    shelf = Bookshelf()
    shelf.books = [Book(**b) for b in BOOKS_MIX]
    # assert shelf is not None
    assert len(shelf.books) == 5

def test_zero_books_a_year():
    # prepare
    shelf = Bookshelf()
    # execute
    stats = shelf.statistics_for_year(2019)
    assert stats["read"] == 0

def test_one_book_a_year():
    # prepare
    shelf = Bookshelf()
    shelf.books = [Book(**BOOKS_MIX[0])]
    # execute
    stats = shelf.statistics_for_year(2019)
    assert stats["read"] == 1

def test_some_books_a_year():
    """Not taking into account unread books"""
    # prepare
    shelf = Bookshelf()
    shelf.books = [Book(**b) for b in BOOKS_2021_READ_UNREAD_MIX]
    # execute
    stats = shelf.statistics_for_year(2021)
    assert stats["read"] == 2

    # Read by language
# Notice that language is set a posteriory
BOOKS_2021_READ_BY_LANGUAGE_MIX = [
    {"Book Id": "00", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2021/11/23", "My Rating": "3"},
    {"Book Id": "01", "Title": "Book 1", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2021/11/23", "My Rating": "3"},
    {"Book Id": "02", "Title": "Book 2", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2021/11/23", "My Rating": "3"},
    {"Book Id": "03", "Title": "Book 3", "Author": "Cervantes", "Exclusive Shelf": "currently-reading", "Date Read": "", "My Rating": "3"},
    {"Book Id": "04", "Title": "Book 4", "Author": "Cervantes", "Exclusive Shelf": "currently-reading", "Date Read": "", "My Rating": "3"}
]

def test_read_by_language_in_a_year():
    # prepare
    shelf = Bookshelf()
    shelf.books = [Book(**b) for b in BOOKS_2021_READ_BY_LANGUAGE_MIX]
    shelf.books[0].language = "EN"
    shelf.books[1].language = "EN"
    shelf.books[2].language = "FR"
    shelf.books[3].language = "EN" #unread
    shelf.books[4].language = "FR" #unread
    # execute
    stats = shelf.statistics_for_year(2021)
    assert stats["languages"]["EN"] == 2
    assert stats["languages"]["FR"] == 1

def test_read_by_language_in_a_year_if_none():
    # prepare
    shelf = Bookshelf()
    shelf.books = [Book(**b) for b in BOOKS_2021_READ_BY_LANGUAGE_MIX]
    # execute
    stats = shelf.statistics_for_year(2026)
    assert stats["languages"] == {}