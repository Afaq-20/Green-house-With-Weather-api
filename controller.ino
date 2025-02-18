// Sensor pins
#define NPK_SENSOR_PIN A0
#define MOISTURE_SENSOR_PIN A1
#define TEMP_SENSOR_PIN A2

// Actuator pins
#define FAN_PIN 8
#define WATER_PUMP_PIN 9
#define MOTOR_IN1 4
#define MOTOR_IN2 5
#define MOTOR_EN 6

// Thresholds (will be updated via serial communication)
float MOISTURE_MIN = 0.0;
float MOISTURE_MAX = 100.0;
float TEMP_MIN = 0.0;
float TEMP_MAX = 50.0;

// Control flags
bool mainPowerOn = true;
bool waterPumpEnabled = true;
bool lightEnabled = true;

// Sensor values
float npk_values[3];  // N, P, K values
float pH_value;
float moisture_value;
float temperature;

void setup() {
  Serial.begin(9600);
  
  // Initialize pins
  pinMode(FAN_PIN, OUTPUT);
  pinMode(WATER_PUMP_PIN, OUTPUT);
  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MOTOR_IN2, OUTPUT);
  pinMode(MOTOR_EN, OUTPUT);
  
  // Initial state: all actuators OFF
  digitalWrite(FAN_PIN, LOW);
  digitalWrite(WATER_PUMP_PIN, LOW);
  digitalWrite(MOTOR_IN1, LOW);
  digitalWrite(MOTOR_IN2, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    handleCommand(command);
  }
  
  if (mainPowerOn) {
    readSensors();
    if (waterPumpEnabled) {
      controlWaterPump();
    }
    if (lightEnabled) {
      controlLight();
    }
    sendDataToSerial();
  } else {
    // Turn off all actuators when main power is off
    digitalWrite(WATER_PUMP_PIN, LOW);
    digitalWrite(FAN_PIN, LOW);
  }
  delay(1000);
}

void handleCommand(String command) {
  if (command.startsWith("THRESH")) {
    // Format: THRESH,moisture_min,moisture_max,temp_min,temp_max
    int firstComma = command.indexOf(',');
    int secondComma = command.indexOf(',', firstComma + 1);
    int thirdComma = command.indexOf(',', secondComma + 1);
    int fourthComma = command.indexOf(',', thirdComma + 1);
    
    MOISTURE_MIN = command.substring(firstComma + 1, secondComma).toFloat();
    MOISTURE_MAX = command.substring(secondComma + 1, thirdComma).toFloat();
    TEMP_MIN = command.substring(thirdComma + 1, fourthComma).toFloat();
    TEMP_MAX = command.substring(fourthComma + 1).toFloat();
  }
  else if (command == "POWER_ON") mainPowerOn = true;
  else if (command == "POWER_OFF") mainPowerOn = false;
  else if (command == "PUMP_ON") waterPumpEnabled = true;
  else if (command == "PUMP_OFF") waterPumpEnabled = false;
  else if (command == "LIGHT_ON") lightEnabled = true;
  else if (command == "LIGHT_OFF") lightEnabled = false;
}

void readSensors() {
  // Simulate NPK sensor readings
  npk_values[0] = random(0, 140);  // N
  npk_values[1] = random(5, 145);  // P
  npk_values[2] = random(5, 205);  // K
  pH_value = random(4.0, 8.0);
  
  // Read actual sensors
  moisture_value = analogRead(MOISTURE_SENSOR_PIN);
  temperature = analogRead(TEMP_SENSOR_PIN);
  
  // Convert analog readings to actual values
  moisture_value = map(moisture_value, 0, 1023, 0, 100);
  temperature = (analogRead(TEMP_SENSOR_PIN) * 0.48875);
}

void controlWaterPump() {
  if (moisture_value < MOISTURE_MIN) {
    digitalWrite(WATER_PUMP_PIN, HIGH);
  } else if (moisture_value > MOISTURE_MAX) {
    digitalWrite(WATER_PUMP_PIN, LOW);
  }
}

void controlLight() {
  if (temperature > TEMP_MAX) {
    digitalWrite(FAN_PIN, HIGH);
  } else if (temperature < TEMP_MIN) {
    digitalWrite(FAN_PIN, LOW);
  }
}

void sendDataToSerial() {
  // Format: N,P,K,pH,moisture,temperature
  Serial.print(npk_values[0]); Serial.print(",");
  Serial.print(npk_values[1]); Serial.print(",");
  Serial.print(npk_values[2]); Serial.print(",");
  Serial.print(pH_value); Serial.print(",");
  Serial.print(moisture_value); Serial.print(",");
  Serial.println(temperature);
}