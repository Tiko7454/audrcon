from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil
import time
import math


class Drone:
    def __init__(self, connection_string):
        self.vehicle = connect(connection_string, wait_ready=True)
        self.has_taken_off = False

    def print_information(self):
        print(" GPS: %s" % self.vehicle.gps_0)
        print(" Battery: %s" % self.vehicle.battery)
        print(" Last Heartbeat: %s" % self.vehicle.last_heartbeat)
        print(" System status: %s" % self.vehicle.system_status.state)
        print(" Mode: %s" % self.vehicle.mode.name)

    def set_mode(self, mode):
        print("Switching to %s mode " % mode)
        self.vehicle.mode = VehicleMode(mode)

    def arm(self, force=False):
        if force:
            self.set_mode("GUIDED_NOGPS")

        if not force and self.vehicle.mode != "GUIDED":
            self.set_mode("GUIDED")

        print("Basic pre-arm checks")
        while not force and not self.vehicle.is_armable:
            print("Waiting for vehicle to initialise...")
            time.sleep(1)

        self.vehicle.armed = True
        while not self.vehicle.armed:
            print("Waiting for arming...")
            time.sleep(1)
        print("Drone is armed")

    def disarm(self):
        self.vehicle.armed = False
        while self.vehicle.armed:
            print("Waiting for drone to disarm...")
            time.sleep(1)
        print("Drone is disarmed.")

    def take_off(self, target_altitude):
        if not self.vehicle.armed:
            print("Drone was not armed")
            self.arm()

        if self.vehicle.mode != "GUIDED":
            self.set_mode("GUIDED")

        print("Taking off!")
        self.vehicle.simple_takeoff(target_altitude)

        while True:
            print("Altitude: %s" % self.vehicle.location.global_relative_frame.alt)
            if (
                self.vehicle.location.global_relative_frame.alt
                >= target_altitude * 0.95
            ):
                print("Reached target altitude")
                self.has_taken_off = True
                break
            time.sleep(1)

    def yaw(self, degree, relative=False):
        if not self.has_taken_off:
            print("Drone has not taken off yet")
            return

        if relative:
            is_relative = 1
        else:
            is_relative = 0

        msg = self.vehicle.message_factory.command_long_encode(
            0,
            0,
            mavutil.mavlink.MAV_CMD_CONDITION_YAW,
            0,
            degree,
            0,
            1,
            is_relative,
            0,
            0,
            0,
        )
        self.vehicle.send_mavlink(msg)
        print("Drone was yawed at %s degrees" % degree)

    def get_location_metres(self, original_location, d_north, d_east):
        earth_radius = 6378137.0
        d_lat = d_north / earth_radius
        d_lon = d_east / (
            earth_radius * math.cos(math.pi * original_location.lat / 180)
        )

        new_lat = original_location.lat + (d_lat * 180 / math.pi)
        new_lon = original_location.lon + (d_lon * 180 / math.pi)
        if type(original_location) is LocationGlobal:
            target_location = LocationGlobal(new_lat, new_lon, original_location.alt)
        elif type(original_location) is LocationGlobalRelative:
            target_location = LocationGlobalRelative(
                new_lat, new_lon, original_location.alt
            )
        else:
            raise Exception("Invalid Location object passed")

        return target_location

    def get_distance_metres(self, a_location1, a_location2):
        d_lat = a_location2.lat - a_location1.lat
        d_long = a_location2.lon - a_location1.lon
        return math.sqrt((d_lat * d_lat) + (d_long * d_long)) * 1.113195e5

    def goto(self, d_north, d_east):
        current_location = self.vehicle.location.global_relative_frame
        target_location = self.get_location_metres(current_location, d_north, d_east)
        target_distance = self.get_distance_metres(current_location, target_location)
        self.vehicle.simple_goto(target_location)

        while (
            self.vehicle.mode.name == "GUIDED"
        ):  # Stop action if we are no longer in guided mode.
            remaining_distance = self.get_distance_metres(
                self.vehicle.location.global_frame, target_location
            )
            print("Distance to target: %f" % remaining_distance)
            if remaining_distance <= target_distance * 0.01:
                print("Reached target")
                break
            time.sleep(2)

    def set_ground_speed(self, speed):
        self.vehicle.groundspeed = speed
        print("Ground speed is %d" % speed)

    def finish(self):
        self.vehicle.close()
