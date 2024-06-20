from ultralytics import YOLO

model = YOLO("/home/soumyajit-das/Desktop/pdf-check-algorithm/YOLO MODELS/Page Detection/best.pt")
k = model.predict("86.jpg", save = True)
bounding_box = []
for result in k:
    for box in result.boxes:
        bounding_box.append(box.xyxy.tolist())
print(bounding_box)