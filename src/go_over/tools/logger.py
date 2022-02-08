

class Logger:

    def __init__(self, verbose: bool):
        self.verbose = verbose
    
    def error(self, msg):
        print("Error: " + msg)

    def warning(self, msg):
        if self.verbose:
            print("Warning: " + msg)
    
    def info(self, msg):
        if self.verbose:
            print("Info: " + msg)