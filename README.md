# gst-playbin-seek-test

Plays a sound with a fast attack with gstreamer playbin. Check
behavior in VMs debian bullseye with pulseaudio and debien testing
with pipewire.

Dependencies: vagrant (virtualbox)

Usage:

- build the VMS

```
$ vagrant up
```

- connect to a VM and run the test

```
$ vagrant ssh <debstable|debtesting>
vagrant$ cd /vagrant
vagrant$ ./gst-playbin-seek-test.py
```
