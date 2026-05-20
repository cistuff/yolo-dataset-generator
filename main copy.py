from img_data_functions import image_functions, overlay_image
from vars import img_overlay_data, dataset_folder_name, path_to_data

import os
import cv2

images = [] # Array to store all images in data

# Add image to dataset function

def add_image_to_dataset(cv2Image, imageObj, img_name_extension):
    image_name = imageObj['name'] + "_" + img_name_extension
    class_index = imageObj['index']

    # Create image files in folders

    cv2.imwrite(dataset_folder_name + "/images/train/" + image_name + ".png", cv2Image) # train folder
    cv2.imwrite(dataset_folder_name + "/images/val/" + image_name + ".png", cv2Image) # val folder

    # Create labels in folders

    with open(labels_train_path + "\\" + image_name + ".txt", "w") as labels: # train folder
        labels.write(str(class_index) + " .5 .5 1.0 1.0")

    with open(labels_val_path + "\\" + image_name + ".txt", "w") as labels: # val folder
        labels.write(str(class_index) + " .5 .5 1.0 1.0")
        
# Create dataset folder

path = os.path.dirname(os.path.realpath(__file__))
dataset_path = path + "\\" + dataset_folder_name
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# Handle image when looping through raw data

def handle_image_file(file_path):
    class_name = file_path[::-1].split('\\', 1)[0].split('.', 1)[1][::-1]
    images.append({
        "index": len(images),
        "name": class_name,
        "path": file_path
    })

# Handle folder when looping through raw data

def handle_folder_file(parent_folder_path):
    parent_folder = os.fsencode(parent_folder_path)
    for file in os.listdir(parent_folder):
        file_path = os.fsdecode(parent_folder) + "\\" + os.fsdecode(file)

        if os.path.isdir(file_path):
            handle_folder_file(file_path)
        else:
            handle_image_file(file_path)

# Loop through folders with folders in it and add images from those folders to array of images

handle_folder_file(path_to_data)

# Create classes.txt

with open(dataset_path + "\\classes.txt", "w") as classes:
    for image in images:
        classes.write(image['name'] + '\n')

# Create images folder & subfolders

images_path = dataset_path + '\\' + 'images'
images_train_path = images_path + '\\' + 'train'
images_val_path = images_path + '\\' + 'val'

if not os.path.exists(images_path):
    os.makedirs(images_path)

if not os.path.exists(images_train_path):
    os.makedirs(images_train_path)

if not os.path.exists(images_val_path):
    os.makedirs(images_val_path)

# Create labels folder & subfolders

labels_path = dataset_path + '\\' + 'labels'
labels_train_path = labels_path + '\\' + 'train'
labels_val_path = labels_path + '\\' + 'val'

if not os.path.exists(labels_path):
    os.makedirs(labels_path)

if not os.path.exists(labels_train_path):
    os.makedirs(labels_train_path)

if not os.path.exists(labels_val_path):
    os.makedirs(labels_val_path)

# Generate test data

def handle_create_image_data(imageObj):
    total = 1
    base_img = cv2.imread(imageObj['path'])

    # Add unmodified image to dataset
    add_image_to_dataset(base_img, imageObj, str(total))
    total+=1

    # Apply all modifications to image and add image to dataset
    for img_mod_function in image_functions:
        add_image_to_dataset(
            img_mod_function(base_img), # Send image
            imageObj, # Send image object information to categorize data
            str(total) # Send modification type to categorize data
        )
        total+=1
    
    # Apply all warps to image and add image to dataset
    for overlay_data in img_overlay_data:
        overlay_image(base_img, overlay_data)
        add_image_to_dataset(
            overlay_image(base_img, overlay_data),
            imageObj,
            str(total)
        )
        total+=1

# for imageObj in images:
#     total = 1
#     base_img = cv2.imread(imageObj['path'])

#     # Add unmodified image to dataset
#     add_image_to_dataset(base_img, imageObj, str(total))
#     total+=1

#     # Apply all modifications to image and add image to dataset
#     for img_mod_function in image_functions:
#         add_image_to_dataset(
#             img_mod_function(base_img), # Send image
#             imageObj, # Send image object information to categorize data
#             str(total) # Send modification type to categorize data
#         )
#         total+=1
    
#     # Apply all warps to image and add image to dataset
#     for overlay_data in img_overlay_data:
#         overlay_image(base_img, overlay_data)
#         add_image_to_dataset(
#             overlay_image(base_img, overlay_data),
#             imageObj,
#             str(total)
#         )
#         total+=1