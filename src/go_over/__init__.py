from .hello_dad import heyo
import argparse

DESCRIPTION = "What!!"

parser = argparse.ArgumentParser(description=DESCRIPTION,
    formatter_class=argparse.RawDescriptionHelpFormatter)

subparsers = parser.add_subparsers(dest="command", help = "jal subcomamnd help")

# Global artument options
parser.add_argument("-v", "--verbose", action="store_true")

# GOODREADS Method and Parser 

DEFAULT_GR_CVS_FILE_PATH = "goodreads_library_export.csv"
DEFAULT_GR_JSON_COMPLEMENT_FILE_PATH = "books_complement.json"

# Action when the Goodreads parser is selected
def gr_processor(args, options):
    print("gr processor")
    print(args)

# Create Parser for Good Reads processing
parser_gr = subparsers.add_parser("goodreads", 
    help="jal goodreads help")
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
        print(parser.parse_args(['-h']))
