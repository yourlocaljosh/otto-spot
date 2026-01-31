import cv2
import numpy as np

# Barbell color marking
LOWER_MARKER = np.array([93, 56, 88])
UPPER_MARKER = np.array([127, 255, 255])

def detect_barbell_markers(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_MARKER, UPPER_MARKER)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, 
                                    cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) >= 2:
        valid_contours = [c for c in contours if cv2.contourArea(c) > 200]
        
        if len(valid_contours) >= 2:
            sorted_contours = sorted(valid_contours, key=cv2.contourArea, reverse=True)
            marker1 = sorted_contours[0]
            marker2 = sorted_contours[1]
            
            M1 = cv2.moments(marker1)
            M2 = cv2.moments(marker2)
            
            if M1["m00"] > 0 and M2["m00"] > 0:
                cx1 = int(M1["m10"] / M1["m00"])
                cy1 = int(M1["m01"] / M1["m00"])
                cx2 = int(M2["m10"] / M2["m00"])
                cy2 = int(M2["m01"] / M2["m00"])
                
                cv2.circle(frame, (cx1, cy1), 10, (0, 255, 0), -1)
                cv2.circle(frame, (cx2, cy2), 10, (0, 255, 0), -1)
                
                cv2.line(frame, (cx1, cy1), (cx2, cy2), (0, 255, 0), 3)
                
                center_y = (cy1 + cy2) // 2
                
                cv2.line(frame, (0, center_y), (frame.shape[1], center_y), 
                        (255, 0, 0), 2)
                
                distance = np.sqrt((cx2 - cx1)**2 + (cy2 - cy1)**2)
                
                return center_y, distance, (cx1, cy1, cx2, cy2)
    
    return None, None, None

# Main loop
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    y_pos, distance, coords = detect_barbell_markers(frame)
    
    if y_pos is not None:
        cv2.putText(frame, f"Barbell Y: {y_pos}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Detected length:{int(distance)}px", (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No market detected", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.imshow('Barbell Detector', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()