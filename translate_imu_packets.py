#---------------------------------- READ FROM A IMU BINARY FILE AND WRITE IN A HUMAN READBLE FORMAT ----------------------------------#
import time
import struct
import os

# Create target Directory if don't exist
save_directory = "/media/nizar/Transcend/test in the lab/Data/myFormat/IMU"

if not os.path.exists(save_directory):
    os.mkdir(save_directory)
    print("Directory ", save_directory, " Created ")
else:
    print("Directory ", save_directory, " already exists")

os.chdir('/media/nizar/Transcend/test in the lab/Data/Bytes/IMU')

file_name_t = input("Time and date:")
file_name = 'IMU_byte_packet_' + str(file_name_t) + '.txt'
f = open('IMU_byte_packet_' + file_name_t + '.txt', 'rb')

os.chdir('/media/nizar/Transcend/test in the lab/Data/myFormat/IMU')
f_write = open('IMU_myFormat_packet_' + file_name_t + '.txt', 'w')

f_read = f.read()
start = time.time()
j = 0
for i in range(0, 2419):
    f_write.write('IMU_T: '  + str(struct.unpack('Q', f_read[j:j+8])[0]) + ' ')  # IMU read time
    f_write.write('Acc_T: '  + str(struct.unpack('Q', f_read[j+8:j+16])[0]) + ' ')  # Accelerometer read time
    f_write.write('Gyro_T: ' + str(struct.unpack('Q', f_read[j+16:j+24])[0]) + '\n')  # Gyroscope read time
    f_write.write('acc_x: '  + str(struct.unpack('f', f_read[j+24:j+28])[0]) + ' ')  # Acceleration in x-axis (g)
    f_write.write('acc_y: '  + str(struct.unpack('f', f_read[j+28:j+32])[0]) + ' ')  # Acceleration in y-axis (g)
    f_write.write('acc_z: '  + str(struct.unpack('f', f_read[j+32:j+36])[0]) + ' ')  # Acceleration in z-axis (g)
    f_write.write('angV_x: ' + str(struct.unpack('f', f_read[j+36:j+40])[0]) + ' ')  # Angular velocity in x-axis
    f_write.write('angV_y: ' + str(struct.unpack('f', f_read[j+40:j+44])[0]) + ' ')  # Angular velocity in y-axis
    f_write.write('angV_z: ' + str(struct.unpack('f', f_read[j+44:j+48])[0]) + '\n')  # Angular velocity in z-axis

end = time.time()
elapse = end - start
f.close()
f_write.close()
print('\nFiles are closed!\n')
print('time: ', elapse)
