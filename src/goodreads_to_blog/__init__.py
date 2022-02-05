from .hello_dad import heyo
import argparse

DESCRIPTION = "What!!"

parser = argparse.ArgumentParser(description=DESCRIPTION,
    formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("gr_csv_path", help="Export csv from good reads.")
parser.add_argument("complement_json_path", default="books_complement.json",
    help="JSON file with data to complement goodreads data.")
args = parser.parse_args()

# The methods here have to be defined as entry points and will be called when
# called direclty
def hello_world2():
    print(args.gr_csv_path)
    print("what!")
    print("Hello world2")
    heyo()
