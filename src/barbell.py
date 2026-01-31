import cv2
import numpy as np

# Barbell color marking
LOWER_MARKER = np.array([100, 100, 100])
UPPER_MARKER = np.array([130, 255, 255])

def detect_barbell_marker(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, LOWER_MARKER, UPPER_MARKER)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, 
                                    cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest = max(contours, key=cv2.contourArea)
        
        if cv2.contourArea(largest) > 100:
            x, y, w, h = cv2.boundingRect(largest)
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            center_y = y + h // 2
            
            #Draw line at barbell
            cv2.line(frame, (0, center_y), (frame.shape[1], center_y), 
                    (0, 255, 0), 1)
            
            return center_y
    
    return None

# Main loop
cap = cv2.VideoCapture(0)

print("Barbell Detection")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    y_pos = detect_barbell_marker(frame)
    
    if y_pos is not None:
        cv2.putText(frame, f"Barbell Y: {y_pos}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No marker detected", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imshow('Barbell Detector', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()