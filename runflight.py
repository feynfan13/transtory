import sys
import argparse

from transtory.flight import logger, switch_to_test_mode
from transtory.flight import get_public_data_app
from transtory.flight import FlightRecorder, FlightTripStats


def save_all_stats():
    stator = FlightTripStats()
    stator.save_all_stats()
    # stator = CrhTrainStats()
    # stator.save_all_stats()


parser = argparse.ArgumentParser(description="Flight database command.")
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
    recorder = FlightRecorder()
    recorder.record_trips_from_xmls()
    save_all_stats()
elif args.update:
    pass
elif args.stat:
    save_all_stats()
elif args.publicdata:
    app = get_public_data_app()
    app.save_public_data()
else:
    logger.info("Flight module did nothing.")
