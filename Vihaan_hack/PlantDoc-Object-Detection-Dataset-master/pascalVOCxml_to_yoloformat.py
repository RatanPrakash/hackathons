import os
import xml.etree.ElementTree as ET

# Define class names and corresponding IDs
classes = {"leaves": 0}

# Define function to convert bounding box coordinates to YOLO format
def convert_coordinates(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

path = "PlantDoc-Object-Detection-Dataset-master/TRAIN"
# Loop through all XML files in the folder
for filename in os.listdir(path):
    if filename.endswith(".xml"):
        # Parse XML file
        tree = ET.parse(os.path.join(path, filename))
        root = tree.getroot()
        
        # Get image size
        size = root.find("size")
        width = int(size.find("width").text)
        height = int(size.find("height").text)
        
        # Create YOLO text file
        yolo_filename = filename[:-4] + ".txt"
        with open(os.path.join(path, yolo_filename), "w") as f:
            # Loop through all objects in the XML file
            for obj in root.findall("object"):
                # Get object name and bounding box coordinates
                name = obj.find("name").text
                bbox = obj.find("bndbox")
                xmin = int(bbox.find("xmin").text)
                xmax = int(bbox.find("xmax").text)
                ymin = int(bbox.find("ymin").text)
                ymax = int(bbox.find("ymax").text)
                
                # Convert bounding box coordinates to YOLO format
                box = (xmin, xmax, ymin, ymax)
                try:
                    yolo_box = convert_coordinates((width,height), box)
                except:
                    pass
                # Write YOLO text file line
                class_id = 0
                line = f"{class_id} {yolo_box[0]} {yolo_box[1]} {yolo_box[2]} {yolo_box[3]}\n"
                f.write(line)
                print(yolo_filename, " done")
