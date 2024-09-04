import os
import csv
import time
from datetime import datetime
from picamera2 import Picamera2
import L298NHBridge as HBridge
import shutil
from PIL import Image
import numpy as np
import tensorflow as tf

#--------- Helper Functions ---------

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

def preprocess_image(image):
    img = Image.fromarray(image)
    img = img.resize((64, 64))  # Resize to match CNN input
    img = np.array(img)
    img = img / 255.0  # Normalize image
    return img

#--------- Global Variables ---------

running = True

#----------- Main Program -----------

picam2 = Picamera2()

config = picam2.create_still_configuration(
    main={"size": (3280, 2464)},
    controls={"ExposureTime": 10000, "AnalogueGain": 2.0},
    buffer_count=1
)
picam2.configure(config)
picam2.start()

# Load the pre-trained model
model = tf.keras.models.load_model('cnn_steering_model_1.0_10epochs.keras')

try:
    while running:
        # Capture image from the camera
        image_array = picam2.capture_array()
        image = preprocess_image(image_array)  # Preprocess image for the model
        image = np.expand_dims(image, axis=0)  # Add batch dimension

        # Predict left and right stick values using the model
        predicted_sticks = model.predict(image)[0]  # Model predicts [right_stick, left_stick]
        right_stick, left_stick = predicted_sticks

        # Control the robot with the predicted values
        control_robot(left_stick, right_stick)

        time.sleep(0.1)  # Adjust the loop time as needed

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    HBridge.setMotorLeft(0)
    HBridge.setMotorRight(0)
    HBridge.exit()
    picam2.stop()
    csv_file.close()
