const int PIN_ENA = 22; // PWM Speed Pin
const int PIN_IN1 = 18; // Direction 1
const int PIN_IN2 = 19; // Direction 2

void setup() {
  pinMode(PIN_ENA, OUTPUT);
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);

  // Initial state: Stopped
  digitalWrite(PIN_IN1, LOW);
  digitalWrite(PIN_IN2, LOW);
  analogWrite(PIN_ENA, 0);

  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == '1') {
      // ASSIST: Pull up (forward)
      digitalWrite(PIN_IN1, HIGH);
      digitalWrite(PIN_IN2, LOW);
      analogWrite(PIN_ENA, 255); // Max speed
    } 
    else if (command == '2') {
      // RELEASE: Reverse to give slack
      digitalWrite(PIN_IN1, LOW);
      digitalWrite(PIN_IN2, HIGH);
      analogWrite(PIN_ENA, 180);
    }
    else if (command == '0') {
      // STOP: Hold position / idle
      analogWrite(PIN_ENA, 0);
      digitalWrite(PIN_IN1, LOW);
      digitalWrite(PIN_IN2, LOW);
    }
  }
}