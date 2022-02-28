import logging
from typing import Dict, List

from go_over.goodreads.generator import Generator

from .loader import Loader
from .printer import OnDirectoryPrinter
from .bookshelf import Bookshelf
from .bookshelfComplement import BookshelfComplement

def process(gr_csv_path: str, complement_json_path: str, results_path: str, options: Dict): 

    options.setdefault("verbose", False)
    if options["verbose"]:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    logger = logging.getLogger(__name__)
    
    # Load.
    logger.info("\n * Load source CVS:")
    loader = Loader(gr_csv_path)
    bookshelf = Bookshelf.build_from_loader(loader)
    
    # Load complementary data and update it if needed with the existing shelf.
    # Note that if complementray data file is not there, it will be created.
    # Existing information on the complementary data wont be overriden.
    logger.info("\n * Load and update complementary json:")
    complement_loader = Loader(complement_json_path)
    bookshelf_complement = BookshelfComplement(complement_loader)
    bookshelf_complement.update_from_shelf_if_needed(bookshelf)

    # Update Shell with complementary data.
    # Now with the complete complementary data update the shelf.
    # This will apply all changes that the user made to the complementary data.
    logger.info("\n * Update shelf with complementary data.")
    bookshelf.update_with_complementary_information(
        bookshelf_complement.complementary_information_list
    )

    # If requested force the regeneration of the complementary data with the
    # shelf. Notice that that new complementary data will update the non existing 
    # complementary data parts with the information from the books.
    options.setdefault("rewrite_complementary_data", False)
    if options["rewrite_complementary_data"]:
        logger.info("\n * Force write the complementary data.")
        bookshelf_complement.update_from_shelf(bookshelf)

    # Print out all the wanted results from the new shelf.
    logger.info("\n * Print out resulting files:")
    printer = OnDirectoryPrinter(results_path)
    generator = Generator(bookshelf, printer)
    generator.execute()

    logger.info("\n * Done!")
