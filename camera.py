from picamera import PiCamera
from time import sleep
from subprocess import call, Popen
from datetime import datetime
from gpiozero import Button
from signal import pause
from os import mkdir
from PIL import Image

trigger = Button(2)
camera = PiCamera()
camera.resolution = (1920, 1080)
usb_path="/media/pi/"
overlay = Image.open("./overlay.png")
pad = Image.new('RGBA', (
        ((overlay.size[0] + 31) // 32) * 32,
        ((overlay.size[1] + 15) // 16) * 16,
        ))
pad.paste(overlay, (0, 0), overlay)

camera.start_preview()

def capture_all():
    o = camera.add_overlay(pad.tobytes(), size=overlay.size)
    o.alpha = 128
    o.layer = 3
    # create datetime stamped name for video file.
    nowish = datetime.now()
    datestamp = "%d%d%d%d%d" % (nowish.year, nowish.month, nowish.day, nowish.second, nowish.microsecond)
    recording_name = "useyourwords_%s" % (datestamp)

    rec_folder = usb_path + recording_name     
    mkdir(rec_folder)

    # create command to initilize recording and save as .wav
    recording_subprocess = "arecord --device=hw:1,0 -f dat -c1 -d 30 %s/%s.wav" % (rec_folder, recording_name)

    # record 10 seconds of video, show preview.
    # camera.start_preview()
    camera.start_recording(rec_folder + "/" + recording_name + '.h264')
    print("recording video...")
    
    # execute audio recording command in terminal UNSAFELY LOLZ
    Popen(recording_subprocess, shell=True)
    print("recording audio...")
    # Record 30 seconds of video
    camera.wait_recording(30)
    camera.stop_recording()
    camera.remove_overlay(o)
    # camera.stop_preview()

    print("capture complete!")
    #hold for 2 seconds
    sleep(2)

    # create command to convert the .h264 file to an .mp4 
    mp4_subprocess = "MP4Box -add %s/%s.h264 %s/%s.mp4" % (rec_folder, recording_name, rec_folder, recording_name)
    # execute conversion command in terminal 
    print("attempting to convert video...",  end='')
    call(mp4_subprocess, shell=True)
    print("success!")
    # remove original .h264 file.
    call('rm ' + rec_folder + '/' + recording_name +  '.h264', shell=True)
    print("deleted h264 capture.")
    # Settle down for 2 seconds, give processor some time to beath (it seems to crash less with this)
    sleep(2)


trigger.when_pressed = capture_all

pause()



