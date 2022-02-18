# More info at: https://vald-phoenix.github.io/pylint-errors/
# pylint: disable=C0114
# pylint: disable=C0116
import pytest

from go_over.goodreads import Book, BookRead, Bookshelf

# pylint: disable=C0301
# Line too long
BOOKS_MIX = [
    # unread
    {"Book Id": "00", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "currently-reading", "Date Read": "", "My Rating": "3"},
    {"Book Id": "01", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "", "My Rating": "3"},
    {"Book Id": "02", "Title": "Book 0", "Author": "Cervantes", "Exclusive Shelf": "read", "Date Read": "", "My Rating": "3"}
]

# Read books a year

#@pytest.mark.skip()
def test_getting_all_reads():
    # In a shelf with multiple books with multiple reads get them all.
    # Prepare
    shelf = Bookshelf()
    shelf.books = [Book(**b) for b in BOOKS_MIX]
    shelf.books[1].add_reads(["2019/01/01", "2020/01/01"])
    shelf.books[2].add_reads(["2018/01/01"])
    # Execute
    result = shelf.all_reads
    # Verify
    assert len(result) == 3
    print(result)
    for r in result:
        assert isinstance(r, BookRead)
