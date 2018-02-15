import sys
import argparse
from transtory.shanghaimetro import switch_to_test_mode, logger
from transtory.shanghaimetro import ShmRecorder, ShmTripStats, ShmTrainStats


def save_all_stats():
    stator = ShmTripStats()
    stator.save_all_stats()
    stator = ShmTrainStats()
    stator.save_all_stats()


parser = argparse.ArgumentParser(description="Shanghai metro database command.")
parser.add_argument("--testmode", action="store_const", const=True, default=False)
parser.add_argument("--record", action="store_const", const=True, default=False)
parser.add_argument("--stats", action="store_const", const=True, default=False)
args = parser.parse_args(sys.argv[1:])

if args.testmode:
    logger.info("Running test mode")
    switch_to_test_mode()

if args.record:
    recorder = ShmRecorder()
    recorder.record_trips_from_xlsx()
    save_all_stats()
elif args.stats:
    save_all_stats()
else:
    logger.info("Module shanghaimetro does nothing.")
