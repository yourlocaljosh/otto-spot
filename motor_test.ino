/*
  Teensy 4.1 & DROK Driver - PWM Sweep Test
  Gradually increases and decreases motor speed.
*/

const int PIN_ENA = 22; // PWM Speed Pin
const int PIN_IN1 = 18; // Direction 1
const int PIN_IN2 = 19; // Direction 2

void setup() {
  // Set frequency to 8kHz for silent operation (Max is 10kHz)
  analogWriteFrequency(PIN_ENA, 8000); 

  pinMode(PIN_ENA, OUTPUT);
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);

  Serial.begin(9600);
  Serial.println("Starting PWM Sweep in 3 seconds...");
  delay(3000);
}

void loop() {
  // Set Direction: Forward
  digitalWrite(PIN_IN1, HIGH);
  digitalWrite(PIN_IN2, LOW);

  // Ramp Up
  Serial.println("Ramping UP...");
  for (int speed = 0; speed <= 255; speed++) {
    analogWrite(PIN_ENA, speed);
    delay(20); // Takes ~5 seconds to reach full speed
  }

  // Hold Full Speed
  Serial.println("FULL SPEED");
  delay(10000);

  // Ramp Down
  Serial.println("Ramping DOWN...");
  for (int speed = 255; speed >= 0; speed--) {
    analogWrite(PIN_ENA, speed);
    delay(20);
  }

  // Brake/Stop
  Serial.println("STOPPED");
  digitalWrite(PIN_IN1, LOW);
  digitalWrite(PIN_IN2, LOW);
  delay(2000);
}