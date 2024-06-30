import os

# Define folder path
folder_path = "PlantDoc-Object-Detection-Dataset-master/TRAIN"

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an XML file
    if filename.endswith(".xml"):
        # Delete the file
        os.remove(os.path.join(folder_path, filename))
