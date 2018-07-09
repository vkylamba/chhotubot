# ifndef _CAR_H_
#define _CAR_H_
#include "motor_shield/AFMotor.h"

class Car
{
    public:
    Car(AF_DCMotor motor_a, AF_DCMotor motor_b, AF_DCMotor motor_c, AF_DCMotor motor_d)
    {

        motor_a.setSpeed(200);
        motor_a.run(RELEASE);

        motor_b.setSpeed(200);
        motor_b.run(RELEASE);

        motor_c.setSpeed(200);
        motor_c.run(RELEASE);

        motor_d.setSpeed(200);
        motor_d.run(RELEASE);
    }

    void move_forward(AF_DCMotor motor_a, AF_DCMotor motor_b, AF_DCMotor motor_c, AF_DCMotor motor_d);
    void move_backward(AF_DCMotor motor_a, AF_DCMotor motor_b, AF_DCMotor motor_c, AF_DCMotor motor_d);
    void move_left(AF_DCMotor motor_a, AF_DCMotor motor_b, AF_DCMotor motor_c, AF_DCMotor motor_d);
    void move_right(AF_DCMotor motor_a, AF_DCMotor motor_b, AF_DCMotor motor_c, AF_DCMotor motor_d);
    void stop(AF_DCMotor motor_a, AF_DCMotor motor_b, AF_DCMotor motor_c, AF_DCMotor motor_d);
};

void Car::move_forward(AF_DCMotor motor_a, AF_DCMotor motor_b, AF_DCMotor motor_c, AF_DCMotor motor_d)
{
    motor_a.run(FORWARD);
    motor_a.setSpeed(250);

    motor_b.run(FORWARD);
    motor_b.setSpeed(250);

    motor_c.run(FORWARD);
    motor_c.setSpeed(250);

    motor_d.run(FORWARD);
    motor_d.setSpeed(250);
}

void Car::move_left(AF_DCMotor motor_a, AF_DCMotor motor_b, AF_DCMotor motor_c, AF_DCMotor motor_d)
{
    motor_a.run(BACKWARD);
    motor_a.setSpeed(250);

    motor_b.run(BACKWARD);
    motor_b.setSpeed(250);

    motor_c.run(FORWARD);
    motor_c.setSpeed(250);

    motor_d.run(FORWARD);
    motor_d.setSpeed(250);
}

void Car::move_right(AF_DCMotor motor_a, AF_DCMotor motor_b, AF_DCMotor motor_c, AF_DCMotor motor_d)
{
    motor_a.run(FORWARD);
    motor_a.setSpeed(250);

    motor_b.run(FORWARD);
    motor_b.setSpeed(250);

    motor_c.run(BACKWARD);
    motor_c.setSpeed(250);

    motor_d.run(BACKWARD);
    motor_d.setSpeed(250);
}


void Car::move_backward(AF_DCMotor motor_a, AF_DCMotor motor_b, AF_DCMotor motor_c, AF_DCMotor motor_d)
{
    motor_a.run(BACKWARD);
    motor_a.setSpeed(250);

    motor_b.run(BACKWARD);
    motor_b.setSpeed(250);

    motor_c.run(BACKWARD);
    motor_c.setSpeed(250);

    motor_d.run(BACKWARD);
    motor_d.setSpeed(250);
}

void Car::stop(AF_DCMotor motor_a, AF_DCMotor motor_b, AF_DCMotor motor_c, AF_DCMotor motor_d)
{
    motor_a.setSpeed(250);
    motor_a.run(RELEASE);

    motor_b.setSpeed(250);
    motor_b.run(RELEASE);

    motor_c.setSpeed(250);
    motor_c.run(RELEASE);

    motor_d.setSpeed(250);
    motor_d.run(RELEASE);
}

#endif