from helpers import number_of_frames, frame_list
import os


mode = 1024

os.chdir('/media/nizar/Transcend/test in the lab/Data/myFormat/Lidar')
file_name_t = input("Time and date:")
# file_name = 'Lidar_myFormat_packet_' + str(file_name_t) + '.txt'
# img_array = get_signal(file_name, mode, 'signal')
########################################################################################################################
file_name = 'Lidar_myFormat_packet_' + str(file_name_t)
img_array_depth, list = number_of_frames(file_name + '.txt', mode)

lis = frame_list(list)
frame = []
index = []
i = 0
j = 0
element_old_old = 0
element_old = lis[0]
for element in lis:

    if element_old == element:
        i += 1
        element_old = element
    else:
        frame.append(i)
        i=0
        if element-element_old > 1 and j != 0:
            print ('dropping frames:', element-element_old )
            idx = lis.index(element_old)
            index.append(idx)
            element_old_old = element_old
        else:
            print ('no frame losses')
        element_old = element
    j += 1


import matplotlib.pyplot as plt
plt.plot(frame)
plt.ylabel('number of frames')
plt.show()