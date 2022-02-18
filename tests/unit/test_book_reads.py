# More info at: https://vald-phoenix.github.io/pylint-errors/
# pylint: disable=C0114
# pylint: disable=C0116
from datetime import datetime
import pytest

from go_over.goodreads import Book, BookRead, Bookshelf

# pylint: disable=C0301
# Line too long
BOOKS = [
    {"Book Id": "00", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "", "My Rating": "3"},
    {"Book Id": "01", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2019/11/23", "My Rating": "3"},
    {"Book Id": "10", "Title": "Book 2", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2020/11/23", "My Rating": "3"},
    {"Book Id": "21", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "currently reading", "Date Read": "", "My Rating": "3"},
]

# Last read

def test_unread_book_date():
    # A book without date read will have no last read date
    book = Book(**BOOKS[0])
    assert book.last_read == None

def test_read_book_date():
    # A book with one read date return that date as its last read
    book = Book(**BOOKS[1])
    assert book.last_read == datetime(2019, 11, 23)

# Adding dates

def test_adding_read_dates_to_a_book():
    # Adding read dates to a book with no read will store those dates
    book = Book(**BOOKS[0])
    book.add_reads(["2019/11/23", "2020/10/14"])
    assert len(book.read_dates) == 2

def test_adding_read_dates_to_a_book_with_date():
    # Adding read dates to a book with that that will do nothing
    book = Book(**BOOKS[1])
    book.add_reads(["2018/01/11", "2020/10/14"])
    assert len(book.read_dates) == 3

def test_adding_read_dates_to_a_book_with_that_date():
    # Adding read dates to a book with that that will do nothing
    book = Book(**BOOKS[1])
    book.add_reads(["2019/11/23", "2020/10/14"]) # The first one exist
    assert len(book.read_dates) == 2

# Last read when adding dates

def test_adding_read_dates_can_change_last_read():
    # Adding a newer date will update the last read date.
    book = Book(**BOOKS[1])
    book.add_reads(["2020/10/14"])
    assert book.last_read == datetime(2020, 10, 14)

def test_adding_old_read_dates_wont_change_last_read():
    # Adding old read date wont change the last read.
    book = Book(**BOOKS[1])
    book.add_reads(["2010/10/14"])
    assert book.last_read == datetime(2019, 11, 23)

# Read on year

def test_unread_book_not_read_in_year():
    book = Book(**BOOKS[0])
    assert book.read_on_year(2019) == False

def test_read_book_read_in_year():
    book = Book(**BOOKS[1])
    assert book.read_on_year(2019) == True

def test_check_positive_read_on_multiple_read():
    book = Book(**BOOKS[0])
    book.add_reads(["2020/01/01", "2019/01/01"])
    assert book.read_on_year(2018) is False
    assert book.read_on_year(2019) is True
    assert book.read_on_year(2020) is True
    assert book.read_on_year(2021) is False

# Read on unknown date

def test_book_read_on_unknown_date():
    book = Book(**BOOKS[0])
    assert book.read_in_unknown_date is True

def test_book_not_read_on_unknown_date():
    book = Book(**BOOKS[3])
    assert book.read_in_unknown_date is False

# all reads

def test_get_all_reads():
    # get all the reads from a book
    book = Book(**BOOKS[0])
    book.add_reads(["2020/01/01", "2019/01/01"])
    # Execute
    reads = book.reads()
    # Vefiry
    assert len(reads) == 2
    for read in reads:
        assert isinstance(read, BookRead)

# reads order

def test_read_order_when_not_sorted():
    # get all the reads from a book
    book = Book(**BOOKS[0])
    book.add_reads(["2020/01/01", "2019/01/01"])
    # Execute
    reads = book.reads()
    # Vefiry
    assert len(reads) == 2
    assert reads[0].date ==  datetime(2019, 1, 1)
    assert reads[0].read_number == 1
    assert reads[1].date == datetime(2020, 1, 1)
    assert reads[1].read_number == 2

def test_read_order_when_sorted():
    # get all the reads from a book
    book = Book(**BOOKS[0])
    book.add_reads(["2019/01/01", "2020/01/01"])
    # Execute
    reads = book.reads()
    # Vefiry
    assert len(reads) == 2
    assert reads[0].date ==  datetime(2019, 1, 1)
    assert reads[0].read_number == 1
    assert reads[1].date == datetime(2020, 1, 1)
    assert reads[1].read_number == 2