import sys
import argparse

from transtory.crh import logger, switch_to_test_mode
from transtory.crh import get_public_data_app


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
    # recorder = MobikeRecorder()
    # recorder.record_trips_from_xlsx()
    # stator = MobikeBikeStats()
    # stator.save_all_stats()
elif args.update:
    pass
    # recorder = MobikeRecorder()
    # recorder.update_trips_from_xlsx()
    # stator = MobikeBikeStats()
    # stator.save_all_stats()
elif args.stat:
    pass
    # stator = MobikeBikeStats()
    # stator.save_all_stats()
elif args.publicdata:
    app = get_public_data_app()
    app.save_public_data()
else:
    logger.info("CRH module did nothing.")
