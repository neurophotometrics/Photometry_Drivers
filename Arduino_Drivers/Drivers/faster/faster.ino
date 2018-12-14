#include "faster.h"

/*
 * Filename: faster
 * Author: Christopher Yin & John Messerly
 * Description:
 * User interface for Neurophotometrics
 * Date: 10.24.17
 *
 */

void setup() {

  /*
   * initialize all I/O pins
   */
   
  cli(); // disable interrupts 
  
  //set timer1 interrupt at 1kHz
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 1hz increments
  OCR1A = 15;// = (16*10^6) / (1000*1024) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS10 and CS12 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);
  

  sei(); // enable interrupts 
   
  for(int pin = 0;pin++;pin<3){
    pinMode(potPins[pin],INPUT);
  }

  /*
   * individually initialize output pins
   * error when initialized in loop
   */
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  pinMode(9,OUTPUT);
  pinMode(A0,INPUT);
  pinMode(A1,INPUT);
  pinMode(A2,INPUT);
  pinMode(A3,INPUT);
  
  pinMode(cameraPin,OUTPUT);
  pinMode(selectPin,OUTPUT);

  // initialize SPI communication with digipot
  SPI.begin();
  SPI.setBitOrder(MSBFIRST);

  init_lcd();
}

void loop() {
  startCheck();
  if (!start){
    switchEnable = false;
    shutdown_LED();
    lcd.setCursor(17,3);
    lcd.print("OFF");
    digitalWrite(cameraPin,HIGH);
    while (!start){
      delay(50);
      updateLED();
      updateFPS();    
      modeCheck();
      startCheck();
    }
  }
  else {  
    lcd.setCursor(17,3);
    lcd.print("ON "); 
    switch(mode) {
      case CONSTANT_MODE:
        init_LED(HIGH,HIGH,HIGH);
      break;
      case TRIGGER1_MODE: // interleave purple with blue/green
        init_LED(LOW,HIGH,HIGH);
      break;
      case TRIGGER2_MODE: // interleave green/blue. purple unused
        init_LED(LOW,HIGH,LOW);
      break;
      case TRIGGER3_MODE:
        init_LED(LOW,LOW,LOW);
      break;
    }
    switchEnable = true;
    while(start){
      if (mode == CONSTANT_MODE){
        updateLED();
        delay(50);
      }
      startCheck();
    }
  }
}
