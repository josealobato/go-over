import os
import json
from typing import Dict, List
import logging

_FILE_EXTENSION = ".json"

class Printer:
    """ Printer for a concrete file.
        It needs the full path of a file to print on."""

    def __init__(self, target_path: str) -> None:
        """ Build a printer with the full path (path + filename + extension)."""
        self.__target_path = target_path
        self.__logger = logging.getLogger(__name__)

    @classmethod
    def in_current_directory(cls, file_name: str) -> 'Printer':
        """ Return a printer to print on a given filename within the current folder."""
        current_path = os.getcwd()
        full_path = os.path.join(current_path, file_name + _FILE_EXTENSION)
        return cls(full_path)

    @classmethod
    def in_directory(cls, directory_path: str, file_name: str) -> 'Printer':
        """ Returns a printer to print in a given directory with a given file name."""
        full_path = os.path.join(directory_path, file_name + _FILE_EXTENSION)
        return cls(full_path)

    @property
    def target_path_exist(self) -> bool:
        return os.path.exists(self.__target_path)

    def _create_folder_if_needed(self):
        """ Create the target folder if needed. """
        dir_name = os.path.dirname(self.__target_path)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    def dump(self, dict: Dict) -> None:
        """ Getting a dictionary and a file name it will create a file in given path 
        with the content in JSON. """
        self.__logger.info(f"Write file at: {self.__target_path}")
        self._create_folder_if_needed()
        with open(self.__target_path, 'w', encoding="utf-8") as json_file:
            json.dump(dict, json_file, indent=4)

class OnDirectoryPrinter:
    """ Printer for files in a directory
        It needs the full path of a directory to print files on."""

    def __init__(self, directory_path: str="./") -> None:
        """ Build a printer with the full directory path. If no path is given it assumes the current directory. """
        self.__directory_path = directory_path
        self.__logger = logging.getLogger(__name__)

    @property
    def directory_path_exist(self) -> bool:
        return os.path.exists(self.__directory_path)

    @property
    def printer_path(self) -> str:
        return self.__directory_path

    def _create_directory_if_needed(self):
        """ Create the target folder if needed. """
        dir_name = os.path.abspath(self.__directory_path)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

    def dump(self, dict: Dict, file_name: str) -> None:
        """ Getting a dictionary and a file name it will create a file in given path 
        with the content in JSON. """
        full_path = os.path.join(self.__directory_path, file_name + _FILE_EXTENSION)
        self.__logger.info(f"Write file at: {full_path}")
        self._create_directory_if_needed()
        with open(full_path, 'w', encoding="utf-8") as json_file:
            json.dump(dict, json_file, indent=4)