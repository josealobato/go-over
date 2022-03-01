""" 
Bookshelf Module
A book shelf represent a collection of books.
It offers action that could be performed on such collection.
"""
import itertools

from datetime import datetime
from typing import Dict, List
import logging

# from .bookread import BookRead
from .book import Book, BookRead
from .loader import Loader

# pylint: disable=C0301
# line too long

class Bookshelf:
    """ A collection of books. """

    def __init__(self) -> None:
        self.books = []

    @property
    def sorted_books(self) -> List['Book']:
        """ Return the books sorted by date."""
        return sorted(self.books, reverse=True,
                    key=lambda b: b.date_read if b.date_read is not None else datetime.min)

    @property
    def all_reads(self) -> List['BookRead']:
        """ Get a list of all reads """
        all_reads = [b.reads() for b in self.books]
        # flatten the list
        return list(itertools.chain(*all_reads))

    @property
    def tags(self) -> List:
        """ Getting a list of the existing tags """
        tags_collection = []
        for book in self.books:
            for tag in book.tags:
                if tag not in tags_collection:
                    tags_collection.append(tag)
        return tags_collection

    @property
    def books_by_tags(self) -> Dict:
        """ Create a dictionary that will hold and entry for very tag with an array of books """
        tags_collection = {}
        for book in self.books:
            if not book.read:
                continue
            for tag in book.tags:
                tags_collection.setdefault(tag, [])
                tags_collection[tag].append(book.dictionary)
        return tags_collection

    @property
    def years_with_books(self) -> List[int]:
        """ Get the list of years that has books """
        years = set()
        for book in self.books:
            if book.date_read:
                years.add(book.date_read.year)
        return list(years)

    @property
    def statistics(self) -> Dict:
        """ Dictionary with the bookshelf statistics """
        stats = {}
        years = self.years_with_books
        for year in years:
            stats[str(year)] = self.statistics_for_year(year)
        return stats

    def reads_on_year(self, year: int) -> List[BookRead]:
        """ Return the list of reads ordered by year in invers order. """
        reads = [read for read in self.all_reads if read.date.year == year]
        return sorted(reads, reverse=True, key=lambda b: b.date)

    def read_on_unkown_date(self) -> List[Book]:
        """ Read books but with unknonw date """
        books = [book for book in self.books if book.read_in_unknown_date]
        return books

    def reading_books(self) -> List[Book]:
        """ Getting the list of currently reading books """
        books = [book for book in self.books if book.currently_reading]
        return books

    def favourites(self) -> List[Book]:
        """ Get the books marked as favourites """
        books = [book for book in self.books if book.is_favourite]
        return books

    def to_read(self) -> List[Book]:
        """ Get the books marked as to read sorted by position """
        books = [book for book in self.books if book.is_to_read]
        return sorted(books, key=lambda x: x.to_read_position)
    
    def statistics_for_year(self, year: int) -> Dict:
        """ Getting the statistics for a year """
        stats = { "read": 0 }
        languages = {}
        book_that_year = [b for b in self.books if b.read_on_year(year)]
        stats["read"] = len(book_that_year)
        for book in book_that_year:
            # Language
            language = book.language
            if language:
                languages.setdefault(language, 0)
                languages[language] += 1
        stats["languages"] = languages
        return stats

    @classmethod
    def build_from_loader(cls, loader: Loader) -> 'Bookshelf':
        """ load content from the give"""
        log = logging.getLogger(__name__)
        log.info(f"Loading goodreads csv data from file: {loader.source_path}")
        shelf = Bookshelf()
        loaded_data = loader.load()
        for dictionary in loaded_data:
            book = Book.build_from_dictionary(dictionary)
            shelf.books.append(book)
        log.info(f"A total of {len(shelf.books)} loaded.")
        log.info("Goodreads csv data loaded.")
        return shelf

    def update_with_complementary_information(self, books_complementary_data: List) -> None:
        """  Getting the complementary data it will update the bookshelf with the new data. """
        # books_comp_data = complementary_data["books"]
        for book in self.books:
            # More  info:
            # https://vald-phoenix.github.io/pylint-errors/plerr/errors/variables/W0640.html
            # pylint: disable=W0640
            equal_ids = lambda b: b["id"] == book.identifier
            comp_data = list(filter(equal_ids, books_complementary_data))
            if comp_data:
                book.update_with_complentary_data_dictionary(comp_data[0])
