import gradio as gr
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

# Function to load data
def load_data(data_source, gen_1_file=None, sens_1_file=None):
    if data_source == "Use Default GitHub Data":
        gen_1_url = "https://raw.githubusercontent.com/Sivatech24/SolarPanelDataAnalysis/256b8a98839900c42f44ee5edd14d57f18997a8d/Jupyter%20Notebook/DataSet/SolarPower/Plant_1_Generation_Data.csv"
        sens_1_url = "https://raw.githubusercontent.com/Sivatech24/SolarPanelDataAnalysis/256b8a98839900c42f44ee5edd14d57f18997a8d/Jupyter%20Notebook/DataSet/SolarPower/Plant_1_Weather_Sensor_Data.csv"
        
        gen_1 = pd.read_csv(gen_1_url)
        sens_1 = pd.read_csv(sens_1_url)
    else:
        gen_1 = pd.read_csv(gen_1_file.name)
        sens_1 = pd.read_csv(sens_1_file.name)
    
    return gen_1, sens_1

# Preprocessing and model training function
def train_model(data_source, gen_1_file, sens_1_file, model_type, epochs, batch_size):
    gen_1, sens_1 = load_data(data_source, gen_1_file, sens_1_file)
    
    # Preprocess data
    gen_1['DATE_TIME'] = pd.to_datetime(gen_1['DATE_TIME'], format='%d-%m-%Y %H:%M')
    gen_1.set_index('DATE_TIME', inplace=True)
    gen_1 = gen_1[['DAILY_YIELD']]
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(gen_1.values)
    
    train_size = int(len(scaled_data) * 0.8)
    train_data, test_data = scaled_data[:train_size], scaled_data[train_size:]

    def create_dataset(data, time_step=1):
        X, y = [], []
        for i in range(len(data) - time_step):
            X.append(data[i:i + time_step, 0])
            y.append(data[i + time_step, 0])
        return np.array(X), np.array(y)

    time_step = 60
    X_train, y_train = create_dataset(train_data, time_step)
    X_test, y_test = create_dataset(test_data, time_step)

    X_train_lstm = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test_lstm = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
    X_train_dense = X_train.reshape(X_train.shape[0], X_train.shape[1])
    X_test_dense = X_test.reshape(X_test.shape[0], X_test.shape[1])

    if model_type == "LSTM":
        model = Sequential()
        model.add(InputLayer(input_shape=(X_train_lstm.shape[1], 1)))
        model.add(LSTM(units=50, return_sequences=True))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        history = model.fit(X_train_lstm, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test_lstm, y_test), verbose=1)
    else:
        model = Sequential([
            Dense(256, activation='relu', input_shape=(X_train_dense.shape[1],)),
            Dense(256, activation='relu'),
            Dense(128, activation='relu'),
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            Dense(16, activation='relu'),
            Dense(8, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        history = model.fit(X_train_dense, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_test_dense, y_test), verbose=1)

    predicted_yield = model.predict(X_test_dense if model_type == "Dense Neural Network" else X_test_lstm)
    predicted_yield = scaler.inverse_transform(predicted_yield)
    y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Plot results
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(y_test_actual, label='True Daily Yield', color='navy')
    ax.plot(predicted_yield, label='Predicted Daily Yield', color='green')
    ax.legend()
    ax.set_title(f'Solar Power Forecast using {model_type} Model', fontsize=17)
    
    return fig

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# Solar Power Data Analysis")
    
    with gr.Row():
        data_source = gr.Radio(["Use Default GitHub Data", "Upload Your Own Files"], label="Choose Data Source")
        gen_1_file = gr.File(label="Upload the Solar Generation Data (CSV)", file_types=["csv"])
        sens_1_file = gr.File(label="Upload the Weather Sensor Data (CSV)", file_types=["csv"])

    model_type = gr.Dropdown(["LSTM", "Dense Neural Network"], label="Choose model type")
    epochs = gr.Slider(minimum=10, maximum=100, value=50, step=10, label='Select number of epochs')
    batch_size = gr.Slider(minimum=16, maximum=128, value=32, step=16, label='Select batch size')

    output = gr.Plot(label="Model Predictions Plot")

    def run_analysis(data_source, gen_1_file, sens_1_file, model_type, epochs, batch_size):
        return train_model(data_source, gen_1_file, sens_1_file, model_type, epochs, batch_size)

    submit_btn = gr.Button("Run Analysis")
    submit_btn.click(run_analysis, inputs=[data_source, gen_1_file, sens_1_file, model_type, epochs, batch_size], outputs=output)

demo.launch()
