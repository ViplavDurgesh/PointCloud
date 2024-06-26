import cv2
import numpy as np
import os
import open3d as o3d
import matplotlib.pyplot as plt


import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np

# Load color and depth images

color_raw = o3d.io.read_image('Color_input_image')
depth_raw = o3d.io.read_image('Depth_input_image')

# Create RGBD image from color and depth images

rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw,convert_rgb_to_intensity=False)

# Display grayscale image and depth image

plt.subplot(1, 2, 1)
plt.title('RGB image')
plt.imshow(rgbd_image.color)
plt.subplot(1, 2, 2)
plt.title('Depth image')
plt.imshow(rgbd_image.depth)
plt.show()

# Intrinsic parameters

int = np.load('camera1_calibration.npz')
intrinsic_matrix = int['mtx']

# Create PinholeCameraIntrinsic object

intrinsic = o3d.camera.PinholeCameraIntrinsic(640, 480, intrinsic_matrix[0, 0], intrinsic_matrix[1, 1],
                                               intrinsic_matrix[0, 2], intrinsic_matrix[1, 2])

# Create point cloud from RGBD image

pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, intrinsic)

# Flip it, otherwise the point cloud will be upside down

pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
# Define the distance threshold (1 meter)
distance_threshold = .6

# Calculate the distances from the origin to each point

distances = np.linalg.norm(np.asarray(pcd.points), axis=1)

# Filter points based on the distance threshold

filtered_indices = np.where(distances < distance_threshold)[0]
cropped_point_cloud = pcd.select_by_index(filtered_indices)

# Visualize the point cloud

o3d.visualization.draw_geometries([cropped_point_cloud])
