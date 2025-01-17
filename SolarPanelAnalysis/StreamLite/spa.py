import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, InputLayer
from sklearn.model_selection import train_test_split

# Ignore warnings
warnings.filterwarnings('ignore')

# Streamlit UI for file upload or default dataset selection
st.title("Solar Power Data Analysis")
st.write("### Solar Plant 1 Generation Data")

# Option for uploading files or using default datasets
data_source = st.radio("Choose Data Source", ("Use Default GitHub Data", "Upload Your Own Files"))

if data_source == "Use Default GitHub Data":
    # Default GitHub URLs for datasets
    gen_1_url = "https://raw.githubusercontent.com/Sivatech24/SolarPanelDataAnalysis/256b8a98839900c42f44ee5edd14d57f18997a8d/Jupyter%20Notebook/DataSet/SolarPower/Plant_1_Generation_Data.csv"
    sens_1_url = "https://raw.githubusercontent.com/Sivatech24/SolarPanelDataAnalysis/256b8a98839900c42f44ee5edd14d57f18997a8d/Jupyter%20Notebook/DataSet/SolarPower/Plant_1_Weather_Sensor_Data.csv"
    
    # Load the data from GitHub links
    gen_1 = pd.read_csv(gen_1_url)
    sens_1 = pd.read_csv(sens_1_url)
    st.write("#### Plant Generation Data Head")
    st.write(gen_1.head())
    st.write("#### Plant Generation Data Description")
    st.write(gen_1.describe())

else:
    # File uploader for custom dataset
    gen_1_file = st.file_uploader("Upload the Solar Generation Data (CSV)", type=["csv"])
    sens_1_file = st.file_uploader("Upload the Weather Sensor Data (CSV)", type=["csv"])

    if gen_1_file is not None and sens_1_file is not None:
        # Load the uploaded files
        gen_1 = pd.read_csv(gen_1_file)
        sens_1 = pd.read_csv(sens_1_file)
        st.write("#### Plant Generation Data Head")
        st.write(gen_1.head())
        st.write("#### Plant Generation Data Description")
        st.write(gen_1.describe())
    else:
        st.warning("Please upload both files to proceed with the analysis.")

# Preprocessing and feature extraction
gen_1['DATE_TIME'] = pd.to_datetime(gen_1['DATE_TIME'], format='%d-%m-%Y %H:%M')
gen_1.set_index('DATE_TIME', inplace=True)
gen_1 = gen_1[['DAILY_YIELD']]  # We focus on forecasting DAILY_YIELD

# Normalize the data (MinMax Scaling)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(gen_1.values)

# Create train/test data
train_size = int(len(scaled_data) * 0.8)
train_data, test_data = scaled_data[:train_size], scaled_data[train_size:]

# Convert data to sequences for neural network (Sliding window approach)
def create_dataset(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step):
        X.append(data[i:i + time_step, 0])
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

time_step = 60  # Use the last 60 data points to predict the next
X_train, y_train = create_dataset(train_data, time_step)
X_test, y_test = create_dataset(test_data, time_step)

# Reshape input data for the models (samples, time steps, features)
X_train_lstm = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test_lstm = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
X_train_dense = X_train.reshape(X_train.shape[0], X_train.shape[1])
X_test_dense = X_test.reshape(X_test.shape[0], X_test.shape[1])

# Function to build LSTM model
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(InputLayer(input_shape=input_shape))  # Input layer for LSTM
    model.add(LSTM(units=50, return_sequences=True))  # First LSTM layer
    model.add(LSTM(units=50, return_sequences=False))  # Second LSTM layer
    model.add(Dense(units=1))  # Output layer for forecasting
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Function to build Dense neural network model
def build_dense_model(input_shape):
    model = Sequential([
        Dense(64, activation='relu', input_shape=(input_shape,)),  # Input layer with 64 neurons
        Dense(64, activation='relu'),   # Fourth hidden layer with 64 neurons
        Dense(32, activation='relu'),   # Fifth hidden layer with 32 neurons
        Dense(16, activation='relu'),   # Sixth hidden layer with 16 neurons
        Dense(8, activation='relu'),    # Seventh hidden layer with 8 neurons
        Dense(1, activation='sigmoid')  # Output layer with 1 output for forecasting using Sigmoid
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Choose between LSTM and Dense model
model_type = st.selectbox("Choose model type", ["LSTM", "Dense Neural Network"])

if model_type == "LSTM":
    # Build and train LSTM model
    model = build_lstm_model((X_train_lstm.shape[1], 1))
    st.write(f"Training the LSTM model with 50 epochs and batch size 32...")
    history = model.fit(X_train_lstm, y_train, epochs=50, batch_size=32, validation_data=(X_test_lstm, y_test), verbose=1)
elif model_type == "Dense Neural Network":
    # Build and train Dense neural network model
    model = build_dense_model(X_train_dense.shape[1])
    st.write(f"Training the Dense neural network model with 50 epochs and batch size 32...")
    history = model.fit(X_train_dense, y_train, epochs=50, batch_size=32, validation_data=(X_test_dense, y_test), verbose=1)

# Predict on the test set
st.write("Making Predictions...")
predicted_yield = model.predict(X_test_dense if model_type == "Dense Neural Network" else X_test_lstm)

# Invert scaling to get actual values
predicted_yield = scaler.inverse_transform(predicted_yield)
y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))

# Plotting the results
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(y_test_actual, label='True Daily Yield', color='navy')
ax.plot(predicted_yield, label='Predicted Daily Yield', color='green')
ax.legend()
ax.set_title(f'Solar Power Forecast using {model_type} Model', fontsize=17)
st.pyplot(fig)

# Show model training loss curve
fig2, ax2 = plt.subplots(figsize=(15, 5))
ax2.plot(history.history['loss'], label='Training Loss', color='blue')
ax2.plot(history.history['val_loss'], label='Validation Loss', color='orange')
ax2.legend()
ax2.set_title(f'{model_type} Model Loss Curve', fontsize=17)
st.pyplot(fig2)

# Display final model summary
st.write("Final Model Summary:")
st.text(model.summary())
