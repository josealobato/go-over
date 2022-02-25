from typing import Dict
import pytest
import json
import os

def load_result(file_name: str, results_path: str) -> Dict:
    """ Load the resulting file with a given name """
    file_path = os.path.join(results_path, file_name)
    with open(file_path, 'r') as f:
        result_dictionary = json.load(f)
    return result_dictionary