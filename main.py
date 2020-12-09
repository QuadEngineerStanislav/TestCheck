#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative

vehicle = connect('/dev/ttyAMA0', baud=57600, wait_ready=True)

print(vehicle.location.global_relative_frame)
print(vehicle.system_status)
time.sleep(20)
def arm_and_takeoff(aTargetAltitude):

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)


arm_and_takeoff(2)

print("Set default/target airspeed to 3")
vehicle.airspeed = 3

print("Go target!")
point = LocationGlobalRelative(50.194884, 39.573052, 2)
vehicle.simple_goto(point)
time.sleep(2)
while vehicle.airspeed > 0.1:
   print ("Speed: %s" % vehicle.airspeed)
   print(" Altitude: ", vehicle.location.global_relative_frame.alt)
   time.sleep(1)

time.sleep(5)
print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")


print("Close vehicle object")
vehicle.close()

