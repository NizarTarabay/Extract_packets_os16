from __future__ import print_function
import cv2
import os
import pickle
import helpers


import numpy as np
def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


os.chdir('/media/nizar/Transcend/pavement_distress_project/images/20191013135858/foreground/index')  # pickle file directory
frame_crack_id = pickle.load(open("frame_crack.pkl", "rb"))
cap = cv2.VideoCapture("/media/nizar/Transcend/pavement_distress_project/videos/20191013135858/rgb/2.MOV")
total_frames = cap.get(7)

# directory to save the extracted frames
''' uncomment this section to extract frames from rgb cam'''
os.chdir('/media/nizar/Transcend/pavement_distress_project/images/20191013135858/foreground/rgb')
for i in range(1, len(frame_crack_id)):
    filename = 'rgb' + str(frame_crack_id[i]) + '.png'
    cap.set(1, frame_crack_id[0] + frame_crack_id[i])
    ret, frame = cap.read()
    frame = np.rot90(frame, 2)
    crop_frame = frame[300:980, 0:1920]
    cv2.imwrite(filename, crop_frame)

# TODO: fetch lidar frmaes
file_name_t = input("Time and date:")
# my_format_directory = '/media/nizar/Transcend/test in the lab/Data/myFormat/Lidar'
# training_directory = '/media/nizar/Transcend/test in the lab/Data/training_data/'
# os.chdir(my_format_directory)

# file_name = 'Lidar_myFormat_packet_' + str(file_name_t) + '.txt'
#
# img_array_ref = helpers.get_signal(file_name, 2048, 'reflectivity')
# print ('reflectivity done \n')
# img_array_sig = helpers.get_signal(file_name, 2048, 'signal')
# print ('signal done \n')
# img_array_amb = helpers.get_signal(file_name, 2048, 'ambient')
# print ('ambient done \n')
# img_array_ran = helpers.get_signal(file_name, 2048, 'range')
# print ('range done \n')
#
#
# os.chdir(training_directory + '/reflectivity_lidar')
#
# for i in range(1, len(frame_crack_id)):
#     filename = 'reflectivity_lidar' + str(i) + '.png'
#     frame = img_array_ref[int(frame_crack_id[i]/12)]
#     frame = np.flip(np.rot90(frame, 3), 1)
#     img = cv2.resize(frame.astype('uint8'), (1024, 256))
#     adjusted = adjust_gamma(img, gamma=3)
#     cv2.imwrite(filename, adjusted)
#
# os.chdir(training_directory + '/signal_lidar')
#
# for i in range(1, len(frame_crack_id)):
#     filename = 'signal_lidar' + str(i) + '.png'
#     frame = img_array_sig[int(frame_crack_id[i]/12)]
#     frame = np.flip(np.rot90(frame, 3), 1)
#     img = cv2.resize(frame.astype('uint8'), (1024, 256))
#     adjusted = adjust_gamma(img, gamma=3)
#     cv2.imwrite(filename, adjusted)
#
# os.chdir(training_directory + '/ambient_lidar')
#
# for i in range(1, len(frame_crack_id)):
#     filename = 'ambient_lidar' + str(i) + '.png'
#     frame = img_array_amb[int(frame_crack_id[i]/12)]
#     frame = np.flip(np.rot90(frame, 3), 1)
#     img = cv2.resize(frame.astype('uint8'), (1024, 256))
#     adjusted = adjust_gamma(img, gamma=3)
#     cv2.imwrite(filename, adjusted)
#
# os.chdir(training_directory + '/range_lidar')
#
# for i in range(1, len(frame_crack_id)):
#     filename = 'range_lidar' + str(i) + '.png'
#     frame = img_array_ran[int(frame_crack_id[i]/12)]
#     frame = np.flip(np.rot90(frame, 3), 1)
#     img = cv2.resize(frame.astype('uint8'), (1024, 256))
#     adjusted = adjust_gamma(img, gamma=3)
#     cv2.imwrite(filename, adjusted)

def fetch_lidar_frame (signal, file_name_t, mode):
    '''
    this function fetch the frames that contains cracks or other distress
    :param signal: the lidar signal: range, reflectivity, signal, ambient
    :param file_name_t: file name: date and time e.g., 2019-10-13 13:58:58
    :return: save the frames in the corresponding directory
    '''
    my_format_directory = '/media/nizar/Transcend/pavement_distress_project/myformat/20191013135858'  # lidar myformat directory
    os.chdir(my_format_directory)
    file_name = 'Lidar_myFormat_packet_' + str(file_name_t) + '.txt'
    img_array = helpers.get_signal(file_name, 2048, signal)
    print(signal + ' done \n')

    training_directory = '/media/nizar/Transcend/pavement_distress_project/images/20191013135858/foreground'
    os.chdir(training_directory + '/' + signal)
    for i in range(1, len(frame_crack_id)):
        filename = signal + str(frame_crack_id[i]) + '.png'
        frame = img_array[int(frame_crack_id[i] / 12)]
        frame = frame[0:int(mode/4), :]
        frame = np.flip(np.rot90(frame, 3), 1)
        img = cv2.resize(frame.astype('uint8'), (1920, 680))  # size of the output image
        adjusted = adjust_gamma(img, gamma=3)
        cv2.imwrite(filename, adjusted)

mode = 2048
fetch_lidar_frame('reflectivity', file_name_t, mode)
fetch_lidar_frame('ambient', file_name_t, mode)
fetch_lidar_frame('signal', file_name_t, mode)
fetch_lidar_frame('range', file_name_t, mode)



# img = cv2.imread('/media/nizar/Transcend/test in the lab/Data/myFormat/Lidar/lidar2.png')
# for gamma in np.arange(0.0, 10, 0.5):
#     # ignore when gamma is 1 (there will be no change to the image)
#     if gamma == 1:
#         continue
#     # apply gamma correction and show the images
#     gamma = gamma if gamma > 0 else 0.1
#     adjusted = adjust_gamma(img, gamma=gamma)
#     cv2.putText(adjusted, "g={}".format(gamma), (10, 30),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
#     cv2.imshow("Images", np.hstack([img, adjusted]))
#     cv2.waitKey(0)

#
# img = cv2.imread('/media/nizar/Transcend/test in the lab/Data/myFormat/Lidar/lidar2.png')
#
# adjusted = adjust_gamma(img, gamma=3)
# cv2.imshow("Images", np.hstack([img, adjusted]))
# cv2.waitKey(0)