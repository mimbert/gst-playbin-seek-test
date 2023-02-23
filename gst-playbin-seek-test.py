#!/usr/bin/env python3

import gi, os.path, pathlib, time, argparse
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, Gtk, GLib

BLOCKING_GET_STATE_TIMEOUT = 1000 * Gst.MSECOND

def set_state_blocking(element, state):
    print(f"set state blocking {state}")
    r = element.set_state(state)
    if r == Gst.StateChangeReturn.ASYNC:
        retcode, state, pending_state = element.get_state(BLOCKING_GET_STATE_TIMEOUT)
        if retcode == Gst.StateChangeReturn.FAILURE:
            print(f"WARNING: gst async state change failure after timeout of {BLOCKING_GET_STATE_TIMEOUT / Gst.MSECOND}ms. retcode: {retcode}, state: {state}, pending_state: {pending_state}")
        elif retcode == Gst.StateChangeReturn.ASYNC:
            print(f"WARNING gst async state change still async after timeout of {BLOCKING_GET_STATE_TIMEOUT / Gst.MSECOND}ms. retcode: {retcode}, state: {state}, pending_state: {pending_state}")
    retcode, state, pending_state = element.get_state(0)
    print(f"set_state_blocking returns {retcode} {state} {pending_state}")
    return retcode, state, pending_state

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gstreamer playbin seek test')
    parser.add_argument('path', help='file to open with playbin')
    args = parser.parse_args()

    Gst.init(None)
    player = Gst.ElementFactory.make('playbin')
    uri = pathlib.Path(os.path.abspath(args.path)).as_uri()
    player.set_property('uri', uri)

    while True:
        player.set_state(Gst.State.PAUSED)
        player.seek(1.0,
                    Gst.Format.TIME,
                    Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
                    Gst.SeekType.SET, 0,
                    Gst.SeekType.NONE, 0)
        player.set_state(Gst.State.PLAYING)
        while True:
            got_duration, duration = player.query_duration(Gst.Format.TIME)
            got_position, position = player.query_position(Gst.Format.TIME)
            print(f"got_position={got_position} position={position} got_duration={got_duration} duration={duration}")
            if got_duration and got_position:
                if position >= duration:
                    print(f"reached end")
                    break
            time.sleep(0.1)
        time.sleep(2) # wait 2 seconds before replaying the sound
