import socket
import time
import keyboard
import os
import datetime
UDP_IP = '10.5.5.1'
UDP_port_IMU = 7503
#
sock_IMU = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
sock_IMU.bind((UDP_IP, UDP_port_IMU))
#

# Create target Directory if don't exist
save_directory = "/media/nizar/Transcend/test in the lab/Data/Bytes/IMU"
if not os.path.exists(save_directory):
    os.mkdir(save_directory)
    print("Directory ", save_directory, " Created ")
else:
    print("Directory ", save_directory, " already exists")
os.chdir(save_directory)

now = datetime.datetime.now()
T = now.strftime("%Y-%m-%d %H:%M:%d")

file_name = 'IMU_byte_packet_' + T + '.txt'


IMU_file = open(file_name, 'wb')
j=0
running = True
start = time.time()
while running:
    IMU_data = sock_IMU.recvfrom(UDP_port_IMU)
    IMU_file.write(IMU_data[0: 48][0])  # IMU packet
    print('iswriting dont bother:)')
    if keyboard.is_pressed('q'):
        running = False

end = time.time()
elapse = end - start
sock_IMU.close()
print('Sockets are closed!')
IMU_file.close()
print('\nFiles are closed!\n')
print('time: ', elapse)

