#!/bin/bash

# if usb is not mounted then mount it!
if [ $(mount | grep -c /media/pi) != 1 ]
then
	sudo mount -v /dev/sda1 /media/pi # mount usb
else
	echo "USB drive already mounted! Good to go..."
fi

python3 $PWD/camera.py # run camera script
