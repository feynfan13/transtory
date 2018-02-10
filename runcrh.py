import sys
import argparse

from transtory.crh import logger, switch_to_test_mode
from transtory.crh import get_public_data_app
from transtory.crh import CrhRecorder, CrhTripStats, CrhTrainStats


def save_all_stats():
    stator = CrhTripStats()
    stator.save_all_stats()
    stator = CrhTrainStats()
    stator.save_all_stats()


parser = argparse.ArgumentParser(description="Shanghai metro database command.")
parser.add_argument("--testmode", action="store_const", const=True, default=False)
parser.add_argument("--record", action="store_const", const=True, default=False)
parser.add_argument("--update", action="store_const", const=True, default=False)
parser.add_argument("--stat", action="store_const", const=True, default=False)
parser.add_argument("--publicdata", action="store_const", const=True, default=False)
args = parser.parse_args(sys.argv[1:])

if args.testmode:
    logger.info("Running test mode")
    switch_to_test_mode()

if args.record:
    pass
    recorder = CrhRecorder()
    recorder.record_trips_from_json()
    save_all_stats()
elif args.update:
    pass
elif args.stat:
    save_all_stats()
elif args.publicdata:
    app = get_public_data_app()
    app.save_public_data()
else:
    logger.info("CRH module did nothing.")
