# Fiber Photometry Drivers

![Image of NPM] (/RPi_Drivers/NPMLogo.png)

Arduino and Rapsberry Pi code for controlling fiber photometry machines found at 
https://www.neurophotometrics.com/


*Legacy Arduino Driver*:

Uses an LCD display and physical knobs as the user interface. Controls the machine's LEDs and 
camera triggering directly with GPIO. 



*Rasberry Pi with Touch Screen*:

Kivy implementation of a touch screen GUI for the photometry machine. Has two drivers:

1. Pure Raspberry Driver. Uses the Raspberry GPIO to control the LEDs and camera triggering, i.e. interfaces
directly with the machine with no other parts. 

2. Raspberry Serial-To-Arduino Driver. For legacy use. The Raspberry Pi communicates with the legacy arduino 
system via USB cable, and is able to control the machine via the arduino. Enables users who have old circuitry 
to add a touch screen GUI 
