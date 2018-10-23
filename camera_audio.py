from picamera import PiCamera
from time import sleep
from subprocess import call, Popen
from datetime import datetime
from gpiozero import Button
from signal import pause

trigger = Button(2)
camera = PiCamera()
camera.resolution = (1920, 1080)

def capture_all():
    # create datetime stamped name for video file.
    nowish = datetime.now()
    datestamp = "%d%d%d%d%d" % (nowish.year, nowish.month, nowish.day, nowish.second, nowish.microsecond)
    recording_name = "useyourwords_%s" % (datestamp)

    # create command to initilize recording and save as .wav
    recording_subprocess = "arecord --device=hw:1,0 -f dat -c1 -d 30 %s.wav" % (recording_name)

    # record 10 seconds of video, show preview.
    camera.start_preview()
    camera.start_recording(recording_name + '.h264')
    print("recording video...")
    
    # execute audio recording command in terminal UNSAFELY LOLZ
    Popen(recording_subprocess, shell=True)
    print("recording audio...")
    # Record 30 seconds of video
    camera.wait_recording(30)
    camera.stop_recording()
    camera.stop_preview()

    print("capture complete!")
    #hold for 2 seconds
    sleep(2)

    # create command to convert the .h264 file to an .mp4 
    mp4_subprocess = "MP4Box -add %s.h264 %s.mp4" % (recording_name, recording_name)
    # execute conversion command in terminal 
    print("attempting to convert video...",  end="")
    call(mp4_subprocess, shell=True)
    print("success!")
    # remove original .h264 file.
    call('rm ' + recording_name +  '.h264', shell=True)
    print("deleted h264 capture.")
    # Settle down for 2 seconds, give processor some time to beath (it seems to crash less with this)
    sleep(2)

    # compose command to merge audio and video
    merge_subprocess = "ffmpeg -i %s.mp4 -i %s.wav -shortest %s_final.mp4" %(recording_name,recording_name,recording_name)
    # execute merge subprocess
    print("attempting audio / video merge...", end="")
    call(merge_subprocess, shell=True)
    print("success!")

    # close camera
    camera.close();

trigger.when_pressed = capture_all

pause()
