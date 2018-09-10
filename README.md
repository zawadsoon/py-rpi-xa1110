# py-rpi-xa1110
# Setup and Connections
//Be patient
# Documentation
// Soon
# But how do I know it works?
Um... Fistly if LED on Device is endabled and blink (It is hard to miss blue LED) thats means your GPS have a satellite fix. Second, when you see something most interesting than zeros it also means your GPS have a satellite fix.
In my case I have to go outside to be in range of the satellites. Usually I have to wait about 1-2 min to find sattelites (I do not have antenna)
# Known ISSUE
I can't figure it out where the data starts. Deviace sends stream of bytes. When you receive 255 bytes (or other number), you will have only part of first and last NMEA frame. It is up to you to concat last incomplete frame with first uncomplete frame of the next request. To illustrate this I attach two subsequent frames
```
# First frame
,,,,,*02
$GNRMC,114442.090,V,,,,,0.00,0.00,100918,,,N*5D
$GNVTG,0.00,T,,M,0.00,N,0.00,K,N*2C
$GNGGA,114443.090,,,,,0,0,,,M,,M,,*58
$GPGSA,A,1,,,,,,,,,,,,,,,*1E
$GLGSA,A,1,,,,,,,,,,,,,,,*02
$GNRMC,114443.090,V,,,,,0.00,0.00,100918,,,N*5C
$GNVTG,0.00,T,,M,0.00,N,0.00,K,N*2C
$GNG

# Second frame
GA,114444.090,,,,,0,0,,,M,,M,,*5F
$GPGSA,A,1,,,,,,,,,,,,,,,*1E
$GLGSA,A,1,,,,,,,,,,,,,,,*02
$GNRMC,114444.090,V,,,,,0.00,0.00,100918,,,N*5B
$GNVTG,0.00,T,,M,0.00,N,0.00,K,N*2C
$GNGGA,114445.090,,,,,0,0,,,M,,M,,*5E
$GPGSA,A,1,,,,,,,,,,,,,,,*1E
$GLGSA,A,1,,,,,,,,,,,,,,,*02
$GNRMC
```
# Contribution
Do you know whats going on? Can you help? Contribute and send pull-request! Or share some info. Did I something wrong? Tell me I will do it better.
Any help will be very welcome.
# License 
This code is public domain but you buy me a beer if you use this and we meet someday (Beerware license).
