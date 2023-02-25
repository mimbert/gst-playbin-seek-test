#!/usr/bin/env python3

import gi, os.path, pathlib, time, argparse, threading
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, Gtk, GLib

BLOCKING_GET_STATE_TIMEOUT = 1000 * Gst.MSECOND

finished = threading.Event()

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

def wait_state_stable(element):
    while True:
        print(f"wait state of {element} stable")
        retcode, state, pending_state = element.get_state(Gst.CLOCK_TIME_NONE)
        print(f"retcode = {retcode}, state = {state}, pending_state = {pending_state}")
        if retcode == Gst.StateChangeReturn.SUCCESS:
            print(f"ok no more pending state changes")
            return retcode, state, pending_state

def safe_seek(element, rate, format, flags, start_type, start, stop_type, stop):
    while True:
        retcode, state, pending_state = wait_state_stable(element)
        if (state == Gst.State.PAUSED
            or (state == Gst.State.PLAYING
                and flags & Gst.SeekFlags.FLUSH)):
            break
    print(f"OK we can seek")
    return element.seek(rate, format, flags, start_type, start, stop_type, stop)

def gst_bus_message_handler(bus, message, *user_data):
    player = user_data[0]
    print(f"gst_bus_message_handler message: {message.type.first_value_name}: {message.get_structure().to_string() if message.get_structure() else 'None'}")
    if message.type in [ Gst.MessageType.EOS, Gst.MessageType.SEGMENT_DONE ]:
        finished.set()
    if message.type == Gst.MessageType.WARNING:
        print(f"WARNING: Gstreamer WARNING: {message.type}: {message.get_structure().to_string()}")
    elif message.type == Gst.MessageType.ERROR:
        print(f"WARNING: Gstreamer ERROR: {message.type}: {message.get_structure().to_string()}")
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='gstreamer playbin seek test')
    parser.add_argument('path', help='file to open with playbin')
    parser.add_argument('--sink', type=str, help='select audio sink. List of properties can be given with the syntax --sink=sinkname[/property1=value1][/property2=value2...].')
    args = parser.parse_args()
    threading.Thread(daemon=True, target=lambda: GLib.MainLoop.new(None, False).run()).start()
    Gst.init(None)
    player = Gst.ElementFactory.make('playbin')
    player.set_property('flags', player.get_property('flags') & ~(0x00000001 | 0x00000004 | 0x00000008)) # disable video, subtitles, visualisation
    if args.sink:
        params = args.sink.split('/')
        sinkname = params.pop(0)
        properties = {}
        for p in params:
            k, _, v = p.partition('=')
            properties[k] = v
        audiosink = Gst.ElementFactory.make(sinkname)
        if not audiosink:
            print(f"unable to instanciate {sinkname}")
            exit(1)
        for k in properties:
            audiosink.set_property(k, properties[k])
        player.set_property("audio-sink", audiosink)
    player.get_bus().add_watch(GLib.PRIORITY_DEFAULT, gst_bus_message_handler, player)
    uri = pathlib.Path(os.path.abspath(args.path)).as_uri()
    player.set_property('uri', uri)
    while True:
        print("start")
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
                if position >= duration or finished.is_set():
                    print("end")
                    break
            time.sleep(0.1)
        finished.clear()
        time.sleep(1) # wait before replaying the sound
