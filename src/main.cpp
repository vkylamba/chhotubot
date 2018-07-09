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

#ifndef LED_BUILTIN
#define LED_BUILTIN 13
#endif

AF_DCMotor motor1(1);
AF_DCMotor motor2(4);
AF_DCMotor motor3(2);
AF_DCMotor motor4(3);


Car car = Car(motor1, motor2, motor3, motor4);
IR ir_left(0);
IR ir_right(1);
IR ir_front(2);

char buffer[100];
char extra[50];
uint8_t counter = 0, buffer_counter=0;
int forward = 0;
int backward = 0;
int left = 0;
int right = 0;
int servo_horizontal = 0;
int servo_vertical = 0;

void setup()
{
  Serial.begin(9600);
  servo_h.attach(10);
  servo_h.write(90);
  servo_v.attach(9);
  servo_v.write(90);
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  // car.move_forward(motor1, motor2, motor3, motor4);
  // delay(5000);
  // car.move_left(motor1, motor2, motor3, motor4);
  // delay(2000);
  // car.move_forward(motor1, motor2, motor3, motor4);
  // delay(5000);
  // car.move_right(motor1, motor2, motor3, motor4);
  // delay(2000);
  // car.stop(motor1, motor2, motor3, motor4);
  uint8_t distance_left = ir_left.get_distance();
  uint8_t distance_right = ir_right.get_distance();
  uint8_t distance_front = ir_front.get_distance();

  // if(distance_left < 20)
  //   car.move_left(motor1, motor2, motor3, motor4);
  // else if(distance_right < 20)
  //   car.move_right(motor1, motor2, motor3, motor4);
  // else if(distance_front < 20)
  //   car.stop(motor1, motor2, motor3, motor4);
  // else
  //   car.move_forward(motor1, motor2, motor3, motor4);


  // if(i>0)
  // {
  //   servo1.write(180);
  //   servo2.write(180);
  //   i=0;
  // }
  // else
  // {
  //   servo1.write(-180);
  //   servo2.write(-180);
  //   i=1;
  // }

  // Serial.println("L: ");
  // Serial.println(distance_left);
  // Serial.println("R: ");
  // Serial.println(distance_right);
  // Serial.println("F: ");
  // Serial.println(distance_front);

  // Serial.println("H: ");
  // Serial.println(servo_h.read());
  // Serial.println("V: ");
  // Serial.println(servo_v.read());


  // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_BUILTIN, HIGH);
  // wait for a second
  // delay(10);

  // turn the LED off by making the voltage LOW
  digitalWrite(LED_BUILTIN, LOW);
   // wait for a second
  // delay(10);

  if(Serial.available() > 0)
  {
    buffer[buffer_counter] = Serial.read();
    // Serial.println(buffer);
    if(buffer[buffer_counter] == ';')
    {
      buffer[buffer_counter + 1] = '\0';
      // Serial.println(buffer);
      if(sscanf(buffer, "MF:%d,MB:%d,ML:%d,MR:%d,SH:%d,SV:%d;", &forward, &backward, &left, &right, &servo_horizontal, &servo_vertical))
      {
        buffer_counter = 0;
        buffer[0] = '\0';
        // sprintf(buffer, "MF:%d,MB:%d,ML:%d,MR:%d,SH:%d,SV:%d",forward, backward, left, right, servo_horizontal, servo_vertical);
        // Serial.println(buffer);
        for(uint8_t i=0;i<100;i++)
          buffer[0] = '\0';

        sprintf(buffer, "LD:%d,RD:%d,FD:%d,SH:%d,SV:%d",distance_left, distance_right, distance_front, servo_h.read(), servo_v.read());
        Serial.println(buffer);
      }
      else
      {
        for(uint8_t i=0;i<100;i++)
          buffer[0] = '\0';
        buffer_counter = 0;
        sprintf(buffer, "LD:%d,RD:%d,FD:%d,SH:%d,SV:%d",distance_left, distance_right, distance_front, servo_h.read(), servo_v.read());
        Serial.println(buffer);
      }
    }
    else
      buffer_counter += 1;
  }

  if(forward > 0)
  {
    car.move_forward(motor1, motor2, motor3, motor4);
    forward -= 1;
  }

  if(backward > 0)
  {
    car.move_backward(motor1, motor2, motor3, motor4);
    backward -= 1;
  }

  if(left > 0)
  {
    car.move_left(motor1, motor2, motor3, motor4);
    left -= 1;
  }
  if(right > 0)
  {
    car.move_right(motor1, motor2, motor3, motor4);
    right -= 1;
  }

  if(forward == 0 && backward == 0 && left == 0 && right == 0)
    car.stop(motor1, motor2, motor3, motor4);

  if(servo_horizontal > 0)
  {
    servo_h.write(servo_horizontal);
    servo_horizontal = 0;
  }

  if(servo_vertical > 0)
  {
    servo_v.write(servo_vertical);
    servo_vertical = 0;
  }

  // if(counter > 100)
  // {
  //   sprintf(buffer, "LD:%d,RD:%d,FD:%d,SH:%d,SV:%d",distance_left, distance_right, distance_front, servo_h.read(), servo_v.read());
  //   Serial.println(buffer);
  //   counter = 0;
  // }
  // else
  //   counter += 1;
}