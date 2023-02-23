#!/usr/bin/env python3

import gi, os.path, pathlib, time
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst, Gtk, GLib

if __name__ == '__main__':
    Gst.init(None)
    player = Gst.ElementFactory.make('playbin')
    fakevideosink = Gst.ElementFactory.make('fakesink')
    player.set_property("video-sink", fakevideosink)
    uri1 = pathlib.Path(os.path.abspath("./bass_drum.wav")).as_uri()
    uri2 = pathlib.Path(os.path.abspath("./bass_drum_reverb.wav")).as_uri()
    player.set_property('uri', uri2)

    while True:
        player.set_state(Gst.State.PAUSED)
        player.seek(1.0,
                    Gst.Format.TIME,
                    Gst.SeekFlags.FLUSH,
                    Gst.SeekType.SET, 0,
                    Gst.SeekType.NONE, 0)
        player.set_state(Gst.State.PLAYING)
        while True:
            got_duration, duration = player.query_duration(Gst.Format.TIME)
            got_position, position = player.query_position(Gst.Format.TIME)
            print(f"position={position} duration={duration}")
            if got_duration and got_position:
                if position >= duration:
                    print(f"reached end")
                    break
            time.sleep(0.1)
        time.sleep(2) # wait 2 seconds before replaying the sound
