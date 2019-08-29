import numpy as np
import os
mode = 2048

def number_of_frames(file, mode):
    '''
    :arg: string;  Name of the file with a specific format (like the one returned by the function "extract_data_txt_file")
    :return: int; This function return the total number of frames in the txt file
    '''
    # mode = 2048  # depend on the scanning mode of the lidar, it can take the following values: 512, 1024, 2048
    fn = 65536  # 2^16 max frame number (max reached)
    # =============== open the file =============== #
    file1 = open(file, 'r')
    lineList = file1.readlines()  # save all the lines in a list
    file1.close()
    # =============== close the file =============== #

    # =============== get the first frame number =============== #
    for line in lineList:
        if 'F' in line:
            # print(line)
            i = 0
            l = []
            for c in line:
                if i == 1 and c != ' ':
                    l.append(c)
                if c == ' ':
                    i += 1
                if i == 2:
                    break
            f1 = ''
            f1 = int(f1.join(l))
            break
    # =============== get the last frame number =============== #
    for line in lineList[::-1]:
        if 'F' in line:
            # print(line)
            i = 0
            l = []
            for c in line:
                if i == 1 and c != ' ':
                    l.append(c)
                if c == ' ':
                    i += 1
                if i == 2:
                    break
            f2 = ''
            f2 = int(f2.join(l))
            break
    # =============== check if the max has been reached =============== #
    max_frame_reach = 0
    i = 0
    for line in lineList:
        if i % 17 == 0:
            if 'F 65535' in line:
                # print(line)
                max_frame_reach += 1
        i += 1


    i = int(max_frame_reach/(mode/4))
    # print (i)
    number_frames = int(f2 - f1 + i * fn)

    return number_frames, lineList


# =============== Build the array of images =============== #
os.chdir('/media/nizar/Transcend/test in the lab/Data/myFormat/Lidar')
file_name_t = input("Time and date:")
file_name = 'Lidar_myFormat_packet_' + str(file_name_t) + '.txt'
img_array_depth, list = number_of_frames(file_name, mode)
img_array = np.zeros((img_array_depth, int(mode/4)+17, 16)).astype(np.int) # this is the array the contains all the pixels acquired by the sensor
m, i, j, k, l = 0 , 0 ,0 , 0, 0
enc_list = []
#find the smallest encoder number
for m in range(0, len(list)):
    if m % 17 == 0:
        encoder_count = ['0']
        s = 0
        for c in list[m]:
            if s == 3 and (c != ' ' or c != '\n'):  # s=3 for encoder count
                encoder_count.append(c)
            if c == ' ':
                s += 1
            if s == 4:  # s=4 for encoder count
                break
        enc = ''
        enc = (int(enc.join(encoder_count)))
        #print(enc)
        enc_list.append(enc)

enc_min = min(enc_list)
######################################### for: fill the array! ##############################################
for k in range(0, img_array_depth):
    # print(l)
    for j in range(0, int(mode/4)+17):
        for i in range(0, 17):
            if l % 17 == 0:
                encoder_count = ['0']
                s = 0
                for c in list[l]:
                    if s == 3 and (c != ' ' or c != '\n'):  # s=3 encoder don't touch!
                        encoder_count.append(c)
                    if c == ' ':
                        s += 1
                    if s == 4:  # s=4 encoder don't touch!
                        break
                enc = ''
                enc = (int(enc.join(encoder_count))-enc_min)/(44*(2048/mode))
            else:
                signal = ['0']
                s = 0
                for c in list[l]:
                    if s == 0 and (c != ' ' or c != '\n'):  # s=1 or 0 1 for reflectivity 0 for range
                        signal.append(c)
                    if c == ' ':
                        s += 1
                    if s == 1:    # s=1 or 2; 2 for reflectivity 1 for range
                        break
                sig = ''
                sig = int(sig.join(signal))
                img_array[k][int(enc)][i-1] = sig

            l += 1
            # print(l)
            if l >= len(list):
                break
        if l >= len(list):
            break
    if l >= len(list):
        break
            # print (l)
        # print (j)
    # print (k)
print(enc)
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

# ax = sns.heatmap(img_array[222][0:256], square=True, linewidth=0)
# plt.show()


b = np.zeros((k, int(mode/4), 64))
for frame in range(0, k):
    for i in range(0, 16):
        for j in range(0, 4):
            b[frame][0:int(mode/4), i*4+j] = img_array[frame][0:int(mode / 4), i]



im = plt.imshow(b[1][0:int(mode/4)])
for i in range(0, k):
    # im.set_data(b[i][0:int(mode/4)])
    im = plt.imshow(np.rot90(b[i][0:int(mode/4)], 3))
    plt.axis('off')
    plt.pause(0.01)

