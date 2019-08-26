import socket
import struct

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
# sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,12607)
# while True:
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 12607)
#     data, addr = sock.recvfrom(UDP_port)
#     # print('receiadved msg:', data )
#     print (struct.unpack('Q2HILHHHH', data[0:32])) # Q for the time stamp, 2H for Measurement ID and Frame ID, I for the encoder count
#     # print (struct.unpack_from('I', data[33:37]))

f = open("entire_packet.txt",'w')
while True:

    data = sock.recv(12608)
    while int(struct.unpack('I', data[12 + 197 * 4 * 15:16 + 197 * 4 * 15])[0]) in range (33792 , 56320):
        # print(struct.unpack('H', data[10 + 197 * 4 * 15:12 + 197 * 4 * 15]),
        #      struct.unpack('H', data[8 + 197 * 4 * 15:10 + 197 * 4 * 15]),
        #      struct.unpack('I', data[12 + 197 * 4 * 15:16 + 197 * 4 * 15])) #Frame ID, Mesurement ID, Encoder count
        # print(struct.unpack('Q', data[
        #                                  0:8]))  # Q for the time stamp, 2H for Measurement ID and Frame ID, I for the encoder count
        for i in range(0, 16):
            # f.write('Frame ID: ' + str(struct.unpack('H', data[(2*4+2) + 197 * 4 * i:
            #                                                     (2*4+2+2) + 197 * 4 * i])[0]) + ' ')
            print('Frame ID: ' + str(struct.unpack('H', data[(2 * 4 + 2) + 197 * 4 * i:
                                                               (2 * 4 + 2 + 2) + 197 * 4 * i])[0]) + ' ')
            f.write('F ' + str(struct.unpack('H', data[(2 * 4 + 2) + 197 * 4 * i:
                                                               (2 * 4 + 2 + 2) + 197 * 4 * i])[0]) + ' ') # Frame ID
            f.write(str(struct.unpack('H', data[(2*4) + 197 * 4 * i:
                                                                    (2*4+2) + 197 * 4 * i])[0]) + ' ') # Measurement ID
            f.write(str(struct.unpack('I', data[(3*4) + 197 * 4 * i:
                                                                     (3*4+4) + 197 * 4 * i])[0]) + '\n') # Encoder Count
            for j in range(0, 16):
                f.write(str(struct.unpack('I', data[(((10+(4*3*j))*4) + 197 * 4 * i):
                                                                                        (((10+(4*3*j))*4+4) + 197 * 4 * i)])[0]) + ' ') # Range_mm_channel
            #
                f.write(str(struct.unpack('H', data[(((11+(4*3*j))*4) + 197 * 4 * i):
                                                                                            ((((11+(4*3*j))*4)+2) + 197 * 4 * i)])[0]) + ' ') # Reflectivity_channel
            #
                f.write(str(struct.unpack('H', data[(((11+(4*3*j))*4+2) + 197 * 4 * i):
                                                                                      ((((11+(4*3*j))*4+2)+2) + 197 * 4 * i)])[0]) + ' ') # Signal_photons
            #
                f.write(str(struct.unpack('H', data[(((12+(4*3*j))*4+2) + 197 * 4 * i):
                                                                                     ((((12+(4*3*j))*4+2)+2) + 197 * 4 * i)])[0]) + '\n') # Noise_photons

        data = sock.recv(12608)
