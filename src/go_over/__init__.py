from .example_module import heyo
import argparse
from . import __setup_gr

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

# Configure subparers.
# Every new parsert represents a different subtool. It will have its
# configuration in a module in at `go_over` lever. 
__setup_gr.setup_gr_parser(subparsers)

# Function to build the global options to be intected in all tools.
def _build_options(args):
    options = { 
        "verbose": args.verbose
    }
    # Some paramenters are not always there (depend on the tool) so, 
    # they need to be checked.
    args_dictionary = vars(args)
    if "force_complementary_rewrite" in args_dictionary:
        options["rewrite_complementary_data"] = args.force_complementary_rewrite
    
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
