import os
import csv
import time
from inputs import get_gamepad
import threading
from datetime import datetime
from picamera2 import Picamera2, Preview
import L298NHBridge as HBridge

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

def control_robot(left_stick, right_stick):
    dead_zone = 0.1
    
    if abs(left_stick) < dead_zone:
        left_stick = 0
    if abs(right_stick) < dead_zone:
        right_stick = 0

    exponent = 2
    left_stick = left_stick ** exponent if left_stick >= 0 else -(abs(left_stick) ** exponent)
    right_stick = right_stick ** exponent if right_stick >= 0 else -(abs(right_stick) ** exponent)

    left_motor_speed = left_stick + right_stick
    right_motor_speed = left_stick - right_stick

    left_motor_speed = normalize(left_motor_speed)
    right_motor_speed = normalize(right_motor_speed)

    set_motor_speeds(left_motor_speed, right_motor_speed)

if not os.path.exists('training_data'):
    os.makedirs('training_data')

csv_file = open('training_data/data_log.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'image_path', 'left_speed', 'right_speed', 'steering_angle'])

collecting_data = False
left_stick = 0
right_stick = 0
running = True

picam2 = Picamera2()
config = picam2.create_still_configuration()
picam2.configure(config)
picam2.start()

def collect_data():
    global collecting_data
    global running
    while running:
        print("thraed running")
        if collecting_data:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')
            image_path = f'training_data/{timestamp}.jpg'
            picam2.capture_file(image_path)
            print(f'Captured image: {image_path}')
            #csv_writer.writerow([timestamp, image_path, speed, steering_angle])
            time.sleep(0.1) 
        else:
            time.sleep(0.01)

data_collection_thread = threading.Thread(target=collect_data)
data_collection_thread.start()

try:
    while running:
        events = get_gamepad()
        for event in events:
            if event.ev_type == "Key" and event.code == "BTN_SOUTH" and event.state == 1:  # X-Button
                collecting_data = not collecting_data
                if collecting_data:
                    print("Data collection started")
                else:
                    print("Data collection stopped")

            elif event.ev_type == "Key" and event.code == "BTN_WEST" and event.state == 1: # Square-Button
                running = False
            
            if event.ev_type == "Absolute":

                if event.code == "ABS_Y":        
                    left_stick = -(event.state - 128) / 127   # Normalize to range [-1, 1]

                elif event.code == "ABS_RX":                
                    right_stick = (event.state - 128) / 127  # Normalize to range [-1, 1]

                elif event.code == 'ABS_Z':  # Left trigger
                    print(f'Left Trigger: {event.state}')

                elif event.code == 'ABS_RZ':  # Right trigger
                    print(f'Right Trigger: {event.state}')

            control_robot(left_stick, right_stick) 

except KeyboardInterrupt:
    print("Data collection interrupted")
    
finally:
    data_collection_thread.join()
    HBridge.setMotorLeft(0)
    HBridge.setMotorRight(0)
    HBridge.exit()
    picam2.stop()
    csv_file.close()