import os
import csv
import time
from inputs import get_gamepad
from datetime import datetime
#from picamera import PiCamera
import L298NHBridge as HBridge

# Helper to make talking to the motors easy
def set_motor_speeds(left_speed, right_speed):
    HBridge.setMotorLeft(left_speed)
    HBridge.setMotorRight(right_speed)

# Create a directory to save images and a csv file to write the raw data
if not os.path.exists('training_data'):
    os.makedirs('training_data')

csv_file = open('training_data/data_log.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'image_path', 'left_speed', 'right_speed', 'steering_angle'])

# Initialize variables
collecting_data = False
speed = 0
steering_angle = 0
running = True
#camera = PiCamera()
#camera.resolution = (640, 480)

try:
    while running:
        events = get_gamepad()
        for event in events:
            if event.ev_type == "Key" and event.code == "BTN_SOUTH" and event.state == 1:  # X-Button
                #collecting_data = not collecting_data
                if collecting_data:
                    print("Data collection started")
                else:
                    print("Data collection stopped")

            elif event.ev_type == "Key" and event.code == "BTN_WEST" and event.state == 1: # Square-Button
                running = False
            
            if event.ev_type == "Absolute":

                if event.code == "ABS_Y":        
                    speed = -(event.state - 128) / 127   # Normalize to range [-1, 1]
                    #print(f"Speed: {speed}") 

                elif event.code == "ABS_RX":                
                    steering_angle = (event.state - 128) / 127  # Normalize to range [-1, 1]
                    #print(f"Steering angle: {steering_angle}")

            left_motor_speed = speed + steering_angle              # Calculate motor speeds based on joystick inputs
            right_motor_speed = speed - steering_angle

            left_motor_speed = max(min(left_motor_speed, 1.0), -1.0)    # Capping Motor-Speed at -1 and 1 
            right_motor_speed = max(min(right_motor_speed, 1.0), -1.0)

            set_motor_speeds(left_motor_speed, right_motor_speed)       # Transmit speeds to HBridge Module
            print(f"RightSpeed: {right_motor_speed}") 
            print(f"LeftSpeed: {left_motor_speed}") 

            # Capture and save image, write log-data to csv
            if collecting_data:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')
                image_path = f'training_data/{timestamp}.jpg'
                camera.capture(image_path)
                csv_writer.writerow([timestamp, image_path, left_motor_speed, right_motor_speed, steering_angle])
                time.sleep(0.1)  

except KeyboardInterrupt:
    print("Data collection interrupted")
    
finally:
    HBridge.setMotorLeft(0)
    HBridge.setMotorRight(0)
    HBridge.exit()
    #camera.close()
    #csv_file.close()