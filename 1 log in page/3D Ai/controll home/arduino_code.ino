// Pin definitions
#define LIGHT1 2
#define LIGHT2 3
#define FAN 4
#define STREET1 5
#define STREET2 6

#define MOTOR_IN1 7
#define MOTOR_IN2 8

void setup() {
  Serial.begin(9600);

  pinMode(LIGHT1, OUTPUT);
  pinMode(LIGHT2, OUTPUT);
  pinMode(FAN, OUTPUT);
  pinMode(STREET1, OUTPUT);
  pinMode(STREET2, OUTPUT);
  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MOTOR_IN2, OUTPUT);

  // All devices off at start
  digitalWrite(LIGHT1, LOW);
  digitalWrite(LIGHT2, LOW);
  digitalWrite(FAN, LOW);
  digitalWrite(STREET1, LOW);
  digitalWrite(STREET2, LOW);
  digitalWrite(MOTOR_IN1, LOW);
  digitalWrite(MOTOR_IN2, LOW);
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();

    switch (cmd) {
      case 'A': digitalWrite(LIGHT1, HIGH); break;  // Light 1 ON
      case 'B': digitalWrite(LIGHT1, LOW); break;   // Light 1 OFF
      case 'C': digitalWrite(LIGHT2, HIGH); break;  // Light 2 ON
      case 'D': digitalWrite(LIGHT2, LOW); break;   // Light 2 OFF
      case 'E': digitalWrite(FAN, HIGH); break;     // Fan ON
      case 'F': digitalWrite(FAN, LOW); break;      // Fan OFF
      case 'G':                                     // Street lights ON
        digitalWrite(STREET1, HIGH);
        digitalWrite(STREET2, HIGH);
        break;
      case 'H':                                     // Street lights OFF
        digitalWrite(STREET1, LOW);
        digitalWrite(STREET2, LOW);
        break;
      case 'I':                                     // Door Open - Clockwise 10 sec
        digitalWrite(MOTOR_IN1, HIGH);
        digitalWrite(MOTOR_IN2, LOW);
        delay(10000);
        digitalWrite(MOTOR_IN1, LOW);
        digitalWrite(MOTOR_IN2, LOW);
        break;
      case 'J':                                     // Door Close - Anticlockwise 10 sec
        digitalWrite(MOTOR_IN1, LOW);
        digitalWrite(MOTOR_IN2, HIGH);
        delay(10000);
        digitalWrite(MOTOR_IN1, LOW);
        digitalWrite(MOTOR_IN2, LOW);
        break;
      case 'K':                                     // All lights ON
        digitalWrite(LIGHT1, HIGH);
        digitalWrite(LIGHT2, HIGH);
        digitalWrite(STREET1, HIGH);
        digitalWrite(STREET2, HIGH);
        break;

      case 'L':                                     // All lights OFF
        digitalWrite(LIGHT1, LOW);
        digitalWrite(LIGHT2, LOW);
        digitalWrite(STREET1, LOW);
        digitalWrite(STREET2, LOW);
        break;

        case 'M':  // Fancy blink animation
        for (int i = 0; i < 20; i++) {
          digitalWrite(LIGHT1, HIGH);
          delay(50);
          digitalWrite(LIGHT1, LOW);
          delay(50);
      
          digitalWrite(LIGHT2, HIGH);
          delay(50);
          digitalWrite(LIGHT2, LOW);
          delay(50);
      
          digitalWrite(STREET1, HIGH);
          delay(50);
          digitalWrite(STREET1, LOW);
          delay(50);
      
          digitalWrite(STREET2, HIGH);
          delay(50);
          digitalWrite(STREET2, LOW);
          delay(50);
        }
      
        // End with all ON for effect
        digitalWrite(LIGHT1, HIGH);
        digitalWrite(LIGHT2, HIGH);
        digitalWrite(STREET1, HIGH);
        digitalWrite(STREET2, HIGH);
        break;
      
          }
  }
}
