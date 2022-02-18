# More info at: https://vald-phoenix.github.io/pylint-errors/
# pylint: disable=C0114
# pylint: disable=C0116
from datetime import datetime
import pytest

from go_over.goodreads import Book

# pylint: disable=C0301
# Line too long
BOOKS = [
    {"Book Id": "00", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "", "My Rating": "3"},
    {"Book Id": "01", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "2019/11/23", "My Rating": "3"},
    {"Book Id": "21", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "currently reading", "Date Read": "", "My Rating": "3"},
]

# defaults
def test_default_values():
    # Test that nothing will be updated when nothing is given in the complementary data.
    # Prepare
    complementary_data = {}
    book = Book(**BOOKS[0])
    # Execute
    book.update_with_complentary_data_dictionary(complementary_data)
    # Verify
    assert book.language == "EN"
    assert book.tags == ["nonfiction"]
    assert book.document_format == "audiobook"
    assert book.my_review_url is None
    assert not book.read_dates

# Language

def test_update_book_language():
    # Updating a book with a new language will set the new language 
    # Prepare
    complementary_data = {"language": "CAT"}
    book = Book(**BOOKS[0])
    # Execute
    book.update_with_complentary_data_dictionary(complementary_data)
    # Verify
    assert book.language == "CAT"

# Tags

def test_update_book_tags():
    # Updating a book with a new set of tags will set those tags.
    # Prepare
    complementary_data = {"tags": "novel, fiction"}
    book = Book(**BOOKS[0])
    # Execute
    book.update_with_complentary_data_dictionary(complementary_data)
    # Verify
    assert "novel" in book.tags
    assert "fiction" in book.tags
    assert len(book.tags) == 2

# review url

def test_update_book_review_url():
    # Updating a book with a new review URL
    # Prepare
    complementary_data = {"my_review_url": "/a_review_url/"}
    book = Book(**BOOKS[0])
    # Execute
    book.update_with_complentary_data_dictionary(complementary_data)
    # Verify
    assert book.my_review_url == "/a_review_url/"

# Read dates

def test_update_book_without_dates():
    # Updating a book without read data with one new date will update the book.
    # Prepare
    complementary_data = {"read_dates": ["2021/01/22"]}
    book = Book(**BOOKS[0])
    # Execute
    book.update_with_complentary_data_dictionary(complementary_data)
    # Verify
    assert len(book.read_dates) == 1
    assert datetime(2021, 1, 22) in book.read_dates

def test_update_book_with_more_than_one_date():
    # Updating a book with more than one day should add those dates. 
    # Prepare
    complementary_data = {"read_dates": ["2021/01/22", "2021/01/23"]}
    book = Book(**BOOKS[0])
    # Execute
    book.update_with_complentary_data_dictionary(complementary_data)
    # Verify
    assert len(book.read_dates) == 2
    assert datetime(2021, 1, 22) in book.read_dates
    assert datetime(2021, 1, 23) in book.read_dates

def test_update_book_with_dates():
    # Updating a book with read data will add the new date to the book the book.
    # Prepare
    complementary_data = {"read_dates": ["2021/01/22"]}
    book = Book(**BOOKS[1])
    # Execute
    book.update_with_complentary_data_dictionary(complementary_data)
    # Verify
    assert len(book.read_dates) == 2
    assert datetime(2021, 1, 22) in book.read_dates

def test_update_an_unread_book():
    # Updating a book that is not read will do nothing. 
    # Prepare
    complementary_data = {"read_dates": ["2021/01/22"]}
    book = Book(**BOOKS[2])
    # Execute
    book.update_with_complentary_data_dictionary(complementary_data)
    # Verify
    assert len(book.read_dates) == 0
