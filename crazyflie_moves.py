"""
This script shows the basic use of the MotionCommander class.

Simple example that connects to the crazyflie at `URI` and runs a
sequence. This script requires some kind of location system, it has been
tested with (and designed for) the flow deck.

The MotionCommander uses velocity setpoints.

Change the URI variable to your Crazyflie configuration.
"""
import logging
import time
import _thread
import cflib.crtp

from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from handle_music import play_music

URI = 'radio://0/80/250K'

# Set log level
logging.basicConfig(level=logging.DEBUG)


def handle_beat():

    global beat_cnt
    global move_forward
    if move_forward:
        mc.forward(0.025, velocity=0.6)
        move_forward = False
    else:
        mc.back(0.025, velocity=0.6)
        move_forward = True

    if beat_cnt == 10:
        mc.stop()
    beat_cnt += 1
    print("beat cont: ", beat_cnt)


if __name__ == '__main__':
    # Initialize the low-level drivers (don't list the debug drivers)
    cflib.crtp.init_drivers(enable_debug_driver=False)


    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        # We take off when the commander is created
        with MotionCommander(scf) as mc:
            mc.up(0.5, velocity=0.5)
            time.sleep(3)
            print("Starting music...")
            beat_cnt = 0
            move_forward = True

            _thread.start_new_thread(play_music, ("LaCumparsita.mp3", handle_beat, 0))
            time.sleep(10)

            # There is a set of functions that move a specific distance
            # We can move in all directions
            # mc.up(0.5, velocity=0.5)
            # time.sleep(1)
            #
            # mc.forward(0.5, velocity=0.6)
            #
            # mc.back(0.5, velocity=0.6)
            #
            # mc.forward(0.5, velocity=0.6)
            #
            # mc.back(0.5, velocity=0.6)
            #
            # time.sleep(1)
            #
            # mc.turn_right(90)
            # mc.forward(1.0, velocity=0.4)
            # time.sleep(1)
            #
            # mc.turn_right(90)
            # mc.forward(1.0, velocity=0.4)
            # time.sleep(1)
            #
            # mc.turn_right(360)
            # mc.turn_right(90)
            # time.sleep(1)

            # And we can stop
            mc.stop()


