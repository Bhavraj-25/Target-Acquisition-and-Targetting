#include <Servo.h>
#include <AccelStepper.h>

#define FOV_X 78.0
#define FOV_Y 50.0
#define x_center 960
#define y_center 540
#define step_per_rev 200
#define step_angle 1.8

const float x_per_pixel = 0.0406;
const float y_per_pixel = 0.0463;
int pitch_norm = 90;
int yaw_norm = 0;

AccelStepper stepper(AccelStepper::DRIVER, 3, 2);
Servo servo;

void setup() {
  // put your setup code here, to run once:
  servo.attach(9);
  stepper.setMaxSpeed(500);
  stepper.setAcceleration(100);
  servo.write(pitch_norm);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0){
    String data = Serial.readStringUntil("\n");
    int commaIndex = data.indexOf(",");
    int x_offset = data.substring(0, commaIndex).toInt();
    int y_offset = data.substring(commaIndex + 1).toInt();

    float yaw_step = 0;
    int pitch_angle = 0;

    stepper_move(x_offset, y_offset, &yaw_step, &pitch_angle);

    stepper.move(yaw_step);
    stepper.runToPosition();

    servo.write(pitch_angle);
  }

}

void stepper_move(int x_offset,int y_offset, float *yaw_step, int *pitch_angle){
    float theta_x = x_offset * x_per_pixel;
    float theta_y = y_offset * y_per_pixel;

    *yaw_step = ((theta_x / step_angle) * step_per_rev);
    *pitch_angle = constrain((pitch_norm - theta_y), 0, 180);
}
