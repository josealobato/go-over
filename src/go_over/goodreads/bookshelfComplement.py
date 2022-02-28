from typing import Dict, List
from .bookshelf import Bookshelf
from .loader import Loader
from .printer import Printer
import logging

class BookshelfComplement:
    """ The bookshelf complement manages the complementary data of the bookshelf.
        This is data that comes from other sources (manually created) instead of Goodreads,
        to complement its information."""

    def __init__(self, loader: Loader) -> None:
        self.__data_dictionary = None
        self.logger = logging.getLogger(__name__)
        self.loader = loader
        self.printer = self.loader.printer()

    @property
    def complementary_information_list(self) -> List:
        """ Getting a list of the complementary information for books. """
        return self.__data_dictionary['books']

    def update_from_shelf(self, shelf: 'Bookshelf') -> None:
        """ With the object create with the minimum data (the source path) it will load it,
            update it from the existing shelf and prepare it for its use. Finally it will update
            the source complementary file with the available data."""
        self.__generate_template_if_needed(shelf)
        self.__load()
        self.__update_source_from_bookshelf(shelf)

    def __update_source_from_bookshelf(self, shelf: 'Bookshelf') -> None:
        """ Will update the source file with The books on the shelf. """
        data_dictionary = {"books": []}
        for book in shelf.books:
            data_dictionary['books'].append(book.complementary_data_dictionary)
        self.printer.dump(data_dictionary)

    def update_from_shelf_if_needed(self, shelf: 'Bookshelf') -> None:
        """ With the object create with the minimum data (the source path) it will load it
            update it from the existing shelf and prepare it for its use. Finally it will update
            the source complementary file with the available data for new books only."""
        self.__generate_template_if_needed(shelf)
        self.__load()
        self.__update_source_from_bookshelf_if_needed(shelf)

    def __update_source_from_bookshelf_if_needed(self, shelf: 'Bookshelf') -> None:
        """ Will update the source file with new books if any. """
        is_dirty = False
        all_complementary_data_ids = [c["id"] for c in self.complementary_information_list]
        books_not_in_complementary = [b for b in shelf.books
                                    if b.identifier not in all_complementary_data_ids]
        if books_not_in_complementary:
            is_dirty = True
        for book in books_not_in_complementary:
            self.__data_dictionary['books'].append(book.complementary_data_dictionary)
            self.logger.info(f'Append new book to complementary data with id {book.identifier}')

        if is_dirty:
            self.printer.dump(self.__data_dictionary)

    def __load(self) -> None:
        """ It will load the JSON file into an ivar """
        self.__data_dictionary = self.loader.load()

    def __generate_template_if_needed(self, shelf: 'Bookshelf') -> None:
        """ If the complement data file does not exist it will generate it from the given shelf.
            It will generate a default entry for every book."""
        if not self.loader.source_exist:
            self.logger.info(f"Generate complementary data file: {self.loader.source_path}")
            books_complementary_data = [b.complementary_data_dictionary for b in shelf.books]
            data_dictionary = { 'books': books_complementary_data }
            self.printer.dump(data_dictionary)