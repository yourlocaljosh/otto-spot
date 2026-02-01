import cv2
import sys
sys.path.append('src')

from barbell import detect_barbell_markers
from spot_detection import SpotDetector, BOTTOM_ZONE_THRESHOLD, CLEAR_ZONE_THRESHOLD
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
rep_count = 0
best_set = 0
in_rep_zone = False
rep_completed = False

print("Otto Spot - Running")
print(f"Frame height: {frame_height}")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        bottom_zone_y = int(frame_height * BOTTOM_ZONE_THRESHOLD)
        clear_zone_y = int(frame_height * CLEAR_ZONE_THRESHOLD)

        cv2.line(frame, (0, bottom_zone_y), (frame.shape[1], bottom_zone_y), 
                (0, 255, 255), 3)
        cv2.putText(frame, "Rep threshold", (10, bottom_zone_y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        cv2.line(frame, (0, clear_zone_y), (frame.shape[1], clear_zone_y), 
                (0, 255, 0), 3)
        cv2.putText(frame, "Termination threshold", (10, clear_zone_y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        y_pos, distance, coords = detect_barbell_markers(frame)
        
        assist_needed = spot_detector.is_stuck(y_pos)
        is_clear = spot_detector.is_clear(y_pos)
        stuck_duration = spot_detector.get_stuck_duration()

        if y_pos is not None:
            if y_pos > bottom_zone_y and not in_rep_zone:
                in_rep_zone = True
                rep_completed = False
            
            if in_rep_zone and not rep_completed and is_clear:
                rep_count += 1
                rep_completed = True
                
                # Check if target reached
                if rep_count >= best_set:
                    best_set = rep_count
            
            if y_pos < clear_zone_y:
                in_rep_zone = False


        if assist_needed and not assist_active:
            print("Spot triggered")
            teensy.spot_trigger()
            assist_active = True
        
        elif assist_active and is_clear:
            print("Termination triggered")
            teensy.spot_terminate()
            spot_detector.clear_assist()
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
            
        rep_text = f"Reps: {rep_count} Best Set: {best_set}"
        text_size = cv2.getTextSize(rep_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
        text_x = frame.shape[1] - text_size[0] - 20
        
        # Background box for rep counter
        cv2.rectangle(frame, (text_x - 10, 10), 
                     (frame.shape[1] - 10, 70), (0, 0, 0), -1)
        
        rep_color = (0, 215, 255)
        cv2.putText(frame, rep_text, (text_x, 50),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.5, rep_color, 3)
        
        if assist_needed:
            cv2.putText(frame, "Spot Active", (10, 200),
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