import numpy as np

'''
The following script contains function to extract information from myFormat file. 
MyFormat file is a file created by the author of this code. 
Myformat file is a txt file that contains all the data returned from the lidar in a readable format.
To generate myFormat file, translate the binary txt file: 'Lidar_byte_packet_date_and_time.txt' to 
                                                          'Lidar_myFormat_packet_date_and_time.txt'
Refer to readme(myFormat) for more information on how data is distributed in this file.
'''


def frame_list(linelist):
    '''
    This function helps to find the first and the last frame number from myFormat file
    :param line: string; a line from the file myFormat
    :return: integer; a number reflecting the first or the last frame according on how I start reading the list that
    contains all information from myFormat file.
    '''
    frames = []
    for line in linelist:
        if 'F' in line:
            # print(line)
            i = 0
            l = []
            for c in line:
                if i == 3 and c != ' ':
                    l.append(c)
                if c == ' ':
                    i += 1
                if i == 4:
                    break
            f = ''
            f = int(f.join(l))
            frames.append(f)
            print(line)
    return frames
#
mode = 2048


def first_last_frame_number(line):
    '''
    This function helps to find the first and the last frame number from myFormat file
    :param line: string; a line from the file myFormat
    :return: integer; a number reflecting the first or the last frame according on how I start reading the list that
    contains all information from myFormat file.
    '''

    if 'F' in line:
        # print(line)
        i = 0
        l = []
        for c in line:
            if i == 3 and c != ' ':
                l.append(c)
            if c == ' ':
                i += 1
            if i == 4:
                break
        f = ''
        f = int(f.join(l))
        return f
    else:
        return -1


def number_of_frames(file, mode):
    '''

    :param file: myFormat file name
    :param mode: 512, 1021, 2048
    :return: the total number of frames captured in the myFormat file / lineList: all the lines in the myFormat file

    '''
    # mode = 2048  # depend on the scanning mode of the lidar, it can take the following values: 512, 1024, 2048
    fn = 65536  # 2^16 max frame number (max reached)
    # =============== open the file =============== #
    file1 = open(file, 'r')
    lineList = file1.readlines()  # save all the lines in a list
    file1.close()

    # =============== get the first frame number =============== #
    f1 = -1
    while f1 == -1:
        for line in lineList:
            f1 = first_last_frame_number(line)
            print('First frame: ', f1)
            break
    # =============== get the last frame number =============== #
    f2 = -1
    while f2 == -1:
        for line_rev in lineList[::-1]:
            f2 = first_last_frame_number(line_rev)
            print('Last frame: ', f2)
            if f2 != -1:
                break
    # =============== check if the max has been reached =============== #
    max_frame_reach = 0
    i = 0
    for line in lineList:
        if i % 18 == 0:
            if 'F 65535' in line:
                max_frame_reach += 1
        i += 1

    i = int(max_frame_reach/(mode/4))
    number_frames = int(f2 - f1 + i * fn)

    return number_frames, lineList


def smallest_encoder_tick(linelist):
    '''

    :param linelist: List of all the lines in the myFormat file
    :return: the smallest encoder tick (we need this value to locate the edges of each frame)
    '''
    enc_list = []
    for m in range(0, len(linelist)):
        if m % 18 == 0:
            encoder_count = ['0']
            s = 0
            for c in linelist[m]:
                if s == 5 and (c != ' ' or c != '\n'):  # s=5 for encoder count
                    encoder_count.append(c)
                if c == ' ':
                    s += 1
                if s == 6:  # s=6 for encoder count
                    break
            enc = ''
            enc = (int(enc.join(encoder_count)))
            print(enc)
            enc_list.append(enc)

    enc_min = min(enc_list)
    return enc_min


def signal_data(signal_name, l, line_list, img_array, k, enc, i):
    '''
    This function get access to the lines that contains the channels' signals and extract the requested signal from them
    :param signal_name: string; which signal you are looking after;
    can take the following values:'range', 'reflectivity', 'signal', 'ambient'
    :param l: this is an index to iterate between the list of the lines that belong to myFormat file
    :param line_list: List of all the lines in the myFormat file
    :param img_array: empty, a 3 dimensional array:
    total number of frames x (512 or 256 depending on the mode) x 16 channels
    :param k: to iterate between frames k in range (0: total number of frames)
    :param enc: get the encoder value to locate the 16 channels in each frame enc in range (0: 512) or (0: 256)
    :param i: to iterate between the 16 channels
    :return: img_array: full, a 3 dimensional array:
    total number of frames x (512 or 256 depending on the mode) x 16 channels
    '''
    signal = ['0']
    s = 0
    signal_list = ['range', 'reflectivity', 'signal', 'ambient']
    for idx, val in enumerate(signal_list):
        if signal_name == val:
            break
    for c in line_list[l]:
        if s == idx and (c != ' ' or c != '\n'):  # s=1 or 0 1 for reflectivity 0 for range
            signal.append(c)
        if c == ' ':
            s += 1
        if s == idx + 1:  # s=1 or 2; 2 for reflectivity 1 for range
            break
    sig = ''
    sig = int(sig.join(signal))
    img_array[k][int(enc)][i - 1] = sig
    return img_array


def get_signal(file, mode, signal_name):
    '''
    This function get access to the lines in the myFormat file and extract the information related to the encoder,
    to the frame, and to the signal
    :param file: myFormat file name
    :param mode: 512, 1021, 2048
    :param signal_name: string; which signal you are looking after;
    :return: img_array: full, a 3 dimensional array:
    total number of frames x (512 or 256 depending on the mode) x 16 channels
    '''

    img_array_depth, linelist = number_of_frames(file, mode)
    img_array = np.zeros((img_array_depth+1, int(mode / 4) + 17, 16)).astype(
        np.int)  # this is the array the contains all the pixels acquired by the sensor
    m, i, j, k, l = 0, 0, 0, 0, 0

    enc_min = smallest_encoder_tick(linelist)
    framelist = frame_list(linelist)[0]
    for k in range(0, img_array_depth+1):
        for j in range(0, int(mode / 4) + 17):
            for i in range(0, 18):
                if l % 18 == 0:
                    encoder_count = ['0']
                    s = 0
                    for c in linelist[l]:
                        if s == 5 and (c != ' ' or c != '\n'):  # s=3 encoder don't touch!
                            encoder_count.append(c)
                        if c == ' ':
                            s += 1
                        if s == 6:  # s=4 encoder don't touch!
                            break
                    enc = ''
                    enc = (int(enc.join(encoder_count)) - enc_min) / (44 * (2048 / mode))
                    real_frame = first_last_frame_number(linelist[l]) #add
                else:
                    if (l + 1) % 18 != 0:
                        # img_array = signal_data(signal_name, l, linelist, img_array, k, enc, i)
                        img_array = signal_data(signal_name, l, linelist, img_array, real_frame - framelist, enc, i)


                l += 1
                if l >= len(linelist):
                    break
            if l >= len(linelist):
                break
        if l >= len(linelist):
            break
    return img_array


#
# def packet_checker ():
#     '''
#
#     :return: this function returns a boolean indicates if the packet is good or bad
#     '''
#

def resize_img(max_size):
    '''
    this function take image or image directory and resize the image(s) to the max_size input keeping the aspect ratio of the image
    img_dir: img_dir path
    max_size: output rescale size (width; assumption width of the input image is bigger than the height)
    '''
    from tkinter import filedialog, Tk
    import os
    import glob
    import cv2
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    path_selected = filedialog.askdirectory()  # show an "Open" dialog box and return the path to the selected file
    print(path_selected)

    os.chdir(path_selected)
    for filename in glob.glob("*.png"):
        img = cv2.imread(filename, 0)
        scale_percent = (max_size / img.shape[1]) * 100 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        path = '/media/nizar/Transcend/test in the lab/Data/Build_synthetic_dataset/images'
        cv2.imwrite(os.path.join(path, filename), resized)
        cv2.waitKey(0)
