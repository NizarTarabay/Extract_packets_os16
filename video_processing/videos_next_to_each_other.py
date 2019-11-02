import cv2
import os
import numpy as np
import time
import glob
import keyboard  # using module keyboard
import subprocess
from moviepy.editor import VideoFileClip
import pickle

os.chdir('/home/nizar/Desktop/videos_camera_lidar/2')

f = open("crack.txt", "w+")

sync_frames = 17700
frame_crack = [17700]
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
cap1 = cv2.VideoCapture('2.MOV')  # cam's video
cap1.set(1, sync_frames) # sync_time x number of fps = sync_frames = 17700 is the number of frames at the synchronization time
cap2 = cv2.VideoCapture('Lidar_myFormat_packet_2019-10-13 13:58:58_reflectivity.avi')  # lidar's video
cap2.set(1, 0)
clip = VideoFileClip('Lidar_myFormat_packet_2019-10-13 13:58:58_reflectivity.avi')
clip_duration = clip.duration
# vidwrite = cv2.VideoWriter('20190902_163851_output.MOV', cv2.VideoWriter_fourcc(*'XVID'), 25, (640, 480), True)
img_array = []
i = 0
images = []
while i < clip_duration * 120: # 3000: #clip_duration * 120:  # 120 is the frame number
    # time.sleep(0.01)
    ret1, frame1 = cap1.read()
    if i % 12 == 0:  # 12 = fps_cam/fps_lidar
        print(i)
        ret2, frame2 = cap2.read()
        t = 0
        if keyboard.is_pressed('p'):  # if key 'q' is pressed
            print('Pause')
            frame_crack.append(i)
            while (t == 0):
                if keyboard.is_pressed('u'):
                    print('Play')
                    t = 1
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.resize(gray1, (1920, 500))
    gray2 = cv2.resize(gray2, (1920, 500))
    concatenate = np.vstack((gray2, gray1))
    concatenate = np.rot90(concatenate, 2)
    if i% 12 == 0:
        images.append(concatenate)


    cv2.imshow('frame', concatenate)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i += 1
    # cv2.VideoWriter(['20190902_163851_output.MOV', cv2.VideoWriter_fourcc(*'MJPG'), 20, (1000,700), True])
pickle.dump(frame_crack, open('frame_crack.pkl', 'wb'))
cap1.release()
cap2.release()
cv2.destroyAllWindows()

#
# height = 1000
# width = 1920
#
# image_folder = 'images'
# video_name = 'video.avi'
# fps = 8
#
# # initialize water image

# water_depth = np.zeros((height, width), dtype=float)
# # initialize video writer
# fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
# video_filename = video_name
# out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))
# # new frame after each addition of water
# for image in images:
#     #add this array to the video
#     gray = cv2.normalize(np.asarray(image), None, 255, 0, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
#     gray_3c = cv2.merge([gray, gray, gray])
#     out.write(gray_3c)
# # close out the video writer
# out.release()