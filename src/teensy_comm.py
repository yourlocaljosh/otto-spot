import serial
import serial.tools.list_ports
import time

class TeensyController:
    def __init__(self, port=None, baudrate=9600):
        self.serial = None
        self.connected = False
        
        # auto detection
        if port is None:
            port = self._find_teensy()
        
        if port:
            try:
                self.serial = serial.Serial(port, baudrate, timeout=1)
                time.sleep(2)
                self.connected = True
                print(f"Connected to Teensy on {port}")
            except Exception as e:
                print(f"Failed to connect to Teensy: {e}")
                print("Running in no motor mode")
        else:
            print("No Teensy detected")
            print("Running in no motor mode")
    
    def _find_teensy(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            #probably usbmodem
            if 'usbmodem' in port.device:
                print(f"Detected {port.device}")
                return port.device
        return None
    
    def spot_trigger(self):
        if self.connected and self.serial:
            try:
                self.serial.write(b'1')#SPOT
                self.serial.flush()
                print("→ Motor ASSIST (pulling up)")
                return True
            except Exception as e:
                print(f"Spot trigger error {e}")
                return False
        else:
            print("Would send ASSIST but no motor mode")
            return False

    def spot_terminate(self):
        if self.connected and self.serial:
            try:
                self.serial.write(b'2')#RELEASE
                self.serial.flush()
                print("→ Motor RELEASE (giving slack)")
                
                time.sleep(1)
                
                # Then stop
                self.serial.write(b'0')#STOP
                self.serial.flush()
                print("→ Motor STOP (ready)")
                return True
            except Exception as e:
                print(f"Terminating spot error {e}")
                return False
        else:
            print("Would terminate spot but no motor mode")
            return False
    
    def close(self):
        if self.serial:
            self.serial.close()
            print("Teensy connection closed")