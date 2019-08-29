#---------------------------------- READ FROM LIDAR BINARY FILE AND WRITE IN A HUMAN READBLE FORMAT ----------------------------------#
import time
import struct
import os


# Create target Directory if don't exist
save_directory = "/media/nizar/Transcend/test in the lab/Data/myFormat/Lidar"

if not os.path.exists(save_directory):
    os.mkdir(save_directory)
    print("Directory ", save_directory, " Created ")
else:
    print("Directory ", save_directory, " already exists")

os.chdir('/media/nizar/Transcend/test in the lab/Data/Bytes/Lidar')

file_name_t = input("Time and date:")
file_name = 'Lidar_byte_packet_' + str(file_name_t) + '.txt'
f = open('Lidar_byte_packet_' + file_name_t + '.txt', 'rb')

os.chdir('/media/nizar/Transcend/test in the lab/Data/myFormat/Lidar')
f_write = open('Lidar_myFormat_packet_' + file_name_t + '.txt', 'w')

f_read = f.read()

start = time.time()
for i in range(0, len(f_read)):
    if i % 168 == 0:  # 168 number of bytes in each packet 8+16*10
        f_write.write('F ' + str(struct.unpack('H', f_read[i+2:i+4])[0]) + ' ')  # Frame ID
        f_write.write(str(struct.unpack('H', f_read[i:i+2])[0]) + ' ')  # Measurement ID
        f_write.write(str(struct.unpack('I', f_read[i+4:i+8])[0]) + '\n')  # Encoder Count
        for j in range(0, 16):  # write the channel bytes
            f_write.write(str(struct.unpack('I', f_read[i+8 + j*10:
                                                        i+8 + j*10 + 4])[0]) + ' ')  # Range_mm_channel

            f_write.write(str(struct.unpack('H', f_read[i+8+4 + j*10:
                                                        i+8+4 + j*10 + 2])[0]) + ' ')  # Reflectivity_channel

            f_write.write(str(struct.unpack('H', f_read[i+8+4+2 + j*10:
                                                        i+8+4+2 + j*10 + 2])[0]) + ' ')  # Signal_photons

            f_write.write(str(struct.unpack('H', f_read[i+8+4+2+2 + j*10:
                                                        i+8+4+2+2 + j*10 + 2])[0]) + '\n')  # Noise_photons

end = time.time()
elapse = end - start
f.close()
f_write.close()
print('\nFiles are closed!\n')
print('time: ', elapse, ' s')
