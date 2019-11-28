import os
import helpers
import matplotlib.pyplot as plt
import math as m
import numpy as np
import cv2

from mpl_toolkits.mplot3d import Axes3D


mode = 2048
fps = 10

os.chdir('/media/nizar/Transcend/test in the lab/Data/myFormat/Lidar/test_sanity/no_chess')
file_name_t = input("Time and date:")
file_name = 'Lidar_myFormat_packet_' + str(file_name_t) + '.txt'
img_array = helpers.get_signal(file_name, mode, 'range')
#
k, line_list = helpers.number_of_frames(file_name, mode)

spherical_coordinate_array = helpers.get_spherical_coordinate(k, line_list)
xyz, z = helpers.spherical_to_cartesian (spherical_coordinate_array, 53, 0000)
x = []
y = []
z = []
for elements in xyz[10][:][:]:
    for element in elements:
        # print (element, '\n')
        x.append(element[0])
        y.append(element[1])
        z.append(element[2])

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(x, y, z, c=z, cmap='Greens')

# fig = plt.figure()
# ax = fig.gca(projection='3d')
# ax.plot_trisurf(np.asarray(x), np.asarray(y), np.asarray(z))

#TODO: compute the error between the measured points and the real ones
x_ref = helpers.hypebola_reference()[0]
y_ref = helpers.hypebola_reference()[1]
z_ref = helpers.hypebola_reference()[2]

# plot the reference and the point cloud above each other
x_tot = x + x_ref
y_tot = y + y_ref
z_tot = z + z_ref

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(x_tot, y_tot, z_tot, cmap='Greens')

#-------------------element wise substraction ------------------------#

x_e = [(a_i - b_i) * (a_i - b_i) for a_i, b_i in zip(x, x_ref)]
y_e = [(a_i - b_i) * (a_i - b_i) for a_i, b_i in zip(y[::-1], y_ref)]
z_e = [(a_i - b_i) * (a_i - b_i) for a_i, b_i in zip(z, z_ref)]

xy_e = [(a_i + b_i) for a_i, b_i in zip(x_e, y_e)]
xyz_e = [(a_i + b_i) for a_i, b_i in zip(xy_e, z_e)]

mse = [m.sqrt(elmt) for elmt in xyz_e]
mse = np.reshape(mse, (512, 16)).T
# mse[mse > 1000] = 0

mse = cv2.resize(mse, (512,128))
fig = plt.figure('mse')
plt.imshow(mse)

z = np.reshape(z, (512, 16)).T

z = cv2.resize(z, (512,128))
fig = plt.figure('z')
plt.imshow(z)
