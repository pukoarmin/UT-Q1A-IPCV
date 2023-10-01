import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Clear workspace and close all figure windows
cv2.destroyAllWindows()

# Set the path to the folder containing your images
folder_path = 'original/'

# Create an imageSet object
image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
images = [cv2.imread(file) for file in image_files]


# # Initialize dictionary to store corresponding points
# corresponding_points = {}

# # Manually select corresponding points
# for n in range(4):
#     for m in range(n + 1, 4):
#         fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
#         ax1.imshow(images[n])
#         ax1.set_title(f'Image {n + 1}')
#         ax2.imshow(images[m])
#         ax2.set_title(f'Image {m + 1}')

#         # Use ginput to manually select corresponding points
#         points_n = np.array(plt.ginput(n=-1, timeout=0, show_clicks=True))
#         points_m = np.array(plt.ginput(n=-1, timeout=0, show_clicks=True))

#         # Store points in the dictionary
#         corresponding_points[(n + 1, m + 1)] = (points_n, points_m)

#         plt.close(fig)

# # Save the resulting dictionary on file for later reference
# np.save('corresponding_points.npy', corresponding_points)

# When loading the sets from file:
corresponding_points = np.load('corresponding_points.npy', allow_pickle=True).item()
print(corresponding_points)
#=== PART I ===
# Choose the set of corresponding points for stitching image 2 to image 1
points_image1 = corresponding_points[(1, 2)][0]
points_image2 = corresponding_points[(1, 2)][1]

# Convert points to numpy arrays
points_image1 = np.array(points_image1)
points_image2 = np.array(points_image2)
print(points_image1)
print(points_image2)

# Estimate homography matrix using the selected points
homography_matrix, _ = cv2.findHomography(points_image2, points_image1, cv2.RANSAC, 5.0)

# Get the size of image 1
height_image1, width_image1 = images[0].shape[:2]

# Warp image 2 to the domain of image 1
image2_warped = cv2.warpPerspective(images[1], homography_matrix, (width_image1, height_image1))

# Write the resulting image to file
cv2.imwrite('image2_warped_to_image1.jpg', cv2.cvtColor(image2_warped, cv2.COLOR_RGB2BGR))

# Display the warped image
plt.imshow(image2_warped)
plt.title('Image 2 Warped to Image 1')
plt.show()