dataset_folder_name = r'pokemon-card-images' # Name of dataset folder that will be created
# pathToData = r'C:\Users\maxsc\Downloads\pokemon-card-kaggle-data' # Path to raw dataset
pathToData = r'C:\Users\maxsc\Downloads\pokemon-card-test-data' # Path to raw dataset
image_file_extension = ".jpg" # file extension of generated images for dataset

from create_image_data_functions import create_image_data_functions

import os
import cv2

# Add image to dataset function\

def add_image_to_dataset(cv2Image, imageObj, img_name_extension):
    image_name = imageObj['name'] + "_" + img_name_extension
    class_index = imageObj['index']

    # Create image files in folders

    cv2.imwrite(dataset_folder_name + "/images/train/" + image_name + image_file_extension, cv2Image) # train folder
    cv2.imwrite(dataset_folder_name + "/images/val/" + image_name + image_file_extension, cv2Image) # val folder

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

# Get array of images

images = []

directory = os.fsencode(pathToData)
    
for folder in os.listdir(directory):
    folder_name = os.fsdecode(folder)
    for file in os.listdir(os.fsencode(pathToData + "\\" + folder_name)):
        fileName = os.fsdecode(file)
        className = fileName[::-1]
        className = className.split(".", 1)
        if len(className) > 0:
            className = className[1]
        else:
            continue
        className = className[::-1]
        images.append({
            "index": len(images),
            "name": className,
            "path": pathToData + "\\" + folder_name + "\\" + fileName
        })

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

for imageObj in images:
    baseImage = cv2.imread(imageObj['path'])

    # Add unmodified image to dataset
    add_image_to_dataset(baseImage, imageObj, "")

    # Modify image and add it to dataset
    for i, img_mod_function in enumerate(create_image_data_functions):
        add_image_to_dataset(
            img_mod_function(baseImage), # Send image
            imageObj, # Send image object information to categorize data
            str(i) # Send modification type to categorize data
        )