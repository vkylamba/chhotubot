# ifndef _CAR_H_
#define _CAR_H_
#include "motor_shield/AFMotor.h"

#define INITIALIZATION_SPEED 10
#define CAR_SPEED 80

class Car
{
    public:
    Car(AF_DCMotor motor_a, AF_DCMotor motor_b)
    {

        motor_a.setSpeed(INITIALIZATION_SPEED);
        motor_a.run(RELEASE);

        motor_b.setSpeed(INITIALIZATION_SPEED);
        motor_b.run(RELEASE);

    }

    void move_forward(AF_DCMotor motor_a, AF_DCMotor motor_b);
    void move_backward(AF_DCMotor motor_a, AF_DCMotor motor_b);
    void move_left(AF_DCMotor motor_a, AF_DCMotor motor_b);
    void move_right(AF_DCMotor motor_a, AF_DCMotor motor_b);
    void stop(AF_DCMotor motor_a, AF_DCMotor motor_b);
};

void Car::move_forward(AF_DCMotor motor_a, AF_DCMotor motor_b)
{
    motor_a.run(FORWARD);
    motor_a.setSpeed(CAR_SPEED);

    motor_b.run(FORWARD);
    motor_b.setSpeed(CAR_SPEED);
}

void Car::move_left(AF_DCMotor motor_a, AF_DCMotor motor_b)
{
    motor_a.run(BACKWARD);
    motor_a.setSpeed(CAR_SPEED);

    motor_b.run(BACKWARD);
    motor_b.setSpeed(CAR_SPEED);
}

void Car::move_right(AF_DCMotor motor_a, AF_DCMotor motor_b)
{
    motor_a.run(FORWARD);
    motor_a.setSpeed(CAR_SPEED);

    motor_b.run(FORWARD);
    motor_b.setSpeed(CAR_SPEED);
}


void Car::move_backward(AF_DCMotor motor_a, AF_DCMotor motor_b)
{
    motor_a.run(BACKWARD);
    motor_a.setSpeed(CAR_SPEED);

    motor_b.run(BACKWARD);
    motor_b.setSpeed(CAR_SPEED);
}

void Car::stop(AF_DCMotor motor_a, AF_DCMotor motor_b)
{
    motor_a.setSpeed(CAR_SPEED);
    motor_a.run(RELEASE);

    motor_b.setSpeed(CAR_SPEED);
    motor_b.run(RELEASE);
}

#endif