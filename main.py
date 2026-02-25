from ultralytics import YOLO
import cv2

# model = YOLO("yolov8n.pt") # build model

model = YOLO("runs/detect/train4/weights/best.pt") # trained model

# results = model.train(data="config.yaml", epochs=20) # train model


# Open the webcam (0 = default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Run detection on the frame
    results = model(frame, conf=0.5)  # adjust confidence threshold as needed

    # YOLOv8 returns results.render() as a list of images with boxes drawn
    annotated_frame = results[0].plot()  # draw boxes and labels on frame

    # Show the annotated frame
    cv2.imshow("YOLOv8 Live Detection", annotated_frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()