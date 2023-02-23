# coding: utf-8
Vagrant.configure("2") do |config|

  config.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: [".git/" , ".#*" ]
  config.ssh.forward_agent = true
  config.ssh.forward_x11 = true
  apt = "DEBIAN_FRONTEND=noninteractive apt-get -q -y"
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, '--audio', 'pulse', '--audioin', 'on', '--audioout', 'on', '--audiocontroller', 'ac97'] # choices: hda sb16 ac97
  end

  config.vm.define "debstable" do |conf|
    # debian stable
    conf.vm.box = "debian/bullseye64"
    conf.vm.provision "shell", inline: <<-SHELL
set -e
echo "deb https://deb.debian.org/debian testing main non-free contrib" >> /etc/apt/sources.list
echo "Package: *\nPin: release a=bullseye\nPin-Priority: 700\n\nPackage: *\nPin: release a=stable\nPin-Priority: 700\n\nPackage: *\nPin: release a=bookworm\nPin-Priority: -1\n\nPackage: *\nPin: release a=testing\nPin-Priority: -1" > /etc/apt/preferences.d/pinning
#{apt} update
#{apt} full-upgrade
#{apt} install xauth alsa-utils pulseaudio
#{apt} install python3-yaml python3-schema python3-pyside2.qtcore python3-pyside2.qtgui python3-pyside2.qtwidgets python3-gst-1.0 gir1.2-gtk-3.0
#{apt} install gstreamer1.0-plugins-base gstreamer1.0-plugins-good
adduser vagrant audio
amixer set Master 100%
amixer set Master unmute
amixer set PCM 100%
amixer set PCM unmute
    SHELL
  end

  config.vm.define "debstable2" do |conf|
    # debian stable with gstreamer from testing
    conf.vm.box = "debian/bullseye64"
    conf.vm.provision "shell", inline: <<-SHELL
set -e
echo "deb https://deb.debian.org/debian testing main non-free contrib" >> /etc/apt/sources.list
echo "Package: *\nPin: release a=bullseye\nPin-Priority: 700\n\nPackage: *\nPin: release a=stable\nPin-Priority: 700\n\nPackage: *\nPin: release a=bookworm\nPin-Priority: -1\n\nPackage: *\nPin: release a=testing\nPin-Priority: -1" > /etc/apt/preferences.d/pinning
#{apt} update
#{apt} full-upgrade
#{apt} install xauth alsa-utils pulseaudio
#{apt} install python3-yaml python3-schema python3-pyside2.qtcore python3-pyside2.qtgui python3-pyside2.qtwidgets python3-gst-1.0 gir1.2-gtk-3.0
#{apt} install -t testing gstreamer1.0-plugins-base gstreamer1.0-plugins-good
adduser vagrant audio
amixer set Master 100%
amixer set Master unmute
amixer set PCM 100%
amixer set PCM unmute
    SHELL
  end

  config.vm.define "debtesting" do |conf|
    # debian testing
    conf.vm.box = "debian/testing64"
    conf.vm.provision "shell", inline: <<-SHELL
set -e
echo "deb https://deb.debian.org/debian bullseye main non-free contrib" >> /etc/apt/sources.list
echo "deb https://security.debian.org/debian-security bullseye-security main non-free contrib" >> /etc/apt/sources.list
echo "deb https://deb.debian.org/debian bullseye-updates main non-free contrib" >> /etc/apt/sources.list
echo "deb https://deb.debian.org/debian bullseye-backports main non-free contrib" >> /etc/apt/sources.list
echo "Package: *\nPin: release a=bullseye\nPin-Priority: 700\n\nPackage: *\nPin: release a=stable\nPin-Priority: 700\n\nPackage: *\nPin: release a=bookworm\nPin-Priority: 700\n\nPackage: *\nPin: release a=testing\nPin-Priority: 700" > /etc/apt/preferences.d/pinning
#{apt} update
#{apt} full-upgrade
#{apt} install xauth alsa-utils pipewire
#{apt} install python3-yaml python3-schema python3-pyside2.qtcore python3-pyside2.qtgui python3-pyside2.qtwidgets python3-gst-1.0 gir1.2-gtk-3.0
#{apt} install gstreamer1.0-plugins-base gstreamer1.0-plugins-good
adduser vagrant audio
amixer set Master 100%
amixer set Master unmute
amixer set PCM 100%
amixer set PCM unmute
    SHELL
  end

  config.vm.define "debtesting2" do |conf|
    # debian testing with gstreamer  from stable
    conf.vm.box = "debian/testing64"
    conf.vm.provision "shell", inline: <<-SHELL
set -e
echo "deb https://deb.debian.org/debian bullseye main non-free contrib" >> /etc/apt/sources.list
echo "deb https://security.debian.org/debian-security bullseye-security main non-free contrib" >> /etc/apt/sources.list
echo "deb https://deb.debian.org/debian bullseye-updates main non-free contrib" >> /etc/apt/sources.list
echo "deb https://deb.debian.org/debian bullseye-backports main non-free contrib" >> /etc/apt/sources.list
echo "Package: *\nPin: release a=bullseye\nPin-Priority: 700\n\nPackage: *\nPin: release a=stable\nPin-Priority: 700\n\nPackage: *\nPin: release a=bookworm\nPin-Priority: 700\n\nPackage: *\nPin: release a=testing\nPin-Priority: 700" > /etc/apt/preferences.d/pinning
#{apt} update
#{apt} full-upgrade
#{apt} install xauth alsa-utils pipewire
#{apt} install python3-yaml python3-schema python3-pyside2.qtcore python3-pyside2.qtgui python3-pyside2.qtwidgets python3-gst-1.0 gir1.2-gtk-3.0
#{apt} install -t bullseye gstreamer1.0-plugins-base gstreamer1.0-plugins-good
adduser vagrant audio
amixer set Master 100%
amixer set Master unmute
amixer set PCM 100%
amixer set PCM unmute
    SHELL
  end

end
