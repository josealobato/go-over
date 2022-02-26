from typing import Dict
import json
import pytest

from ...func_test_tools import load_result, load_result_from_path
from ...constants import *

# Under test
from go_over.goodreads.processor import process

# Fixtures

@pytest.fixture(scope='function', name='complemetary_data_modified')
def json_complement_file_with_custom_data(tmpdir_factory):
    """ Create a complementary file with custom data """
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

# Test

def test_comp_file_modification_effect_on_title(csv_one_book, complemetary_data_modified, results_path):
    """ The output use the title in the complementary file  """
    # GIVEN a soucedata and a complementary file that differ on the title.
    # WHEN we process the data.
    process(csv_one_book, complemetary_data_modified, results_path, {"verbose": False})
    # THEN the result files uses the complementary data title.
    results = load_result("books_read_2022.json", results_path)
    book = results['books'][0]
    assert book["title"] == "A new title"

def test_comp_file_modification_effect_on_language(csv_one_book, complemetary_data_modified, results_path):
    """ The output use the language in the complementary file  """
    # GIVEN a soucedata and a complementary file that differ on the language.
    # WHEN we process the data.
    process(csv_one_book, complemetary_data_modified, results_path, {"verbose": False})
    # THEN the result files uses the complementary data language.
    results = load_result("books_read_2022.json", results_path)
    book = results['books'][0]
    assert book["language"] == "JP"

def test_comp_file_modification_effect_on_tags(csv_one_book, complemetary_data_modified, results_path):
    """ The output use the tags in the complementary file  """
    # GIVEN a soucedata and a complementary file that differ on the tags.
    # WHEN we process the data.
    process(csv_one_book, complemetary_data_modified, results_path, {"verbose": False})
    # THEN the result files uses the complementary data tags.
    results = load_result("books_read_2022.json", results_path)
    book = results['books'][0]
    assert book["tags"] == ["ai","be"]

def test_comp_file_modification_effect_on_format(csv_one_book, complemetary_data_modified, results_path):
    """ The output use the format in the complementary file  """
    # GIVEN a soucedata and a complementary file that differ on the format.
    # WHEN we process the data.
    process(csv_one_book, complemetary_data_modified, results_path, {"verbose": False})
    # THEN the result files uses the complementary data format.
    results = load_result("books_read_2022.json", results_path)
    book = results['books'][0]
    assert book["format"] == "flimsybook"

def test_comp_file_modification_effect_on_review(csv_one_book, complemetary_data_modified, results_path):
    """ The output use the review in the complementary file  """
    # GIVEN a soucedata and a complementary file that differ on the review.
    # WHEN we process the data.
    process(csv_one_book, complemetary_data_modified, results_path, {"verbose": False})
    # THEN the result files uses the complementary data review.
    results = load_result("books_read_2022.json", results_path)
    book = results['books'][0]
    assert book["my_review_url"] == "/a_review/"
    