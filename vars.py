import cv2
import os

dataset_folder_name = r'pokemon-card-images' # Name of dataset folder that will be created
path_to_data = r'C:\Users\maxsc\Downloads\pokemon-card-test-data' # Path to raw dataset
background_images_path = os.path.dirname(os.path.realpath(__file__)) + "\\" + "backgrounds"

# Information to use to overlay images from data onto backgrounds to create training data

img_overlay_data = [
    {
        'background_img': cv2.imread(background_images_path + "\\antique_desk.jpg"),
        'new_width': 80,
        'new_height': 100,
        'x_offset': 435,
        'y_offset': 410,
        'warp_type': 'clockwise'
    }
]