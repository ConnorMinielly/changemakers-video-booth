#!/bin/bash

# if usb is not mounted then mount it!
if [ $(mount | grep -c /media/pi) != 1 ]
then
	trymount=sudo mount -v /dev/sda1 /media/pi # mount usb, but first i gotta find out how to check for the usb when everything else is plugged in
else
	echo "USB drive already mounted! Good to go..."
fi

python3 $PWD/camera.py

# Remember you gotta setup MP4Box shit and ffmpeg
