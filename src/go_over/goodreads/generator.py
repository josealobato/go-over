import logging
from datetime import date

from .bookshelf import Bookshelf
from .printer import OnDirectoryPrinter

READING_OUT_FILE_NAME = "books_reading"
READ_OUT_FILE_NAME_PREFIX = "books_read_"
READ_OUT_NO_DATE_FILE_NAME = "books_read_no_date"
BOOKS_BY_TAGS_FILE_NAME = "books_by_tags"
STATS_FILE_NAME = "books_stats"
FAVOURITES_FILE_NAME = "books_favourites"
TO_READ_FILE_NAME = "books_to_read"

class Generator:
    """ 
    The generato is in charge of writing the resulting files.
    It needs the shelf (`Bookshelf`) and a printer with a fix path (`OnDirectoryPrinter`).
    """

    def __init__(self, bookshelf: Bookshelf, printer: OnDirectoryPrinter) -> None:
        self.__printer = printer
        self.__shelf = bookshelf
        self.__logger = logging.getLogger(__name__)

    def __generate_reading_books(self):
        """ Generate the currently reading books. """
        self.__logger.info('Generating reading books.')
        reading_books = [b.dictionary for b in self.__shelf.reading_books()]
        books_dict = { 'books': reading_books }
        self.__printer.dump(books_dict, READING_OUT_FILE_NAME)

    def __generate_read_books(self):
        """ Generate a file for every year with the read books that year. """
        current_year = date.today().year
        for year in range(2022, 2000, -1):
            books_this_year = [b.exportable_dictionary for b in self.__shelf.reads_on_year(year)]
            if len(books_this_year) > 0:
                stats = self.__shelf.statistics_for_year(year)
                self.__logger.info(f'Generate for year {year}. A total of {len(books_this_year)} books')
                books_dict = { 'stats': stats, 'books': books_this_year }
                self.__printer.dump(books_dict, READ_OUT_FILE_NAME_PREFIX + str(year))

    def __generate_no_date_books(self):
        """ Generate a file with the no date books. """
        read_books_without_date = [b.dictionary for b in self.__shelf.read_on_unkown_date()]
        self.__logger.info(f'Generate for books without read date: {len(read_books_without_date)} books')
        books_dict = { 'books': read_books_without_date }
        self.__printer.dump(books_dict, READ_OUT_NO_DATE_FILE_NAME)

    def __generate_books_by_tags(self):
        """ Generate a file with separated by tags. """
        books_by_tag = self.__shelf.books_by_tags
        self.__logger.info(f'Generate for books by tag, for tags: {", ".join(self.__shelf.tags)}')
        books_dict = { 'books': books_by_tag }
        self.__printer.dump(books_dict, BOOKS_BY_TAGS_FILE_NAME)

    def __generate_stats(self):
        """ Generate a file with the genenal statistics. """
        stats = self.__shelf.statistics
        self.__printer.dump(stats, STATS_FILE_NAME)

    def __generate_favourites(self):
        """ Generate the list of favourite books. """
        if self.__shelf.favourites():
            books = [b.dictionary for b in self.__shelf.favourites()]
            books_dict = { 'books': books }
            self.__printer.dump(books_dict, FAVOURITES_FILE_NAME)

    def __generate_to_read(self):
        """ Generate the to read book list. """
        if self.__shelf.to_read():
            books = [b.dictionary for b in self.__shelf.to_read()]
            books_dict = { 'books': books }
            self.__printer.dump(books_dict, TO_READ_FILE_NAME)
    
    def execute(self) -> None:
        """ Execute all exporting """
        self.__generate_reading_books()
        self.__generate_read_books()
        self.__generate_no_date_books()
        self.__generate_books_by_tags()
        self.__generate_stats()
        self.__generate_favourites()
        self.__generate_to_read()
        self.__logger.info(f"Generation done! You will find the resulting files at: \n'{self.__printer.printer_path}'")