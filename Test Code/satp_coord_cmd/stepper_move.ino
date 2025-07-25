#include <Servo.h>
#include <Stepper.h>
#include <math.h>

const int STEPS_PER_REV = 200;
const float STEP_DEG = 360.0 / STEPS_PER_REV;
Stepper yawStepper(STEPS_PER_REV, 2, 3, 4, 5);

Servo pitchServo;
const int PITCH_MIN_SERVO = 20;
const int PITCH_MAX_SERVO = 160;
const float PITCH_MAX_ANGLE = 20.0;   // ±20° from center


const int FRAME_W = 640;
const int FRAME_H = 480;
const float HFOV = 60.0;   
const float VFOV = 45.0;  
float focalX, focalY;

const float YAW_DEADZONE = 0.5;    
const float PITCH_DEADZONE = 0.5;  

char inBuf[32];
uint8_t bufPos = 0;

float currentYawAngle = 0.0; 
int   currentPitch    = 90;   
float targetYawAngle  = 0.0;
int   targetPitch     = 90;
int   stepsRemaining  = 0;
int   stepDir         = 1;
bool  moveInProgress  = false;
unsigned long lastServoUpdate = 0;

void setup() {
  Serial.begin(9600);
  yawStepper.setSpeed(30);     // RPM
  pitchServo.attach(9);
  pitchServo.write(currentPitch);

  // Precompute focal lengths (pixels) from FOV:
  float halfW = FRAME_W / 2.0;
  float halfH = FRAME_H / 2.0;
  focalX = halfW / tan(radians(HFOV / 2.0));
  focalY = halfH / tan(radians(VFOV / 2.0));
}

void loop() {
  //test_serial();
  readSerialNonBlocking();
  if (moveInProgress) {
    performInterleavedMotion();
  }
}

void readSerialNonBlocking() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || bufPos >= sizeof(inBuf)-1) {
      inBuf[bufPos] = '\0';
      parseCommand(inBuf);
      bufPos = 0;
      break;
    }
    if (c >= '0' && c <= '9' || c=='-' || c==',') {
      inBuf[bufPos++] = c;
    }
  }
}

void parseCommand(const char *s) {
  // split on comma
  char *p = strchr(s, ',');
  if (!p) return;
  *p = '\0';
  int x = atoi(s);
  int y = atoi(p+1);

  // pixel offsets
  float dx = x - FRAME_W/2.0;
  float dy = y - FRAME_H/2.0;

  // angle offsets (°)
  float yawAng   = degrees(atan(dx / focalX));
  float pitchAng = -degrees(atan(dy / focalY));

  // dead‑zone filter
  if (fabs(yawAng)  < YAW_DEADZONE)   yawAng   = 0;
  if (fabs(pitchAng) < PITCH_DEADZONE) pitchAng = 0;

  // compute target yaw (absolute)
  targetYawAngle = yawAng;
  float deltaYaw = targetYawAngle - currentYawAngle;
  stepsRemaining = int(fabs(deltaYaw) / STEP_DEG + 0.5);
  stepDir = (deltaYaw >= 0) ? 1 : -1;

  // compute target pitch (servo)
  if (pitchAng >  PITCH_MAX_ANGLE)  pitchAng =  PITCH_MAX_ANGLE;
  if (pitchAng < -PITCH_MAX_ANGLE)  pitchAng = -PITCH_MAX_ANGLE;
  targetPitch = map(pitchAng*100, -100*PITCH_MAX_ANGLE, 100*PITCH_MAX_ANGLE,
                    PITCH_MAX_SERVO, PITCH_MIN_SERVO);
  targetPitch = constrain(targetPitch, PITCH_MIN_SERVO, PITCH_MAX_SERVO);

  moveInProgress = (stepsRemaining>0) || (targetPitch!=currentPitch);
}

// One stepper step + servo nudge every loop iteration
void performInterleavedMotion() {
  if (stepsRemaining > 0) {
    yawStepper.step(stepDir);
    currentYawAngle += STEP_DEG * stepDir;
    stepsRemaining--;
  }

  if (millis() - lastServoUpdate > 20) {
    if (currentPitch < targetPitch) currentPitch++;
    else if (currentPitch > targetPitch) currentPitch--;
    pitchServo.write(currentPitch);
    lastServoUpdate = millis();
  }

  if (stepsRemaining == 0 && currentPitch == targetPitch) {
    moveInProgress = false;
    Serial.print("yaw="); Serial.print(currentYawAngle);
    Serial.print("°, pitch="); Serial.println(currentPitch);
  }
}

void test_serial(){   
  if(Serial.available() > 0){     
    String data = Serial.readStringUntil('\n');     
    data.trim();            
    // Parse x,y coordinates     
    int commaIndex = data.indexOf(',');     
    if (commaIndex > 0) {       
      int x = data.substring(0, commaIndex).toInt();       
      int y = data.substring(commaIndex + 1).toInt();                
      // Print the coordinates       
      Serial.print("X: ");       
      Serial.print(x);       
      Serial.print(", Y: ");       
      Serial.println(y);   
    }   
  } 
}