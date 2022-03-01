from typing import Dict
import json
import pytest

from ...func_test_tools import load_result, load_result_from_path, exist_in_path
from ...constants import *

# Fixtures

@pytest.fixture(scope='function', name="csv_one_read_book")
def csv_one_read_book_file(tmpdir_factory):
    """ Create a CSV file with just one book. """
    csv_text = '''Book Id,Title,Author,Author l-f,Additional Authors,ISBN,ISBN13,My Rating,Average Rating,Publisher,Binding,Number of Pages,Year Published,Original Publication Year,Date Read,Date Added,Bookshelves,Bookshelves with positions,Exclusive Shelf,My Review,Spoiler,Private Notes,Read Count,Recommended For,Recommended By,Owned Copies,Original Purchase Date,Original Purchase Location,Condition,Condition Description,BCID
35755822,Building Evolutionary Architectures: Support Constant Change,Neal Ford,"Ford, Neal","Rebecca Parsons, Patrick Kua","=""1491986360""","=""9781491986363""",0,3.76,O'Reilly Media,Paperback,190,2017,,,2021/12/16,,,read,,,,0,,,0,,,,,'''
    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(CSV_FILE_NAME)
    with file.open('w') as f:
        f.write(csv_text)
    return file

@pytest.fixture(scope='function', name="csv_one_to_read_book")
def csv_one_to_read_book_file(tmpdir_factory):
    """ Create a CSV file with just one book. """
    csv_text = '''Book Id,Title,Author,Author l-f,Additional Authors,ISBN,ISBN13,My Rating,Average Rating,Publisher,Binding,Number of Pages,Year Published,Original Publication Year,Date Read,Date Added,Bookshelves,Bookshelves with positions,Exclusive Shelf,My Review,Spoiler,Private Notes,Read Count,Recommended For,Recommended By,Owned Copies,Original Purchase Date,Original Purchase Location,Condition,Condition Description,BCID
35755822,Building Evolutionary Architectures: Support Constant Change,Neal Ford,"Ford, Neal","Rebecca Parsons, Patrick Kua","=""1491986360""","=""9781491986363""",0,3.76,O'Reilly Media,Paperback,190,2017,,,2021/12/16,to-read,to-read (#12),to-read,,,,0,,,0,,,,,'''
    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(CSV_FILE_NAME)
    with file.open('w') as f:
        f.write(csv_text)
    return file

@pytest.fixture(scope='function', name="csv_to_read_books_unsorted")
def csv_to_read_books_unsorted_file(tmpdir_factory):
    """ Create a CSV file with just one book. """
    csv_text = '''Book Id,Title,Author,Author l-f,Additional Authors,ISBN,ISBN13,My Rating,Average Rating,Publisher,Binding,Number of Pages,Year Published,Original Publication Year,Date Read,Date Added,Bookshelves,Bookshelves with positions,Exclusive Shelf,My Review,Spoiler,Private Notes,Read Count,Recommended For,Recommended By,Owned Copies,Original Purchase Date,Original Purchase Location,Condition,Condition Description,BCID
36398423,"Sarah (La Brigade des Cauchemars, #1)",Franck Thilliez,"Thilliez, Franck","Yomgui Dumont, DRAC","=""""","=""9782822221603""",4,3.81,Jungle,Hardcover,56,2017,2017,2021/10/16,2021/06/20,,,read,,,,1,,,0,,,,,
59207618,A Radical Enterprise: Pioneering the Future of High-Performing Organizations,Matt K Parker,"Parker, Matt K",,"=""1950508021""","=""9781950508020""",0,4.00,It Revolution Press,ebook,192,2022,,,2022/02/18,to-read,to-read (#18),to-read,,,,0,,,0,,,,,
4268826,"Growing Object-Oriented Software, Guided by Tests",Steve  Freeman,"Freeman, Steve",Nat Pryce,"=""0321503627""","=""9780321503626""",0,4.19,Addison-Wesley Professional,Paperback,345,2009,2009,,2022/02/18,to-read,to-read (#17),to-read,,,,0,,,0,,,,,
21343,The Five Dysfunctions of a Team: A Leadership Fable,Patrick Lencioni,"Lencioni, Patrick",,"=""0787960756""","=""9780787960759""",0,4.08,Jossey-Bass,Hardcover,227,2002,2002,,2022/01/13,to-read,to-read (#8),to-read,,,,0,,,0,,,,,
35755822,Building Evolutionary Architectures: Support Constant Change,Neal Ford,"Ford, Neal","Rebecca Parsons, Patrick Kua","=""1491986360""","=""9781491986363""",0,3.76,O'Reilly Media,Paperback,190,2017,,,2021/12/16,to-read,to-read (#12),to-read,,,,0,,,0,,,,,'''
    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(CSV_FILE_NAME)
    with file.open('w') as f:
        f.write(csv_text)
    return file
# Under test
from go_over.goodreads.processor import process

# Test
def test_not_to_read(csv_one_read_book, json_none, results_path):
    """ No to read file is created if there is not book to read. """
    # GIVEN a CSV source with not books to read
    # WHEN processing.
    process(csv_one_read_book, json_none, results_path, {})
    # THEN not "to read" file will be generated.
    assert not exist_in_path("books_to_read.json", results_path)

def test_one_to_read(csv_one_to_read_book, json_none, results_path):
    """ No want to read file is created if there is not book to read. """
    # GIVEN a CSV source with not books to read
    # WHEN processing.
    process(csv_one_to_read_book, json_none, results_path, {})
    # THEN not "want to read" file will be generated.
    assert exist_in_path("books_to_read.json", results_path)
    results = load_result("books_to_read.json", results_path)
    book = results['books'][0]
    assert book["id"] == '35755822'

def test_to_read_sort(csv_to_read_books_unsorted, json_none, results_path):
    """ to read books are sorted by possition. """
    # GIVEN a CSV source with 4 books to read
    # WHEN processing.
    process(csv_to_read_books_unsorted, json_none, results_path, {})
    # THEN The to read books will be sorted by position.
    results = load_result("books_to_read.json", results_path)
    books = results['books']
    assert books[0]["id"] == '21343'
    assert books[1]["id"] == '35755822'
    assert books[2]["id"] == '4268826'
    assert books[3]["id"] == '59207618'

def test_to_read_does_not_include_read(csv_to_read_books_unsorted, json_none, results_path):
    """ to read books contains only to read books. """
    # GIVEN a CSV source with 4 books to read and 1 read
    # WHEN processing.
    process(csv_to_read_books_unsorted, json_none, results_path, {})
    # THEN only to read books are listed in the to read file.
    results = load_result("books_to_read.json", results_path)
    books = results['books']
    assert len(books) == 4