import cv2
import sys
sys.path.append('src')

from barbell import detect_barbell_markers
from spot_detection import SpotDetector, BOTTOM_ZONE_THRESHOLD
from teensy_comm import TeensyController

cap = cv2.VideoCapture(0)

ret, test_frame = cap.read()
if not ret:
    print("Error: Cannot open camera")
    exit()

frame_height = test_frame.shape[0]
spot_detector = SpotDetector(frame_height)

teensy = TeensyController()

assist_active = False

print("Otto Spot - Running")
print(f"Frame height: {frame_height}")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        bottom_zone_y = int(frame_height * BOTTOM_ZONE_THRESHOLD)
        cv2.line(frame, (0, bottom_zone_y), (frame.shape[1], bottom_zone_y), 
                (0, 255, 255), 3)
        cv2.putText(frame, "Rep area", (10, bottom_zone_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        y_pos, distance, coords = detect_barbell_markers(frame)
        
        assist_needed = spot_detector.is_stuck(y_pos)
        stuck_duration = spot_detector.get_stuck_duration()

        if assist_needed and not assist_active:
            #Send spot trigger to Teensy
            print("Spot triggered")
            teensy.spot_trigger()
            assist_active = True
        elif not assist_needed and assist_active:
            print("Spot in progress")
            #Send stop to Teensy
            teensy.spot_terminate()
            assist_active = False
        
        # Display barbell info
        if y_pos is not None:
            cv2.putText(frame, f"Barbell Y: {y_pos}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Length: {int(distance)}px", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Show stuck timer if counting
            if stuck_duration > 0:
                cv2.putText(frame, f"Stuck: {stuck_duration:.1f}s", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2)
        else:
            cv2.putText(frame, "No marker detected", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        if assist_needed:
            cv2.putText(frame, "Spot needed", (10, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
            
        status_color = (0, 255, 0) if teensy.connected else (0, 0, 255)
        status_text = "Teensy: Connected" if teensy.connected else "Teensy: DEMO MODE"
        cv2.putText(frame, status_text, (10, frame_height - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        cv2.imshow('Otto Spot', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nInterrupted by user")
finally:
    teensy.close()
    cap.release()
    cv2.destroyAllWindows()
    print("Terminated")