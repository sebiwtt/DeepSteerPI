import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow.keras.layers import SeparableConv2D

# Load the CSV file
data = pd.read_csv('training_data/data_log.csv')

# Split into training and validation sets
train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

# Image size and batch size
IMG_HEIGHT, IMG_WIDTH = 64, 64
BATCH_SIZE = 32

def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img = np.array(img)
    img = img / 255.0  # Normalize the image
    return img


# Data generators
def data_generator(data, batch_size, is_training):
    while True:
        batch_data = data.sample(batch_size)
        images = []
        right_stick_values = []
        left_stick_values = []
        for index, row in batch_data.iterrows():
            image_path = row['image_path']
            right_stick = row['right_stick']
            left_stick = row['left_stick']
            image = preprocess_image(image_path)
            images.append(image)
            right_stick_values.append(right_stick)
            left_stick_values.append(left_stick)
        
        yield np.array(images), np.array([right_stick_values, left_stick_values]).T 


train_generator = data_generator(train_data, BATCH_SIZE, True)
val_generator = data_generator(val_data, BATCH_SIZE, False)

model = Sequential([
    SeparableConv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D((2, 2)),
    
    SeparableConv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    SeparableConv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Flatten(),
    Dense(256, activation='relu'),
    Dense(2)  # Output layer
])

model.compile(optimizer='adam', loss='mean_squared_error')
model.summary()

# Calculate steps per epoch
train_steps = len(train_data) // BATCH_SIZE
val_steps = len(val_data) // BATCH_SIZE

history = model.fit(
    train_generator,
    steps_per_epoch=train_steps,
    epochs=10, 
    validation_data=val_generator,
    validation_steps=val_steps
)

val_loss = model.evaluate(val_generator, steps=val_steps)
print(f'Validation Loss: {val_loss}')

model.save('cnn_steering_model_9.0_10epochs.keras')

# ----------- Visualization of Metrics -----------

# Plot the training and validation loss
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()