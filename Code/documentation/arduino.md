# Arduino Documentation
This documents information regarding the setting up of the arduino hardware 
with the LCD screen. The Arduino was set up based on the tutorial found on 
the Arduino website, a link to it can be found 
[here](https://www.arduino.cc/en/Tutorial/LibraryExamples/HelloWorld).

In that webpage, it outlines the required hardware and how to set up the 
connections. It also, has some example sketches that can be run to ensure it 
is set up correctly. 

## Changes from the tutorial
### Digital pins used
From the tutorial, I've changed the digital pins used. The reason being the
use of the nRF52 Feather Express instead of an Arduino Uno. So, I've used
the following connections instead (pins 12 and 11 are the same):
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 10
 * LCD D5 pin to digital pin 49
 * LCD D6 pin to digital pin 6
 * LCD D7 pin to digital pin 5

## Find the port - Serial connection
For a linux machine the serial port the device is connected to can be found 
using the following command in the terminal:
```
ls /dev/tty* | grep usb
```

## Future work
### Bluetooth communication
The nRF52 Feather Express board has BLE capabilities. This means Bluetooth
could be used to transfer the data from the computer to the LCD device. This
would be a fun extension of the project and give more experience with
Bluetooth protocols.