# train_model.py
"""
This script loads extracted network features from multiple CSV files,
combines them into one dataset, creates dummy labels, trains a simple neural network,
and saves the trained model.
"""

import glob
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping

# 1. Use glob to find and combine all CSV files
csv_files = glob.glob("FEATURES/ns3_simulation-*.csv")
print(f"Found CSV files: {csv_files}")

dataframes = []
for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Combine all DataFrames into one
data = pd.concat(dataframes, ignore_index=True)
print("Combined data shape:", data.shape)

# 2. Create dummy labels
# Here, we'll assume that if the 'Protocol' is 6 (TCP), we mark it as "normal" (0)
# and everything else as "attack" (1)
data['label'] = data['Protocol'].apply(lambda x: 0 if x == 6 else 1)

# 3. Select features for the model
# For this simple example, we'll use only 'Packet Length' as our feature
X = data[['Packet Length']].values
y = data['label'].values

# 4. Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Build a simple neural network model
model = Sequential([
    Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.5),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')  # For binary classification
])

# 6. Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 7. Train the model with early stopping
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
history = model.fit(X_train, y_train, epochs=50, batch_size=16, validation_split=0.2, callbacks=[early_stopping])

# 8. Evaluate the model on the test set
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {accuracy:.2f}")

# 9. Save the trained model to a file
model.save("intrusion_model.h5")
print("Model saved as intrusion_model.h5")
