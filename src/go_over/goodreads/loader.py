import os
import json
import csv
from typing import Dict, List
from .printer import Printer
import logging

class Loader:
    """ 
    Utility to load abstract the load from disk. 
    It is able to load CSV (resulting in a `List`) or JSON (resulting in a `Dict`).
    It will detect them by their extension.
    It also offers a printer to write on the originaly loaded file.
    """

    def __init__(self, target_path: str) -> None:
        """ Build a loader for a file with a given FULL path """
        self.__target_path = target_path
        self.__logger = logging.getLogger(__name__)

    @property
    def source_exist(self) -> bool:
        return os.path.exists(self.__target_path)

    @property
    def source_path(self) -> str:
        return self.__target_path

    def printer(self) -> 'Printer':
        return Printer(self.__target_path)

    def load(self):
        """ Load the content of the file pointed by the loader. 
            Warning: This method can return a list or a dictionary."""
        extension = os.path.splitext(self.__target_path)[-1]
        if extension == '.json':
            return self.__load_dictionary()
        elif extension == '.csv':
            return self.__load_array()
        else:
            raise Exception(f"Unknown extension: {extension}")

    def __load_dictionary(self) -> Dict: 
        """ Load the content of the loader target path as a dictionary. """
        self.__logger.info(f"Load file at path: {self.__target_path}")
        with open(self.__target_path, "r", encoding="utf-8") as json_file:
            json_content = json.load(json_file)
            return json_content

    def __load_array(self) -> List:
        """ Use to load from a CVS """
        self.__logger.info(f"Load file at path: {self.__target_path}")
        entries = []
        with open(self.__target_path, "r", encoding="utf-8") as cvs_file:
            file_reader = csv.DictReader(cvs_file)
            for line in file_reader:
                entries.append(line)
            return entries
