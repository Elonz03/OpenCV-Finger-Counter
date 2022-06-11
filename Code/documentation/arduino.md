# Arduino Documentation
This documents information regarding the setting up of the arduino hardware 
with the LCD screen. The Arduino was set up based on the tutorial found on 
the Arduino website, a link to it can be found 
[here](https://www.arduino.cc/en/Tutorial/LibraryExamples/HelloWorld).

In that webpage, it outlines the required hardware and how to set up the 
connections. It also, has some example sketches that can be run to ensure it 
is set up correctly. 

## Find the port - Serial connection
For a linux machine the serial port the device is connected to can be found 
using the following command in the terminal:
```
ls /dev/tty* | grep usb
```