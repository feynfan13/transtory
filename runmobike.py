import sys
import argparse

from transtory.mobike import switch_to_test_mode, logger
from transtory.mobike import MobikeRecorder, MobikeBikeStats


parser = argparse.ArgumentParser(description="Mobike database command.")
parser.add_argument("--testmode", action="store_const", const=True, default=False)
parser.add_argument("--record", action="store_const", const=True, default=False)
parser.add_argument("--update", action="store_const", const=True, default=False)
parser.add_argument("--stat", action="store_const", const=True, default=False)
args = parser.parse_args(sys.argv[1:])

if args.testmode:
    logger.info("Running test mode")
    switch_to_test_mode()

if args.record:
    recorder = MobikeRecorder()
    recorder.record_trips_from_xlsx()
    stator = MobikeBikeStats()
    stator.save_all_stats()
elif args.update:
    recorder = MobikeRecorder()
    recorder.update_trips_from_xlsx()
    stator = MobikeBikeStats()
    stator.save_all_stats()
elif args.stat:
    stator = MobikeBikeStats()
    stator.save_all_stats()
else:
    logger.info("Mobike module did nothing.")
