from typing import Dict
import pytest

from .func_test_tools import load_result

# Under test
from go_over.goodreads.processor import process

# Tests
@pytest.mark.skip("Scaffold test")
def test_not_having_complement_json_file(csv_one_book, json_empty, results_path):
    """ Processing when there is not json file. """
    pass