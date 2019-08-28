import socket
import time
import struct
import keyboard
# UDP_IP = '10.5.5.1'
# UDP_port = 7503
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#
# sock.bind((UDP_IP, UDP_port))
#
# while True:
#     data, addr = sock.recvfrom(UDP_port)
#     # print('received msg:', data )
#     print (struct.unpack('3Q6f', data))


UDP_IP = '10.5.5.1'
UDP_port = 7502

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_port))
f = open("entire_packet_bytes_(if_on_each_azimuth_block).txt", 'wb')
j = 0
running = True
start = time.time()
while running:
    data = sock.recv(12608)
    while int(struct.unpack('I', data[12 + 197 * 4 * 0:16 + 197 * 4 * 0])[0]) in range(33704, 56408): #range (33792 , 56320)
        for i in range(0, 16):
            print('Frame ID: ' + str(struct.unpack('H', data[(2 * 4 + 2) + 197 * 4 * i: (2 * 4 + 2 + 2) + 197 * 4 * i])[0]))

            f.write(data[(2*4+2) + 197 * 4 * i: (2*4+2 + 2) + 197 * 4 * i])  # Frame ID

            f.write(data[(2*4) + 197 * 4 * i: (2*4 + 2) + 197 * 4 * i])  # Measurement ID

            f.write(data[(3*4) + 197 * 4 * i: (3*4 + 4) + 197 * 4 * i])  # Encoder Count

            for j in range(0, 16):

                f.write(data[(((10+(4*3*j))*4) + 197 * 4 * i):
                             (((10+(4*3*j))*4+4) + 197 * 4 * i)])  # Range_mm_channel
            #
                f.write(data[(((11+(4*3*j))*4) + 197 * 4 * i):
                             ((((11+(4*3*j))*4)+2) + 197 * 4 * i)]) # Reflectivity_channel
            #
                f.write(data[(((11+(4*3*j))*4+2) + 197 * 4 * i):
                             ((((11+(4*3*j))*4+2)+2) + 197 * 4 * i)]) # Signal_photons
            #                                                                    
                f.write(data[(((12+(4*3*j))*4+2) + 197 * 4 * i):
                             ((((12+(4*3*j))*4+2)+2) + 197 * 4 * i)]) # Noise_photons

        data = sock.recv(12608)

    if keyboard.is_pressed('q'):
        running = False
end = time.time()
elapse = end - start
sock.close()
print('Socket is closed!')
sock.close()
f.close()
print('\nFile is closed!\n')
print('time: ', elapse)

