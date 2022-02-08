import os
import json
from typing import Dict, List
from ..tools.logger import Logger

class FilePrinter:

    def __init__(self, target_folder: str, logger: Logger) -> None:
        self.target_folder = target_folder
        self.logger = logger

    def dump(self, dict: Dict, file_name: str) -> None:
        """ Getting a dictionary and a file name it will create a file in the results folder
        with the content in JSON. """
        file_path = os.path.join(self.target_folder, file_name + '.json')
        self.dump_dictionary_in_path(dict, file_path)

    def create_folder_if_needed(self):
        """ Create the target folder if needed. """
        if not os.path.exists("./" + self.target_folder):
            os.mkdir("./" + self.target_folder)

    def dump_dictionary_in_path(self, full_dictionary: Dict, file_path: str) -> None:
        """ Getting a dictionary and a file path will create a file in the given path
            with the conten of the file in JSON. """
        self.create_folder_if_needed()
        with open(file_path, 'w', encoding="utf-8") as json_file:
            json.dump(full_dictionary, json_file, indent=4)
        # print(f'[info] file write at: {file_path}')
        self.logger.info(f'[info] file write at: {file_path}')
