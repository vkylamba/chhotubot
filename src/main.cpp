/**
 * Blink
 *
 * Turns on an LED on for one second,
 * then off for one second, repeatedly.
 */
#include "Arduino.h"
#include "configurations.h"
#include "motor_shield/AFMotor.h"
#include "car.h"
#include "ir.h"
// #include "camera_servo.h"
#include <Servo.h>
Servo servo_h;
Servo servo_v;

#define MAX_BUFFER_LENGTH 200
// AF_DCMotor motor1(1);
// AF_DCMotor motor2(4);
// AF_DCMotor motor3(2);
// AF_DCMotor motor4(3);

AF_DCMotor motor1(3);
AF_DCMotor motor2(4);


Car car = Car(motor1, motor2);
IR ir_left(0);
IR ir_right(1);
IR ir_front(2);

char buffer_in[MAX_BUFFER_LENGTH];
char buffer_out[MAX_BUFFER_LENGTH];
uint16_t counter = 0, buffer_counter=0;
int forward = 0;
int backward = 0;
int left = 0;
int right = 0;
int servo_horizontal = 90;
int servo_vertical = 90;
uint8_t indicator_led_state = 0;


void test_movements() {
  car.move_forward(motor1, motor2);
  delay(2000);
  car.stop(motor1, motor2);
  delay(1000);
  car.move_left(motor1, motor2);
  delay(500);
  car.stop(motor1, motor2);
  delay(1000);
  car.move_forward(motor1, motor2);
  delay(2000);
  car.stop(motor1, motor2);
  delay(1000);
  car.move_right(motor1, motor2);
  delay(500);
  car.stop(motor1, motor2);
}


void setup()
{
  Serial.begin(9600);
  servo_h.attach(10);
  servo_h.write(90);
  servo_v.attach(9);
  servo_v.write(90);
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  // test_movements();
}


void clear_buffer(char *buffer, uint16_t buffer_length) {
  for(uint16_t i=0;i<buffer_length;i++) {
    buffer[i] = '\0';
  }
}

void toggle_led() {
  if (indicator_led_state > 0) {
    indicator_led_state = 1;
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    indicator_led_state = 0;
    digitalWrite(LED_BUILTIN, LOW);
  }
}

void move_head(int servo_horizontal, int servo_vertical) {
  if(servo_horizontal > -1)
  {
    servo_h.write(servo_horizontal);
    servo_horizontal = -1;
  }

  if(servo_vertical > -1)
  {
    servo_v.write(servo_vertical);
    servo_vertical = -1;
  }
}


void loop()
{

  // while (1) {

  // } 

  // uint8_t distance_left = ir_left.get_distance();
  // uint8_t distance_right = ir_right.get_distance();
  // uint8_t distance_front = ir_front.get_distance();

  uint8_t distance_left = 0;
  uint8_t distance_right = 0;
  uint8_t distance_front = 0;

  if(Serial.available() > 0)
  {
    toggle_led();
    buffer_in[buffer_counter] = Serial.read();
    // Serial.println(buffer);
    if(buffer_in[buffer_counter] == ';')
    {
      buffer_in[buffer_counter + 1] = '\0';
      buffer_counter = 0;
      // Serial.println(buffer);
      sscanf(buffer_in, "MF:%d,MB:%d,ML:%d,MR:%d,SH:%d,SV:%d;", &forward, &backward, &left, &right, &servo_horizontal, &servo_vertical);
      clear_buffer(buffer_in, MAX_BUFFER_LENGTH);
    }
    else if (buffer_counter < MAX_BUFFER_LENGTH)
      buffer_counter += 1;
    else {
      clear_buffer(buffer_in, MAX_BUFFER_LENGTH);
      buffer_counter = 0;
    }
  }

  if(forward > 0)
  {
    car.move_forward(motor1, motor2);
    forward -= 1;
  }

  if(backward > 0)
  {
    car.move_backward(motor1, motor2);
    backward -= 1;
  }

  if(left > 0)
  {
    car.move_left(motor1, motor2);
    left -= 1;
  }
  if(right > 0)
  {
    car.move_right(motor1, motor2);
    right -= 1;
  }

  if(forward == 0 && backward == 0 && left == 0 && right == 0)
    car.stop(motor1, motor2);

  delay(10);

  if(counter > 100)
  {
    toggle_led();
    move_head(servo_horizontal, servo_vertical);
    clear_buffer(buffer_out, MAX_BUFFER_LENGTH);
    sprintf(buffer_out, "LD:%d,RD:%d,FD:%d,SH:%d,SV:%d;",distance_left, distance_right, distance_front, servo_h.read(), servo_v.read());
    Serial.println(buffer_out);
    counter = 0;
  }

  counter += 1;
}