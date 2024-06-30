import torch

# Load YOLOv5s model from .pt file
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt')

# Set the model to evaluation mode
model.eval()
