# Resume from JSON application
__author__ = "Matteo Golin"

# Imports
import pdfkit
from templates import MonospaceResume

# Constants
DATA_FILE = "resume.json"


# Main
def main():

    # Make resume
    resume = MonospaceResume(DATA_FILE)
    resume.save_as()


if __name__ == '__main__':
    main()
