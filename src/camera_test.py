import cv2
import numpy as np

def pick_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        pixel_hsv = hsv[y, x]
        print(f"Coords: ({x}, {y})")
        print(f"HSV: {pixel_hsv}")
        print(f"H: {pixel_hsv[0]}, S: {pixel_hsv[1]}, V: {pixel_hsv[2]}")
        print(f"range:")
        print(f"lower_red = np.array([{max(0, pixel_hsv[0]-10)}, {max(50, pixel_hsv[1]-50)}, {max(50, pixel_hsv[2]-50)}])")
        print(f"upper_red = np.array([{min(180, pixel_hsv[0]+10)}, 255, 255])")

cap = cv2.VideoCapture(0)
cv2.namedWindow('HSV get color')
cv2.setMouseCallback('hsv getcolor', pick_color)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imshow('Color', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()