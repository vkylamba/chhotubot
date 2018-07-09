#ifndef _CAMERA_SERVO_H_
#define _CAMERA_SERVO_H_
#include <Servo.h>

class CameraServo
{
    Servo servo_v;
    Servo servo_h;

public:
    CameraServo()
    {
        servo_h.attach(9);
        servo_v.attach(10);
        servo_h.write(90);
        servo_v.write(90);
    }

    uint8_t get_horizontal()
    {
        return this->servo_h.read();
    }
    uint8_t get_vertical()
    {
        return this->servo_v.read();
    }
    void set_horizontal(uint8_t angle);
    void set_vertical(uint8_t angle);

};

void CameraServo::set_horizontal(uint8_t angle)
{
    servo_h.write(angle);
}

void CameraServo::set_vertical(uint8_t angle)
{
    servo_v.write(angle);
}

#endif