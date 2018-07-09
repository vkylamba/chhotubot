#ifndef _IR_H_
#define _IR_H_

class IR
{
    uint8_t pin;

    public:
    IR(uint8_t pin)
    {
      this->pin = pin;
    }

    uint8_t get_distance();
};

uint8_t IR::get_distance()
{
  uint32_t sum = 0;
  for(uint8_t i=0;i<50;i++)
  {
    sum += analogRead(pin);
    // delay(10);
  }
  sum = sum / 50;
  float volts = sum*0.0048828125;  // value from sensor * (5/1024)
  uint8_t distance = 13*pow(volts, -1); // worked out from datasheet graph

  return distance;
}

#endif