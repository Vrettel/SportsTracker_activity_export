########################################################################################################################
## File name     : spt_export.py
## Date created  : 04/10/2020
## Last update   : 09/10/2020
## Author        : George Vrettos
## Description   : The main class of the program only used for function initiation purposes.
########################################################################################################################

# Imports
import sys
import getopt

from sports_tracker_api import SportsTrackerAPI

class Main:

    def __init__(self, argv):

        token = None
        out_dir = None

        try:
            opts, args = getopt.getopt(argv, "hi:t:o:", ["token=", "out="])
        except getopt.GetoptError:
            print('spt_export.py -t <Sports Tracker token> -o <Output folder>')
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print('Usage: spt_export.py -t <Sports Tracker token> -o <Output folder>')
                sys.exit()
            elif opt in ("-t", "--token"):
                token = arg
            elif opt in ("-o", "--out"):
                out_dir = arg

        if token is not None and out_dir is not None:
            print("Program init")
            # init the sports tracker API
            sp_api = SportsTrackerAPI(token=token, out_dir=out_dir)
        else:
            print('Incorrect arguments. Try again.')
            print('Usage: spt_export.py -t <Sports Tracker token> -o <Output folder>')
            sys.exit(2)

# Initiate main class object
start = Main(sys.argv[1:])