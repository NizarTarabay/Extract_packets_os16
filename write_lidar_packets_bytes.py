import socket
import time
import struct
import keyboard
import os
import datetime

UDP_IP = '10.5.5.1'
UDP_port = 7502

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_port))

# Create target Directory if don't exist
save_directory = "/media/nizar/Transcend/test in the lab/Data/Bytes/Lidar"
if not os.path.exists(save_directory):
    os.mkdir(save_directory)
    print("Directory ", save_directory, " Created ")
else:
    print("Directory ", save_directory, " already exists")
os.chdir(save_directory)

now = datetime.datetime.now()
T = now.strftime("%Y-%m-%d %H:%M:%d")

file_name = 'Lidar_byte_packet_' + T + '.txt'
f = open(file_name, 'wb')
j = 0
running = True
start1 = time.time()
while running:
    data = sock.recv(12608)
    start2 = time.time()

    if int(struct.unpack('I', data[12:16])[0]) in range(33704, 56408): #range (33792 , 56320) ### data[12 + 197 * 4 * 0:16 + 197 * 4 * 0])[0]
	#end = time.time()
        #elapse = end - start
        #print (elapse)
        for i in range(0, 16):

            f.write(data[8 + 788 * i: 16 + 788 * i])  # Frame ID data[(2*4+2) + 197 * 4 * i: (2*4+2 + 2) + 197 * 4 * i]

            for j in range(0, 16):

                f.write(data[(40 + 48*j + 788 * i):
                             (50 + 48*j + 788 * i)] )  # Range_mm_channel data[(((10+(4*3*j))*4) + 197 * 4 * i):
                                                                   #                       (((10+(4*3*j))*4+4) + 197 * 4 * i)
        #print('catcha')
        #data = sock.recv(12608)

    if keyboard.is_pressed('q'):
        running = False
    end2 = time.time()
    elapse2 = end2 - start2
    print (elapse2)

end1 = time.time()
elapse1 = end1 - start1
sock.close()
print('Socket is closed!')
f.close()
print('\nFile is closed!\n')
print('time: ', elapse1)
