import numpy as np
import matplotlib.pyplot as plt
import math


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


def get_frame(file, mode, signal_name, frame_id):
    '''
    this function fetch a specific frame according to its frame id
    :param file: myFormat file name
    :param mode: 512, 1021, 2048
    :param signal_name: string; which signal you are looking after;
    :param frame_id: the requested frame
    :return: array; the array contains the signal value of a specific frame
    '''
    frame = get_signal(file, mode, signal_name)[frame_id]
    return frame


def frame_drop_checker (line_list):
    '''
    This function check myFormat file for any dropping packets and fromes, it shows a graph of where the packages are
    dropped and how many frames are missed
    :param line_list: List of all the lines in the myFormat file
    :return:
    '''

    lis = frame_list(line_list)
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
            # else:
                # print ('no frame losses')
            element_old = element
        j += 1

    plt.plot(frame)
    plt.ylabel('number of frames')
    plt.show()


def spherical_coordinate_data( l, line_list, spherical_coordinate_array, k, enc, i, channel_angle):
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
    enc_min = 33792
    #encoder = (enc * 44 * (2048/mode) + enc_min)*360 / 90112
    encoder = -(enc * 44 * (2048/mode) + enc_min)*360 / 90112 +360
    # encoder = (-(360 / 90112) * enc * 44 * (2048/mode) + 360) +224
    signal = ['0']
    s = 0
    for c in line_list[l]:
        if s == 0 and (c != ' ' or c != '\n'):  # s=1 or 0 1 for reflectivity 0 for range
            signal.append(c)
        if c == ' ':
            s += 1
        if s == 1:  # s=1 or 2; 2 for reflectivity 1 for range
            break
    sig = ''
    sig = int(sig.join(signal))
    spherical_coordinate_array[k][int(enc)][i - 1] = [sig, encoder, 90 + 00 - channel_angle]  # (rho, theta, phi)
    return spherical_coordinate_array

def get_spherical_coordinate(img_array_depth, line_list):
    '''
    This function get access to the lines in the myFormat file and extract the information related to the encoder,
    to the frame, and to the signal
    :param file: myFormat file name
    :param mode: 512, 1021, 2048
    :param signal_name: string; which signal you are looking after;
    :return: img_array: full, a 3 dimensional array:
    total number of frames x (512 or 256 depending on the mode) x 16 channels
    '''

    spherical_coordinate_array = np.zeros((img_array_depth+1, int(mode / 4) , 16), dtype=list)
    # this is the array the contains all the pixels acquired by the sensor
    m, i, j, k, l = 0, 0, 0, 0, 0

    enc_min = smallest_encoder_tick(line_list)
    framelist = frame_list(line_list)[0]

    for k in range(0, img_array_depth+1):
        for j in range(0, int(mode / 4) ):
            for i in range(0, 18):
                if l % 18 == 0:
                    encoder_count = ['0']
                    s = 0
                    for c in line_list[l]:
                        if s == 5 and (c != ' ' or c != '\n'):  # s=3 encoder don't touch!
                            encoder_count.append(c)
                        if c == ' ':
                            s += 1
                        if s == 6:  # s=4 encoder don't touch!
                            break
                    enc = ''
                    enc = (int(enc.join(encoder_count)) - enc_min) / (44 * (2048 / mode))
                    real_frame = first_last_frame_number(line_list[l])  # add
                else:
                    if (l + 1) % 18 != 0:
                        channel_angle = 14.8-(i)*2.006
                        # img_array = signal_data(signal_name, l, linelist, img_array, k, enc, i)
                        spherical_coordinate_array = spherical_coordinate_data(l, line_list, spherical_coordinate_array,
                                                                          real_frame - framelist, enc, i, channel_angle)

                l += 1
                if l >= len(line_list):
                    break
            if l >= len(line_list):
                break
        if l >= len(line_list):
            break
    return spherical_coordinate_array


def spherical_to_cartesian (spherical_coordinate_array, Lidar_direction, height):
    '''

    :param spherical_coordinate_array:
    :param Lidar_direction: angle in degree between the lidar and the ground (54)
    :param height: the heigt of the lidar abobe the ground
    :return: cartezian (xyz) spherical array and the z channel
    '''
    cartesian_coordinate_array = np.zeros ((spherical_coordinate_array.shape[0], spherical_coordinate_array.shape[1],
                         spherical_coordinate_array.shape[2]), dtype= list)
    z_array = np.zeros ((spherical_coordinate_array.shape[0], spherical_coordinate_array.shape[1],
                         spherical_coordinate_array.shape[2]))

    for i in range(0, spherical_coordinate_array.shape[0]):
        for j in range(0, spherical_coordinate_array.shape[1]):
            for k in range(0, spherical_coordinate_array.shape[2]):
                if str(type(spherical_coordinate_array[i][j][k])) == "<class 'list'>":

                    rho = spherical_coordinate_array[i][j][k][0]
                    theta = math.radians(spherical_coordinate_array[i][j][k][1])
                    phi = math.radians(spherical_coordinate_array[i][j][k][2])
                    print (spherical_coordinate_array[i][j][k][2])
                    x = rho * math.sin(phi) * math.cos(theta)
                    y = rho * math.sin(phi) * math.sin(theta)
                    z = rho * math.cos(phi)
                    u = math.cos(math.radians(-Lidar_direction)) * x + math.sin(math.radians(-Lidar_direction)) * z
                    v = y
                    w = -math.sin(math.radians(-Lidar_direction)) * x + math.cos(math.radians(-Lidar_direction)) * z + height
                    cartesian_coordinate_array[i][j][k] = [u, v, w]
                    z_array[i][j][k] = w
                else:
                    cartesian_coordinate_array[i][j][k] = [0, 0, 0]

    return cartesian_coordinate_array, z_array


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
        #cv2.waitKey(0)


def crop_image (output_size = 640):
    '''
    this function take an image and crop it equally to multiple images according to its output_size
    :param input_size:
    :return:
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
        img = cv2.imread(filename)
        for i in range(0, 3):
            crop_img = img[0: img.shape[0], output_size * i : output_size * i + output_size]
            crop_img_resize = cv2.resize(crop_img, (output_size, output_size), interpolation=cv2.INTER_AREA)
            path = '/media/nizar/Transcend/cocosynth/datasets/pavement_distress_synthetic/input/backgrounds/images_crp'
            filename_crp = str(i) + '_' + filename
            cv2.imwrite(os.path.join(path, filename_crp), crop_img_resize)


def hypebola_reference ():
    '''

    :return: points reference
    '''
    from mpl_toolkits.mplot3d import Axes3D
    import math as m
    sensor_direction = 53  # in degree
    channel_angle = [14.8, 12.79, 10.78, 8.78, 6.77, 4.77, 2.76, 0.75,
                     -1.25, -3.26, -5.27, -7.27, -9.28, -11.29, -13.29, -15.3]
    mode = 2048
    phi = m.radians(sensor_direction)  # sensor direction in radian
    d = 1610  # distance in millimeter: sensor to the ground
    t_list = []
    x_list = []
    y_list = []
    z_list = []
    theta_list = []
    for i in range(0, int(mode / 4 )):
        theta = (-90 / ((mode / 4) )) * i + 225
        # print (theta)
        # theta_list.append(theta)
        theta = m.radians(theta)
        # print(i)
        for delta in channel_angle:
            delta = m.radians(delta)
            t = (m.cos(delta) * m.cos(theta) * (-d / m.cos(phi) / m.sin(delta))) / (
                    1 - (-m.tan(phi) * m.cos(delta) * m.cos(theta) / m.sin(delta)))
            x = t
            if theta > 3.14159:
                y = m.sqrt(abs(((t * -m.tan(phi) - d / m.cos(phi)) ** 2) / m.tan(delta) ** 2 - t ** 2))
                # print('>180')
                # print (theta)
            else:
                y = -m.sqrt(abs(((t * -m.tan(phi) - d / m.cos(phi)) ** 2) / m.tan(delta) ** 2 - t ** 2))
                # print('<180')
                # print (theta)
            z = -m.tan(phi) * t - d / m.cos(phi)
            # ---------------rotation------------- #
            u = m.cos(-m.radians(53)) * x + m.sin(-m.radians(53)) * z
            v = y
            w = -m.sin(-m.radians(53)) * x + m.cos(-m.radians(53)) * z - 0
            t_list.append(t)
            x_list.append(u)
            y_list.append(v)
            z_list.append(w)
    # plt.figure()
    # ax = plt.axes(projection='3d')
    # ax.scatter3D(x_list, y_list, z_list, cmap='Greens')
    return x_list, y_list, z_list