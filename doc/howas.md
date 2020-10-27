# H.O.W.A.S

Hands on Wacom and Stick

## Mapping virtual buttons from Wacom touch input to virtual joystick

### To do

  * Hat comms/target controls aren't quite usable at the moment. Alternatives?
    * Use non-return-to-center for wheel, use toggle rather than hold, and unmap from quick look
    * Build hybrid button/wheel control
  * Axis controls "grabbing" input is good, but accidental button presses suck (premature countermeasures, anyone?)
    * Increase spacing between axis/button inputs
    * Cull active touch inputs. Prevent them from triggering others
  * Yaw is good, but maybe too much play?
    * Reduce control size
  * Switch to libev/evdev (Python) for Wacom input--may improve performance
