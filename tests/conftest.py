from typing import Dict
import pytest
import json
import os

SOURCE_DATA_PATH = 'source_data'
CSV_FILE_NAME = 'goodreads.csv'
JSON_COMPLEMENT_FILE = 'complement.json'
RESULTS_PATH = 'results'

# Fixtures

# Goodreads CSV files fixtures

@pytest.fixture(scope='function', name="csv_one_book")
def csv_one_book_file(tmpdir_factory):
    """ Create a CSV file with just one book. """
    csv_text = '''Book Id,Title,Author,Author l-f,Additional Authors,ISBN,ISBN13,My Rating,Average Rating,Publisher,Binding,Number of Pages,Year Published,Original Publication Year,Date Read,Date Added,Bookshelves,Bookshelves with positions,Exclusive Shelf,My Review,Spoiler,Private Notes,Read Count,Recommended For,Recommended By,Owned Copies,Original Purchase Date,Original Purchase Location,Condition,Condition Description,BCID
57343730,"Super Learning: Advanced Strategies for Quicker Comprehension, Greater Retention, and Systematic Expertise",Peter Hollins,"Hollins, Peter",,"=""""","=""""",3,4.19,,Kindle Edition,228,2021,,2022/02/17,2022/02/10,,,read,"I wasn’t expecting much from this book. I have already read many books about learning methodologies and how learning works in humans. But, I enjoyed these types of books and wanted to give another take on the subject.<br/><br/>During the first part of the book, I thought I had made a mistake starting it. Not only I wasn’t learning anything new, but the book felt slow. Thankfully, the second half of the book is much more enjoyable. Especially chapters 4 (Make learning secondary) and 5 (Teaching to learn) are exciting and inspiring. Nothing surprising but inspiring.<br/><br/>In general, and in the end, there is nothing new for me in the book, but it is a fine read. It is short and to the point, and I think it would make a perfect book as a first read on the subject. If you have not read any other essay on learning, this one could be a good entry point.<br/><br/>See it in my blog [josealobato.com](https://josealobato.com/peter-hollins-super-learning)",,,1,,,0,,,,,'''

    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(CSV_FILE_NAME)
    # run with -s --setup-show  to see this
    # print("file:{}".format(str(file)))
    with file.open('w') as f:
        f.write(csv_text)
    return file

@pytest.fixture(scope='function', name="csv_one_unread_book")
def csv_one_unread_book_file(tmpdir_factory):
    """ Create a CSV file with just one book. """
    csv_text = '''Book Id,Title,Author,Author l-f,Additional Authors,ISBN,ISBN13,My Rating,Average Rating,Publisher,Binding,Number of Pages,Year Published,Original Publication Year,Date Read,Date Added,Bookshelves,Bookshelves with positions,Exclusive Shelf,My Review,Spoiler,Private Notes,Read Count,Recommended For,Recommended By,Owned Copies,Original Purchase Date,Original Purchase Location,Condition,Condition Description,BCID
57343730,"Super Learning: Advanced Strategies for Quicker Comprehension, Greater Retention, and Systematic Expertise",Peter Hollins,"Hollins, Peter",,"=""""","=""""",3,4.19,,Kindle Edition,228,2021,,,2022/02/10,,,read,"I wasn’t expecting much from this book. I have already read many books about learning methodologies and how learning works in humans. But, I enjoyed these types of books and wanted to give another take on the subject.<br/><br/>During the first part of the book, I thought I had made a mistake starting it. Not only I wasn’t learning anything new, but the book felt slow. Thankfully, the second half of the book is much more enjoyable. Especially chapters 4 (Make learning secondary) and 5 (Teaching to learn) are exciting and inspiring. Nothing surprising but inspiring.<br/><br/>In general, and in the end, there is nothing new for me in the book, but it is a fine read. It is short and to the point, and I think it would make a perfect book as a first read on the subject. If you have not read any other essay on learning, this one could be a good entry point.<br/><br/>See it in my blog [josealobato.com](https://josealobato.com/peter-hollins-super-learning)",,,1,,,0,,,,,'''

    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(CSV_FILE_NAME)
    # run with -s --setup-show  to see this
    # print("file:{}".format(str(file)))
    with file.open('w') as f:
        f.write(csv_text)
    return file

@pytest.fixture(scope='function', name="csv_one_book_plus_empty_line")
def csv_one_book_file_plus_empty_line(tmpdir_factory):
    """ Create a CSV file with just one book. """
    csv_text = '''Book Id,Title,Author,Author l-f,Additional Authors,ISBN,ISBN13,My Rating,Average Rating,Publisher,Binding,Number of Pages,Year Published,Original Publication Year,Date Read,Date Added,Bookshelves,Bookshelves with positions,Exclusive Shelf,My Review,Spoiler,Private Notes,Read Count,Recommended For,Recommended By,Owned Copies,Original Purchase Date,Original Purchase Location,Condition,Condition Description,BCID
57343730,"Super Learning: Advanced Strategies for Quicker Comprehension, Greater Retention, and Systematic Expertise",Peter Hollins,"Hollins, Peter",,"=""""","=""""",3,4.19,,Kindle Edition,228,2021,,2022/02/17,2022/02/10,,,read,"I wasn’t expecting much from this book. I have already read many books about learning methodologies and how learning works in humans. But, I enjoyed these types of books and wanted to give another take on the subject.<br/><br/>During the first part of the book, I thought I had made a mistake starting it. Not only I wasn’t learning anything new, but the book felt slow. Thankfully, the second half of the book is much more enjoyable. Especially chapters 4 (Make learning secondary) and 5 (Teaching to learn) are exciting and inspiring. Nothing surprising but inspiring.<br/><br/>In general, and in the end, there is nothing new for me in the book, but it is a fine read. It is short and to the point, and I think it would make a perfect book as a first read on the subject. If you have not read any other essay on learning, this one could be a good entry point.<br/><br/>See it in my blog [josealobato.com](https://josealobato.com/peter-hollins-super-learning)",,,1,,,0,,,,,
'''
    # NOTICE that the empty line is just the return.

    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(CSV_FILE_NAME)
    with file.open('w') as f:
        f.write(csv_text)
    return file

# Complementary JSON files fixtures

@pytest.fixture(scope='function', name='json_none')
def json_complement_file_none_existant(tmpdir_factory):
    """ Create just the path of the complement file """
    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(JSON_COMPLEMENT_FILE)
    # run with -s --setup-show  to see this
    # print("file:{}".format(str(file)))
    return file

@pytest.fixture(scope='function', name='json_empty')
def json_complement_file_withou_books(tmpdir_factory):
    """ Create just the path of the complement file """
    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(JSON_COMPLEMENT_FILE)
    # run with -s --setup-show  to see this
    # print("file:{}".format(str(file)))
    to_dump = {"books": list()}
    with open(file, "w") as f:
        json.dump(to_dump, f, indent=4)
    return file

@pytest.fixture(scope='function', name='complemetary_data_modified')
def json_complement_file_with_custom_data(tmpdir_factory):
    """ Fixture to create a complementary file with custom data. """
    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(JSON_COMPLEMENT_FILE)
    book = {
        "id": "57343730",
        "title": "A new title",
        "language": "JP",
        "tags": "ai,be",
        "format": "flimsybook",
        "my_review_url": "/a_review/",
        "read_dates": [
                "2020/10/20",
                "2021/05/06"
            ]
    }
    to_dump = {"books": [book]}
    with open(file, "w") as f:
        json.dump(to_dump, f, indent=4)
    return file

@pytest.fixture(scope='function', name='complemetary_data_with_missing_fields')
def json_complement_file_with_missing_data(tmpdir_factory):
    """ Fixture to create a complementary file with missing data (review and read date). """
    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(JSON_COMPLEMENT_FILE)
    book = {
        "id": "57343730",
        "title": "A new title",
        "language": "JP",
        "tags": "ai,be",
        "format": "flimsybook",
        "my_review_url": None,
        "read_dates": None
    }
    to_dump = {"books": [book]}
    with open(file, "w") as f:
        json.dump(to_dump, f, indent=4)
    return file

# Results path fixtures.

@pytest.fixture(scope='function')
def results_path(tmpdir_factory):
    """ Create just the path of the complement file """
    folder = tmpdir_factory.mktemp(RESULTS_PATH)
    # run with -s --setup-show  to see this
    return folder
