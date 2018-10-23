from picamera import PiCamera
from time import sleep
from subprocess import call, Popen
from datetime import datetime

camera = PiCamera()
camera.resolution = (1920, 1080)

# create datetime stamped name for video file.
nowish = datetime.now()
datestamp = "%d%d%d%d%d" % (nowish.year, nowish.month, nowish.day, nowish.second, nowish.microsecond)
recording_name = "useyourwords_%s" % (datestamp)

# create command to convert the .h264 file to an .mp4 
recording_subprocess = "arecord --device=hw:1,0 -f dat -c1 -d 10 %s.wav" % (recording_name)
# execute command in terminal UNSAFELY LOLZ
Popen(recording_subprocess, shell=True)

# record 10 seconds of video, show preview.
camera.start_preview()
camera.start_recording(recording_name + '.h264')
camera.wait_recording(10)
camera.stop_recording()
camera.stop_preview()

#hold for 2 seconds (previously 3)
sleep(2)

# create command to convert the .h264 file to an .mp4 
mp4_subprocess = "MP4Box -add %s.h264 %s.mp4" % (recording_name, recording_name)
# execute command in terminal UNSAFELY LOLZ
call(mp4_subprocess, shell=True)
# remove original .h264 file.
call('rm ' + recording_name +  '.h264', shell=True)

sleep(2) # was 3

merge_subprocess = "ffmpeg -i %s.mp4 -i %s.wav -shortest %s_final.mp4" %(recording_name,recording_name,recording_name)
call(merge_subprocess, shell=True)

camera.close();
    
