import time
import random   # Simulate CNN input
from datetime import datetime
from picamera import PiCamera
import L298NHBridge as HBridge

# Helper to make talking to the motors easy
def set_motor_speeds(left_speed, right_speed):
    HBridge.setMotorLeft(left_speed)
    HBridge.setMotorRight(right_speed)

# Initialize variables
collecting_data = True
base_speed = 0.5    # Fixed base speed
steering_angle = 0
camera = PiCamera()
camera.resolution = (640, 480)

try:
    while True:
        # Simulate receiving steering angle from CNN
        steering_angle = random.uniform(-1, 1)  # Replace this with actual CNN output

        left_motor_speed = left_speed + steering_angle              # Calculate motor speeds based on joystick inputs
        right_motor_speed = left_speed - steering_angle
        left_motor_speed = max(min(left_motor_speed, 1.0), -1.0)    # Capping Motor-Speed at -1 and 1 
        right_motor_speed = max(min(right_motor_speed, 1.0), -1.0)
        set_motor_speeds(left_motor_speed, right_motor_speed)       # Transmit speeds to HBridge Module      

except KeyboardInterrupt:
    print("Script interrupted")

finally:
    camera.close()
