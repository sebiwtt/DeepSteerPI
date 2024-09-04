import time
import random   # Simulate CNN input
from datetime import datetime
from picamera import PiCamera
import L298NHBridge as HBridge
import tensorflow as tf
import numpy as np
from PIL import Image

# Helper to make talking to the motors easy
def set_motor_speeds(left_speed, right_speed):
    HBridge.setMotorLeft(left_speed)
    HBridge.setMotorRight(right_speed)

def preprocess_image(image):
    img = Image.fromarray(image)
    img = img.resize((64, 64))
    img = np.array(img)
    img = img / 255.0  # Normalize the image
    return img

# Initialize variables
model = tf.keras.models.load_model('cnn_steering_model_1.0_10epochs.keras')
collecting_data = True
base_speed = 0.5    # Fixed base speed
steering_angle = 0
camera = PiCamera()
camera.resolution = (640, 480)

try:
    while True:
        image = np.empty((480, 640, 3), dtype=np.uint8)
        camera.capture(image, 'rgb')

        preprocessed_image = preprocess_image(image)
        preprocessed_image = np.expand_dims(preprocessed_image, axis=0)  # Add batch dimension
        
        right_stick, left_stick = model.predict(preprocessed_image)[0]

        left_motor_speed = left_speed + steering_angle              # Calculate motor speeds based on joystick inputs
        right_motor_speed = left_speed - steering_angle
        left_motor_speed = max(min(left_motor_speed, 1.0), -1.0)    # Capping Motor-Speed at -1 and 1 
        right_motor_speed = max(min(right_motor_speed, 1.0), -1.0)
        set_motor_speeds(left_motor_speed, right_motor_speed)       # Transmit speeds to HBridge Module      

except KeyboardInterrupt:
    print("Script interrupted")

finally:
    camera.close()
