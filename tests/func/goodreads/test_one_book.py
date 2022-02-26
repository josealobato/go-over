from typing import Dict
import pytest

from ..func_test_tools import load_result

# Under test
from go_over.goodreads.processor import process

# Tests

def test_process_one_book(csv_one_book, json_empty, results_path):
    """ Process and generate data for one book. """
    # GIVEN a CVS file with just one book and emtpy complement file.
    source_file = csv_one_book
    complement_file = json_empty
    results_folder = results_path
    # WHEN we process that file.
    process(source_file, complement_file, results_folder, {"verbose": True})
    # THEN All parameters in the book should be loaded
    results = load_result("books_read_2022.json", results_folder)
    books = results['books']
    assert len(books) == 1
    book = books[0]
    assert book["id"] == "57343730"
    assert book["author"] == "Peter Hollins"
    assert book["title"] == "Super Learning: Advanced Strategies for Quicker Comprehension, Greater Retention, and Systematic Expertise"
    assert book["rating"] == 3
    assert book["date"] == "2022-02-17"
    assert book["tags"] == ["nonfiction"]
    assert book["format"] == "audiobook"
    assert book["goodreads_url"] == "https://www.goodreads.com/book/show/57343730"
    assert book["language"] == "EN"
    assert book["my_review_url"] == None
    assert book["read_number"] == "1"

def test_process_one_book_and_return(csv_one_book_plus_empty_line, json_empty, results_path):
   """ Process and generate data for one book. """
   # GIVEN a CVS file with just one book, AN EMPTY LINE at the end, and emtpy complement file.
   source_file = csv_one_book_plus_empty_line
   complement_file = json_empty
   results_folder = results_path
   # WHEN we process that file.
   process(source_file, complement_file, results_folder, {"verbose": True})
   # THEN All parameters in the book should be loaded
   results = load_result("books_read_2022.json", results_folder)
   books = results['books']
   assert len(books) == 1
