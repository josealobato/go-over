# GOODREADS Method and Parser 
import argparse
from .goodreads import processor

DEFAULT_GR_CVS_FILE_PATH = "goodreads_library_export.csv"
DEFAULT_GR_JSON_COMPLEMENT_FILE_PATH = "books_complement.json"
DEFAULT_GR_RESULTS_PATH = "./results"

# Action when the Goodreads parser is selected
def gr_processor(args, options):
    processor.process(args.gr_csv_path, args.complement_json_path, args.results_path, options)

# Create Parser for Good Reads processing
GR_DESCRIPTION = """
This script convert the goodreads csv to a nicer format for jekyll reading.

It takes the `cvs` generated from GoodReads (My Books > Import Export) and 
another JSON file with complementary data, and generates JSON files prepared 
to be read with Liquid and displayed on the Jekyll blog.

The outpu JSON files are:
* reading.
* one for every year.
* one with books with no date.

The idea is that those JSON files cound be maintained by hand if GoodReads stops working.

NOTES on the complementary file.
* It contains fields that are missing on GR. 
* It matches with the GR data using the GR book Id.
* If this file is not there it will be generated from the existing books. You will need to fill it
  and run it again.
* If a new book is added, during processing this file will be updated. You will need to add
  the information and run it again.
"""
def setup_gr_parser(subparsers):
    parser_gr = subparsers.add_parser("goodreads", 
        aliases=['gr'],
        help="Process a Goodreads CSV (see help).",
        description=GR_DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser_gr.add_argument("-g", "--gr_csv_path", 
        default=DEFAULT_GR_CVS_FILE_PATH,
        help="CVS exported from goodreads.")
    parser_gr.add_argument("-c", "--complement_json_path", 
        default=DEFAULT_GR_JSON_COMPLEMENT_FILE_PATH,
        help="JSON file with data to complement goodreads data.")
    parser_gr.add_argument("-r", "--results_path",
        default=DEFAULT_GR_RESULTS_PATH,
        help="Path were the output will be written.")
    parser_gr.add_argument("-f", "--force_complementary_rewrite", 
        action="store_true", 
        help="Force the rewrite of the complementary file (no data loss).")
    parser_gr.set_defaults(func=gr_processor) # Important: this is the function to call if the parser is selected.
