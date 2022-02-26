from typing import Dict
import pytest

from ..func_test_tools import load_result

# Under test
from go_over.goodreads.processor import process

# Tests

def test_process_one_book_stats(csv_one_book, json_empty, results_path):
    """ Process and generate data for one book and test the stats. """
    # GIVEN a CVS file with just one book and empty complement file.
    source_file = csv_one_book
    complement_file = json_empty
    results_folder = results_path
    # WHEN we process that file.
    process(source_file, complement_file, results_folder, {"verbose": True})
    # THEN the stats should be attached to the results 
    results = load_result("books_read_2022.json", results_folder)
    stats = results['stats']
    assert stats["read"] == 1
    assert len(stats["languages"]) == 1
    assert stats["languages"]['EN'] == 1
