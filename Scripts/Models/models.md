
# 1.0 -> Basic CNN Architecture

```

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(256, activation='relu'),
    Dense(2)  # Output layer for both right_stick and left_stick
])

model.compile(optimizer='adam', loss='mean_squared_error')
model.summary()
```

- 10 Epochs -> Validation Loss: 0.04533550143241882

---

# 2.0 -> Shallow CNN with Fewer Filters

```
model = Sequential([
    Conv2D(16, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D((2, 2)),
    
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Flatten(),
    Dense(128, activation='relu'),
    Dense(2)  # Output layer for right_stick and left_stick
])
```

- 10 Epochs -> Validation Loss: 0.06435004621744156

---

# 3.0 -> Deeper Network with Dropout

```
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D((2, 2)),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.5),  # Dropout to reduce overfitting
    Dense(2)  # Output layer
])
```

- 10 Epochs -> Validation Loss: 0.04233463108539581

---

# 4.0 -> Wider Network with Larger Filters

```
model = Sequential([
    Conv2D(64, (5, 5), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D((2, 2)),
    
    Conv2D(128, (5, 5), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(256, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Flatten(),
    Dense(512, activation='relu'),
    Dense(2)  # Output layer
])
```

- 10 Epochs -> Validation Loss: 0.04139081761240959
- 20 Epochs → Validation Loss: 0.04411858320236206

---

# 5.0 -> Deeper Network with Batch Normalization

```
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D((2, 2)),
    
    Conv2D(64, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    
    Conv2D(128, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    
    Flatten(),
    Dense(256, activation='relu'),
    Dense(2)  # Output layer
])

```

- 10 Epochs -> Validation Loss: 6.558771133422852 → Clear Overfit

---

# 6.0 -> Very Deep Network with Small Filters

```
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(64, (3, 3), activation='relu'),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(128, (3, 3), activation='relu'),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Flatten(),
    Dense(512, activation='relu'),
    Dense(2)  # Output layer
])
```

- 10 Epochs -> Validation Loss: 0.0424273684620857242
- 15 Epochs -> Validation Loss: 0.043455980718135834

---

# 7.0 -> Shallow with Global Average Pooling

```
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D((2, 2)),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(128, (3, 3), activation='relu'),
    GlobalAveragePooling2D(),  # Global average pooling instead of flattening
    
    Dense(128, activation='relu'),
    Dense(2)  # Output layer
])
```

- 10 Epochs → Validation Loss: 0.08315066993236542
- 15 Epochs → Validation Loss 0.06012900546193123
- 20 Epochs → Validation Loss 0.04334508255124092

---

# 8.0 -> Very Shallow Network for Testing Simplicity

```
model = Sequential([
    Conv2D(16, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D((2, 2)),
    
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Flatten(),
    Dense(64, activation='relu'),
    Dense(2)  # Output layer
])
```

- 10 Epochs -> Validation Loss: 0.05076305568218231

---

# 9.0 -> Network with Separable Convolutions

```
from tensorflow.keras.layers import SeparableConv2D

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
```

- 10 Epochs -> Validation Loss: 0.07146449387073517

---