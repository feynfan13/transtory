import sys
import argparse
from transtory.shanghaibus import *


def save_all_stats():
    stator = ShbStats()
    stator.save_all_stats()


parser = argparse.ArgumentParser(description="Shanghai metro database command.")
parser.add_argument("--stats", action="store_const", const=True, default=False)
args = parser.parse_args(sys.argv[1:])

if args.stats:
    save_all_stats()
else:
    logger.info("Module shanghaibus does nothing.")
