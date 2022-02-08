import imp
from typing import Dict, List
from ..tools.logger import Logger
from .printer import FilePrinter

def process(args: Dict, options: Dict):
    print("goodreads processor")
    logger = Logger(options["verbose"])
    print(args)
    print(options)

    target = args.results_path
    printer = FilePrinter(target, logger)
    printer.dump({'Jupiter': None, 'Venus': None, 'Earth': None}, "planets")

