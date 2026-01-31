import cv2
import numpy as np

frame = None
samples = []

def pick_color(event, x, y, flags, param):
    global frame, samples

    if event == cv2.EVENT_LBUTTONDOWN and frame is not None:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        pixel_hsv = hsv[y, x]
        samples.append(pixel_hsv)
        
        print(f"\#{len(samples)} at ({x}, {y})")
        print(f" H={pixel_hsv[0]}, S={pixel_hsv[1]}, V={pixel_hsv[2]}")
        
        if len(samples) >= 10:
            samples_array = np.array(samples)
            avg_h = int(np.mean(samples_array[:, 0]))
            avg_s = int(np.mean(samples_array[:, 1]))
            avg_v = int(np.mean(samples_array[:, 2]))
            
            min_h = int(np.min(samples_array[:, 0]))
            max_h = int(np.max(samples_array[:, 0]))
            
            print(f"Cumulative #{len(samples)}")
            print(f"AVG: H={avg_h}, S={avg_s}, V={avg_v}")
            print(f"{min_h} to {max_h}")
            print(f"lower = np.array([{max(0, min_h-15)}, {max(30, avg_s-80)}, {max(30, avg_v-80)}])")
            print(f"upper = np.array([{min(180, max_h+15)}, 255, 255])\n")

cap = cv2.VideoCapture(0)

WINDOW_NAME = 'HSV Color Picker'
cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, pick_color)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.putText(frame, f"Samples: {len(samples)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow(WINDOW_NAME, frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        samples = []
        print("\nSamples reset")

cap.release()
cv2.destroyAllWindows()