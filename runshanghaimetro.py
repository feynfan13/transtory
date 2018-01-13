import sys
import argparse
from transtory.shanghaimetro import switch_to_test_mode, logger
from transtory.shanghaimetro import ShmRecorder


parser = argparse.ArgumentParser(description="Shanghai metro database command.")
parser.add_argument("--testmode", action="store_const", const=True, default=False)
parser.add_argument("--recorder", action="store_const", const=True, default=False)
args = parser.parse_args(sys.argv[1:])

if args.testmode:
    logger.info("Running test mode")
    switch_to_test_mode()

if args.recorder:
    recorder = ShmRecorder()
    recorder.record_trips_from_xlsx()
