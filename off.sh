#!/bin/bash

# if usb is not mounted then unmount it!!
if [ $(mount | grep -c /media/pi) = 1 ]
then
	sudo umount -v /media/pi # unmount usb.
else
	echo "USB drive already not mounted! Double check footage was recorded..."
fi

sudo shutdown -h now
