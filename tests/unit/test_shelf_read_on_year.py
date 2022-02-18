# More info at: https://vald-phoenix.github.io/pylint-errors/
# pylint: disable=C0114
# pylint: disable=C0116
from datetime import datetime
import pytest

from go_over.goodreads import Book, Bookshelf

# pylint: disable=C0301
# Line too long
# from 0 to 4 are 2019, 4 read 1 unread, 2 EN, 1 FR
# from 5 to 9 are 2020, 4 read 1 unread, 2 FR, 1 EN
BOOKS_MIX = [
    # unread
    {"Book Id": "00", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "currently-reading", "Date Read": "", "My Rating": "3"},
    {"Book Id": "01", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "", "My Rating": "3"},    
    {"Book Id": "02", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "", "My Rating": "3"},
    # 2019
    {"Book Id": "11", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2019/01/01", "My Rating": "3"},
    {"Book Id": "12", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2019/12/31", "My Rating": "3"},
    # 2020
    {"Book Id": "21", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2020/01/01", "My Rating": "3"},
    {"Book Id": "22", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2020/12/31", "My Rating": "3"}
]

# Read books a year

def test_books_read_on_given_year_with_no_results():
    shelf = Bookshelf()
    shelf.books = [Book(**b) for b in BOOKS_MIX]
    result = shelf.reads_on_year(2018)
    assert len(result) == 0

def test_books_read_on_given_year_with_results():
    shelf = Bookshelf()
    shelf.books = [Book(**b) for b in BOOKS_MIX]
    result = shelf.reads_on_year(2019)
    assert len(result) == 2

def test_books_read_on_given_year_with_results_sorted():
    shelf = Bookshelf()
    shelf.books = [Book(**b) for b in BOOKS_MIX]
    result = shelf.reads_on_year(2019)
    assert result[0].identifier == "12"
    assert result[1].identifier == "11"

# read on unkown date. Notice that the type is not BookRead but Book.

def test_books_with_no_read_date():
    shelf = Bookshelf()
    shelf.books = [Book(**b) for b in BOOKS_MIX]
    result = shelf.read_on_unkown_date()
    assert len(result) == 2


# Multiple reads in different years.

def test_multiple_reads_in_different_years():
    # Shelf with multiple books but not before 2015
    shelf = Bookshelf()
    shelf.books = [Book(**b) for b in BOOKS_MIX]
    # Add a book with reads in differnt years.
    a_book = Book(**{"Book Id": "110", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2010/01/01", "My Rating": "3"})
    a_book.add_reads(["2011/01/01", "2012/01/01"])
    shelf.books.append(a_book)
    # execute
    reads2010 = shelf.reads_on_year(2010)
    reads2011 = shelf.reads_on_year(2011)
    reads2012 = shelf.reads_on_year(2012)
    # verify
    assert len(reads2010) == 1
    assert reads2010[0].date == datetime(2010, 1, 1)
    assert reads2010[0].identifier == "110"
    assert len(reads2011) == 1
    assert reads2011[0].date == datetime(2011, 1, 1)
    assert reads2011[0].identifier == "110"
    assert len(reads2012) == 1
    assert reads2012[0].date == datetime(2012, 1, 1)
    assert reads2012[0].identifier == "110"


# Multiple reads in the same year.

def test_multiple_reads_in_a_year():
    # Shelf with multiple books but not before 2015
    shelf = Bookshelf()
    shelf.books = [Book(**b) for b in BOOKS_MIX]
    # Add a book with reads in differnt years.
    a_book = Book(**{"Book Id": "110", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2010/01/01", "My Rating": "3"})
    a_book.add_reads(["2011/01/01", "2011/02/01"])
    shelf.books.append(a_book)
    # execute
    reads2010 = shelf.reads_on_year(2010)
    reads2011 = shelf.reads_on_year(2011)
    # verify
    assert len(reads2010) == 1
    assert reads2010[0].date == datetime(2010, 1, 1)
    assert reads2010[0].identifier == "110"
    assert len(reads2011) == 2
    assert reads2011[0].date == datetime(2011, 2, 1)
    assert reads2011[0].identifier == "110"
    assert reads2011[1].date == datetime(2011, 1, 1)
    assert reads2011[1].identifier == "110"