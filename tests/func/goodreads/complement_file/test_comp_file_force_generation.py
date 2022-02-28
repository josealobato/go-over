from typing import Dict
import pytest

from ...func_test_tools import load_result, load_result_from_path

# Under test
from go_over.goodreads.processor import process

# Test

def test_force_generate_without_initial_complementary_data(csv_one_book, json_none, results_path):
    """ Force generate the file when the complementary file is not there does not change regular reneration of complementary file """
    # GIVEN a source CVS data and not complementary file (on fixtures).
    # WHEN process the data forcing the regeneration of the complementary file.
    process(csv_one_book, json_none, results_path, {"verbose": False, "rewrite_complementary_data": True})
    # THEN the resulting complement file is the same as the one wihtout force generation.
    results = load_result_from_path(json_none)
    books = results["books"]
    assert len(books) == 1
    book = books[0]
    assert len(book) == 8
    assert book["id"] == "57343730"
    assert book["title"] == "Super Learning: Advanced Strategies for Quicker Comprehension, Greater Retention, and Systematic Expertise"
    assert book["language"] == "EN"
    assert book["tags"] == "nonfiction"
    assert book["format"] == "audiobook"
    assert book["my_review_url"] == None
    assert book["read_dates"] == [
                "2022/02/17"
            ] # Notice it contains the read date that comes with the book.
    assert book["is_favourite"] == False

def test_force_generation_with_initial_complementary_data(csv_one_book, complemetary_data_modified, results_path):
    """ Force generate when there was a complementary file that modify the original data 
        will leave the modify data the same. Except for the read that will be complemented. """
    # GIVEN a source CSV data and a complementary file that modify all data.
    # WHEN process the data forcing the generation of the complementary data.
    process(csv_one_book, complemetary_data_modified, results_path, {"verbose": False, "rewrite_complementary_data": True})
    # THEN the resulting complement file is the same as the one wihtout force generation exept for the date.
    results = load_result_from_path(complemetary_data_modified)
    books = results["books"]
    assert len(books) == 1
    book = books[0]
    assert len(book) == 8
    assert book["id"] == "57343730"
    assert book["title"] == "A new title"
    assert book["language"] == "JP"
    assert book["tags"] == "ai,be"
    assert book["format"] == "flimsybook"
    assert book["my_review_url"] == "/a_review/"
    assert "2022/02/17" in book["read_dates"] 
    assert "2020/10/20" in book["read_dates"] 
    assert "2021/05/06" in book["read_dates"]  
    assert book["is_favourite"] == False

def test_force_generation_with_initial_complementary_data_missing_fields(csv_one_book, complemetary_data_with_missing_fields, results_path):
    """ Force generate when there was a complementary with missing fiels will complement those fields if they exist on the original data. """
    # GIVEN a source CSV data and a complementary file that modify all data.
    # WHEN process the data forcing the generation of the complementary data.
    process(csv_one_book, complemetary_data_with_missing_fields, results_path, {"verbose": False, "rewrite_complementary_data": True})
    # THEN the resulting complement will be updated with the data from the source file (data)
    results = load_result_from_path(complemetary_data_with_missing_fields)
    books = results["books"]
    assert len(books) == 1
    book = books[0]
    assert len(book) == 8
    assert book["id"] == "57343730"
    assert book["title"] == "A new title"
    assert book["language"] == "JP"
    assert book["tags"] == "ai,be"
    assert book["format"] == "flimsybook"
    assert book["my_review_url"] == None
    assert book["read_dates"] == [
                "2022/02/17"
            ]
    assert book["is_favourite"] == False
    
def test_force_generation_with_initial_complementary_data_missing_fields_of_unread_book(csv_one_unread_book, complemetary_data_with_missing_fields, results_path):
    """ Force generate an unread book and there is not date on either the original nor the complementary  """
    # GIVEN a source CSV data and a complementary file withou read date.
    # WHEN process the data forcing the generation of the complementary data.
    process(csv_one_unread_book, complemetary_data_with_missing_fields, results_path, {"verbose": False, "rewrite_complementary_data": True})
    # THEN the resulting complement data file wont have date either.
    results = load_result_from_path(complemetary_data_with_missing_fields)
    books = results["books"]
    assert len(books) == 1
    book = books[0]
    assert len(book) == 8
    assert book["id"] == "57343730"
    assert book["read_dates"] == None
    assert book["is_favourite"] == False

def test_result_when_force_generation_with_initial_complementary_data(csv_one_book, complemetary_data_modified, results_path):
    """ Force generate wont affect the result data.. """
    # GIVEN a source CSV data and a complementary file that modify all data.
    # WHEN process the data forcing the generation of the complementary data.
    process(csv_one_book, complemetary_data_modified, results_path, {"verbose": False, "rewrite_complementary_data": True})
    # THEN the result files uses the complementary data title as usual.
    results = load_result("books_read_2022.json", results_path)
    book = results['books'][0]
    assert book["title"] == "A new title"
    assert book["language"] == "JP"
    assert book["tags"] == ["ai","be"]
    assert book["format"] == "flimsybook"
    assert book["my_review_url"] == "/a_review/"
    # Data is not tested because it involve several files (see test_comp_file_modification_dates.py)
    assert book["is_favourite"] == False