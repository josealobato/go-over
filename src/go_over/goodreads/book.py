""" 
    Book Module 
    Notice that it contains the BookRead class as well.
    That was done to avoid circular imports. They both depend on each other.
"""
from datetime import datetime
from typing import Dict, List
import logging
import re

def to_read_position_from_string(string: str) -> int:
    pattern = r"to-read \(\#(\d+)\)"
    matched = re.findall(pattern, string)
    if matched:
        value = matched[0]
        return int(value)
    else:
        return 0

# pylint: disable=R0902
class Book:
    """
    This class represents a book.
    """

    def __init__(self, **kwargs) -> None:
        self.identifier = kwargs['Book Id']
        self.title = kwargs['Title']
        self.author = kwargs['Author']
        self.currently_reading = kwargs["Exclusive Shelf"] == "currently-reading"
        self.read = kwargs["Exclusive Shelf"] == "read"
        date_read = kwargs["Date Read"]
        if date_read == "":
            self.date_read = None
            self.read_dates = []
        else:
            self.date_read = datetime.strptime(date_read, "%Y/%m/%d")
            self.read_dates = [self.date_read]
        self.rating = int(kwargs['My Rating'])
        self.language = "EN"
        self.__tags = "nonfiction"
        self.document_format = "audiobook"
        self.my_review_url = None
        self.is_favourite = False
        self.is_to_read = kwargs["Exclusive Shelf"] == "to-read"
        if "Bookshelves with positions" in kwargs:
            self.to_read_position = to_read_position_from_string(kwargs["Bookshelves with positions"])
        else:
            self.to_read_position = 0

    def __str__(self):
        return f'"{self.title}" by {self.author} read on {self.date_read}'

    @classmethod
    def build_from_dictionary(cls, complementary_data: Dict) -> 'Book':
        """ Build a book from a dictionary of the needed data """
        return cls(**complementary_data)

    def update_with_complentary_data_dictionary(self, complementary_data: Dict) -> None:
        """ Update the book with the data comming from a dictionary with complementary data.
            Notice that the complementary data many miss keys. """
        complementary_data.setdefault("title", self.title)
        self.title = complementary_data["title"]
        
        complementary_data.setdefault("language", self.language)
        self.language = complementary_data["language"]

        complementary_data.setdefault("tags", self.__tags)
        self.__tags = complementary_data["tags"]

        complementary_data.setdefault("format", self.document_format)
        self.document_format = complementary_data["format"]

        complementary_data.setdefault("my_review_url")
        self.my_review_url = complementary_data["my_review_url"]

        complementary_data.setdefault("read_dates", [])
        new_read_dates = complementary_data["read_dates"]
        if new_read_dates:
            if self.read:
                self.add_reads(new_read_dates)
            else:
                print(f"[Warning] trying to add a read date to unread book with id {self.identifier}.")
        
        complementary_data.setdefault("is_favourite", False)
        self.is_favourite = complementary_data["is_favourite"]
        if self.is_favourite:
            logger = logging.getLogger(__name__)
            logger.info(f"- Favourite book: {self.title[:30]}...")

    @property
    def last_read(self) -> datetime:
        """ Return the last time the book was read or None"""
        if not self.read_dates:
            return None
        sorted_dates = sorted(self.read_dates, reverse=True)
        return sorted_dates[0]

    def add_reads(self, new_reads: List) -> None:
        """ Add the new reas with format %Y/%m/%d"""
        new_dates = [datetime.strptime(new_read, "%Y/%m/%d") for new_read in new_reads]
        all_read_dates = set(self.read_dates + new_dates)
        self.read_dates = list(all_read_dates)

    def read_on_year(self, year: int) -> bool:
        """ Tell if the book was read in a given year."""
        reads_on_that_year = [read for read in self.read_dates if read.year == year]
        return len(reads_on_that_year) > 0

    @property
    def read_years(self) -> List[int]:
        """ Get the list of year in which this book was read """
        years = set()
        for date in self.read_dates:
            years.add(date.year)
        return list(years)

    @property
    def read_in_unknown_date(self) -> bool:
        """ Tell is the book was read but do not know when. """
        return self.last_read == None and self.read

    @property
    def tags(self) -> List:
        """ Getting a list of tags. """
        return list(map(str.strip, self.__tags.split(",")))

    @property
    def dictionary(self) -> Dict:
        """ Create a dictionary with the Book ready to export. """
        result = {}
        result['id'] = self.identifier
        result['author'] = self.author
        result['title'] = self.title
        result['rating'] = self.rating
        # Note, this date format is the one preffered by Liquid.
        result['date'] = self.date_read.strftime("%Y-%m-%d") if self.date_read else None
        result['tags'] = self.tags
        result['format'] = self.document_format
        result['goodreads_url'] = "https://www.goodreads.com/book/show/" + self.identifier
        result['language'] = self.language
        result['my_review_url'] = self.my_review_url
        result['is_favourite'] = self.is_favourite
        result['to_read_position'] = self.to_read_position
        return result

    @property
    def complementary_data_dictionary(self) -> Dict:
        """ From a book it created a dictionary with only the complementary data """
        result = {}
        result['id'] = self.identifier
        result['title'] = self.title
        result['language'] = self.language
        result['tags'] = self.__tags
        result['format'] = self.document_format
        result['my_review_url'] = self.my_review_url
        if self.read_dates:
            result['read_dates'] = [d.strftime("%Y/%m/%d") for d in self.read_dates]
        else:
            result['read_dates'] = None 
        result['is_favourite'] = self.is_favourite
            
        return result

    def reads(self) -> List['BookRead']:
        """ Getting the list of current reads of this book """
        reads = []
        sorted_dates = sorted(self.read_dates)
        for i, read_date in enumerate(sorted_dates):
            new_read = BookRead(self, read_date, i + 1)
            reads.append(new_read)
        return reads


class BookRead:
    """
    This class represents the read of a book.
    That means that it contains a single data and the information about 
    the read numbe (it was the first time read, the second, etc).
    """

    def __init__(self, book: Book, read_date: datetime, read_number: int = 1) -> None:
        self.__book = book
        self.__date = read_date
        self.__read_number = read_number

    @property
    def date(self) -> datetime:
        """ Get the read date """
        return self.__date

    @property
    def read_number(self) -> int:
        """ Get the read number """
        return self.__read_number

    @property
    def identifier(self) -> str:
        """ Get the book id """
        return self.__book.identifier

    def __str__(self):
        return f'"Read of {self.__book.title}" by {self.__book.author} read on {self.__date}'

    @property
    def exportable_dictionary(self) -> Dict:
        """ The dictionary"""
        book_dictionary = self.__book.dictionary
        book_dictionary['date'] = self.__date.strftime("%Y-%m-%d")
        book_dictionary['read_number'] = str(self.__read_number)
        return book_dictionary