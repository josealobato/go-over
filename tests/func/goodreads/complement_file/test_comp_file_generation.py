from typing import Dict
import pytest

from ...func_test_tools import load_result, load_result_from_path

# Under test
from go_over.goodreads.processor import process

# Test

def test_comp_file_generation_when_it_is_not_there(csv_one_book, json_none, results_path):
    """ Generate the complementary file from the original data if it is not there """
    # GIVEN the original data and not conplementary data.
    # WHEN proccesing the data.
    process(csv_one_book, json_none, results_path, {"verbose": False, "rewrite_complementary_data": False})
    # THEN the file should be generated.
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
    assert book["read_dates"] == ['2022/02/17']
    assert book["is_favourite"] == False