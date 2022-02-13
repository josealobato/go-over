import imp
import logging
from typing import Dict, List

from go_over.goodreads.generator import Generator

from .loader import Loader
from .printer import OnDirectoryPrinter
from .bookshelf import Bookshelf
from .bookshelfComplement import BookshelfComplement

def process(args: Dict, options: Dict):

    if options["verbose"]:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    logger = logging.getLogger(__name__)
    
    # Load.
    logger.info("\n * Load source CVS:")
    loader = Loader(args.gr_csv_path)
    bookshelf = Bookshelf.build_from_loader(loader)
    
    # Load complementary data and update it if needed with the existing shelf.
    # Note that if complementray data file is not there, it will be created.
    # Existing information on the complementary data wont be overriden.
    logger.info("\n * Load and update complementary json:")
    complement_loader = Loader(args.complement_json_path)
    bookshelf_complement = BookshelfComplement(complement_loader)
    bookshelf_complement.update_from_shelf(bookshelf)

    # Update Shell with complementary data.
    # Now with the complete complementary data update the shelf.
    # This will apply all changes that the user made to the complementary data.
    logger.info("\n * Update shelf with complementary data.")
    bookshelf.update_with_complementary_information(
        bookshelf_complement.complementary_information_list
    )

    # Print out all the wanted results from the new shelf.
    logger.info("\n * Print out resulting files:")
    printer = OnDirectoryPrinter(args.results_path)
    generator = Generator(bookshelf, printer)
    generator.execute()

    logger.info("\n * Done!")
