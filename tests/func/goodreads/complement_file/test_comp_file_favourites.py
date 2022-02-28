from typing import Dict
import json
import pytest

from ...func_test_tools import load_result, load_result_from_path, exist_in_path
from ...constants import *

# Favourites fixtures

@pytest.fixture(scope='function', name='complemetary_data_with_favourite_true')
def json_complement_file_with_favourites_true(tmpdir_factory):
    """ Fixture to create complemtary with favourite equal true. """
    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(JSON_COMPLEMENT_FILE)
    book = {
        "id": "57343730",
        "is_favourite": True
    }
    to_dump = {"books": [book]}
    with open(file, "w") as f:
        json.dump(to_dump, f, indent=4)
    return file

@pytest.fixture(scope='function', name='complemetary_data_with_favourite_false')
def json_complement_file_with_favourites_false(tmpdir_factory):
    """ Fixture to create complemtary with favourite equal false. """
    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(JSON_COMPLEMENT_FILE)
    book = {
        "id": "57343730",
        "is_favourite": False
    }
    to_dump = {"books": [book]}
    with open(file, "w") as f:
        json.dump(to_dump, f, indent=4)
    return file

@pytest.fixture(scope='function', name='complemetary_data_without_favourite')
def json_complement_file_without_favourites(tmpdir_factory):
    """ Fixture to create complemtary without favourite. """
    file = tmpdir_factory.mktemp(SOURCE_DATA_PATH).join(JSON_COMPLEMENT_FILE)
    book = {
        "id": "57343730"
    }
    to_dump = {"books": [book]}
    with open(file, "w") as f:
        json.dump(to_dump, f, indent=4)
    return file

# Under test
from go_over.goodreads.processor import process

def test_no_favourites_generation_when_no_favourite(csv_one_book, complemetary_data_without_favourite, results_path):
    """ When no favourites is given to the configuration file not favourites file is generated. """
    # GIVEN A origina CSV and a complementari file that does not contain favourites.
    # WHEN Genertate
    process(csv_one_book, complemetary_data_without_favourite, results_path, {})
    # THEN no favourites file is generated
    assert not exist_in_path("books_favourites.json", results_path)

def test_no_favourites_generation_when_favourite_false(csv_one_book, complemetary_data_with_favourite_false, results_path):
    """ When favourites is given with false value to the configuration file not favourites file is generated. """
    # GIVEN A origina CSV and a complementari file that does not contain favourites.
    # WHEN Genertate
    process(csv_one_book, complemetary_data_with_favourite_false, results_path, {})
    # THEN no favourites file is generated
    assert not exist_in_path("books_favourites.json", results_path)

def test_favourites_generation(csv_one_book, complemetary_data_with_favourite_true, results_path):
    """ When a favourites is given with true value to the configuration file favourites file is generated. """
    # GIVEN A origina CSV and a complementari file that contains favourites.
    # WHEN Genertate
    process(csv_one_book, complemetary_data_with_favourite_true, results_path, {})
    # THEN favourites file is generated
    assert exist_in_path("books_favourites.json", results_path)

def test_favourites_generation_content(csv_one_book, complemetary_data_with_favourite_true, results_path):
    """ When a favourites is given to the configuration file favourites file is generated. """
    # GIVEN A origina CSV and a complementari file that contains favourites.
    # WHEN Genertate
    process(csv_one_book, complemetary_data_with_favourite_true, results_path, {})
    # THEN favourites file is generated
    results = load_result("books_favourites.json", results_path)
    book = results['books'][0]
    assert book["is_favourite"] == True