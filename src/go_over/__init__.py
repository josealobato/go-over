from .hello_dad import heyo
import argparse

DESCRIPTION = """
The 'go-over' provide a set of tools to process input from different sources,
and generate JSON output that is easy to be process with Liquid in Jekyll.

It was build to help me maintaing my blog at `https://josealobato.com`.
"""

parser = argparse.ArgumentParser(description=DESCRIPTION,
    formatter_class=argparse.RawDescriptionHelpFormatter)

subparsers = parser.add_subparsers(dest="command", help = "Available Commands for go-over.")

# Global artument options
parser.add_argument("-v", "--verbose", action="store_true", help="Print extra information.")

# GOODREADS Method and Parser 

DEFAULT_GR_CVS_FILE_PATH = "goodreads_library_export.csv"
DEFAULT_GR_JSON_COMPLEMENT_FILE_PATH = "books_complement.json"

# Action when the Goodreads parser is selected
def gr_processor(args, options):
    print("gr processor")
    print(args)

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
parser_gr.set_defaults(func=gr_processor) # Important: this is the function to call if the parser is selected.

# Add here any future parser.

# Function to build the global options to be intected in all tools.
def _build_options(args):
    options = { 
        "verbose": args.verbose
    }
    return options

# Script entry point defined in the setup.cfg file.
# It will be called after initializing the script, so 
# when the reset of the code in this file is run.
def cli_processor():

    # Parsing the CLI arguments.
    args = parser.parse_args()
    # Creating the options dictionary to be injected to all tools.
    options = _build_options(args)
    # Check if any command has been used... 
    if args.command:
        # if so, call it (notice that every parser is defined with a method to call).
        args.func(args, options) 
    else:
        # otherwise show the help
        parser.print_help()
