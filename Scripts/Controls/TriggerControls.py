import os
import csv
import time
from inputs import get_gamepad
from datetime import datetime
from picamera2 import Picamera2, Preview
import L298NHBridge as HBridge

#----- GLOBALS -----

running = True
collecting_data = False

#----- GLOBALS -----

def stop_motors():
    HBridge.setMotorLeft(0)
    HBridge.setMotorRight(0)
    HBridge.exit()

def collect_data():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')
    image_path = f'training_data/{timestamp}.jpg'
    picam2.capture_file(image_path)
    print(f"Saved image under {image_path}")
    #csv_writer.writerow([timestamp, image_path, left_stick, right_stick])
    #time.sleep(0.1)  # Adjust the sleep duration as necessary 

def normalize_trigger(value):
    normalized_value = value / 255.0
    return normalized_value

def normalize(value):
    if value > 1:
        return 1
    elif value < -1:
        return -1
    else:
        return value

def set_motor_speeds(left_speed, right_speed):
    HBridge.setMotorLeft(left_speed)
    HBridge.setMotorRight(right_speed)

def get_gamepad_data(last_left_trigger, last_right_trigger):
    events = get_gamepad()
    left_trigger_value = last_left_trigger
    right_trigger_value = last_right_trigger

    for event in events:

        if event.ev_type == "Key" and event.code == "BTN_SOUTH" and event.state == 1:  # X-Button
                global collecting_data 
                collecting_data = not collecting_data
                if collecting_data:
                    print("Data collection started")
                else:
                    print("Data collection stopped")

        elif event.ev_type == "Key" and event.code == "BTN_WEST" and event.state == 1: # Square-Button
            print("Exiting") 
            global running 
            running = False

        if event.ev_type == 'Absolute':

            if event.code == 'ABS_Z':  # Left trigger
                left_trigger_value = normalize_trigger(event.state)
                #print(left_trigger_value)

            elif event.code == 'ABS_RZ':  # Right trigger
                right_trigger_value = normalize_trigger(event.state)
                #print(right_trigger_value)
 
    return left_trigger_value, right_trigger_value

#---------- MAIN Program ----------

if not os.path.exists('training_data'):
    os.makedirs('training_data')

csv_file = open('training_data/data_log.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'image_path', 'left_speed', 'right_speed', 'steering_angle'])

picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

try:
    last_left_trigger = 0
    last_right_trigger = 0

    while running:
        
        left_trigger, right_trigger = get_gamepad_data(last_left_trigger, last_right_trigger)

        # Update the last known trigger values
        last_left_trigger = left_trigger
        last_right_trigger = right_trigger

        # Normalize motor speeds to be within -1 to 1
        left_motor_speed = max(min(last_left_trigger, 1), -1)
        right_motor_speed = max(min(last_right_trigger, 1), -1)

        print(f'Left Motor: {left_motor_speed}, Right Motor: {right_motor_speed}')

        # Set the motor speeds using the HBridge interface
        set_motor_speeds(left_motor_speed, right_motor_speed)

        # For debugging purposes
        #print(f'Base Speed: {base_speed}, Steering: {left_joystick_x}')
        #print(f'Left Motor: {left_motor_speed}, Right Motor: {right_motor_speed}')

        if collecting_data:
            collect_data()
            
except KeyboardInterrupt:
    print("Data collection interrupted")
    
finally:
    stop_motors()
    picam2.stop()
    csv_file.close()