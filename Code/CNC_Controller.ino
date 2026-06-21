// shift register pins
const int dataPin = 12; // DS
const int latchPin = 13; // STCP
const int clockPin = 14; // SHCP

byte registerStates[3] = {0, 0, 0};

// virtual stepper pins
const int STEPPER1_PUL_PIN = 7;
const int STEPPER1_DIR_PIN = 6;

const int STEPPER2_PUL_PIN = 4;
const int STEPPER2_DIR_PIN = 3;

const int STEPPER3_PUL_PIN = 1;
const int STEPPER3_DIR_PIN = 9;

void setup() {
  // shift register pins
  pinMode ( dataPin, OUTPUT );
  pinMode ( latchPin, OUTPUT );
  pinMode ( clockPin, OUTPUT );

  clearAllPins();
}

void loop() {
  //motor test block

  // set direction
  updatePin(STEPPER1_DIR_PIN, HIGH);

  for(int i = 0; i < 200; i++) {
    updatePin(STEPPER1_PUL_PIN, HIGH);
    delayMicroseconds(800);
    
    updatePin(STEPPER1_PUL_PIN, LOW);
    delayMicroseconds(800);
  }

  delay(1000); // Wait 1 second
  
  // opposite direction
  updatePin(STEPPER1_DIR_PIN, LOW);
  
  for(int i = 0; i < 200; i++) {
    updatePin(STEPPER1_PUL_PIN, HIGH);
    delayMicroseconds(800);
    
    updatePin(STEPPER1_PUL_PIN, LOW);
    delayMicroseconds(800);
  }

  delay(1000);
  
}

void updatePin(int pin, bool state) {
  int chipIndex = pin / 8;
  int bitIndex = pin % 8;

  bitWrite( registerStates[chipIndex], bitIndex, state );

  updateShiftRegisters();
}

void callPin(int pin) {
  int chipIndex = pin / 8;
  int bitIndex = pin % 8;
}

void updateShiftRegisters() {
  digitalWrite ( latchPin, LOW );

  shiftOut ( dataPin, clockPin, MSBFIRST, registerStates[2] );
  shiftOut ( dataPin, clockPin, MSBFIRST, registerStates[1] );
  shiftOut ( dataPin, clockPin, MSBFIRST, registerStates[0] );

  digitalWrite ( latchPin, HIGH );
}

void clearAllPins() {
  registerStates[0] = 0;
  registerStates[1] = 0;
  registerStates[2] = 0;
  updateShiftRegisters();
}