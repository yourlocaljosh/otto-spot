import cv2
import numpy as np
import time

# Spot detection parameters
STUCK_THRESHOLD = 3.0
BOTTOM_ZONE_THRESHOLD = 0.75
CLEAR_ZONE_THRESHOLD = 0.40

class SpotDetector:
    def __init__(self, frame_height):
        self.frame_height = frame_height
        self.stuck_start_time = None
        self.last_y = None
        self.positions = []
        self.assist_triggered = False
        
    def is_stuck(self, y_pos):
        if y_pos is None:
            self.stuck_start_time = None
            return self.assist_triggered
        
        # Track position history
        self.positions.append(y_pos)
        if len(self.positions) > 10:
            self.positions.pop(0)
        
        # Check if in bottom zone (higher Y = lower on screen)
        bottom_zone_y = self.frame_height * BOTTOM_ZONE_THRESHOLD
        in_bottom_zone = y_pos > bottom_zone_y
        
        if len(self.positions) >= 5:
            position_variance = np.std(self.positions[-5:])
            is_stationary = position_variance < 20
        else:
            is_stationary = False
        
        if in_bottom_zone and is_stationary:
            if self.stuck_start_time is None:
                self.stuck_start_time = time.time()
            
            stuck_duration = time.time() - self.stuck_start_time
            
            if stuck_duration >= STUCK_THRESHOLD:
                self.assist_triggered = True
                return True
        else:
            self.stuck_start_time = None
        
        return self.assist_triggered
    
    def is_clear(self, y_pos):
        if y_pos is None:
            return False
        
        clear_zone_y = self.frame_height * CLEAR_ZONE_THRESHOLD
        return y_pos < clear_zone_y
    
    def clear_assist(self):
        self.assist_triggered = False
        self.stuck_start_time = None
    
    def get_stuck_duration(self):
        if self.stuck_start_time is None:
            return 0
        return time.time() - self.stuck_start_time