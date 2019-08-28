import socket
import time
import keyboard
UDP_IP = '10.5.5.1'
UDP_port_IMU = 7503
#
sock_IMU = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
sock_IMU.bind((UDP_IP, UDP_port_IMU))
#

IMU_file = open('IMU_packet_bytes.txt', 'wb')
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

