
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.layers import LSTM, Dense
from keras.models import Sequential
from keras.optimizers import Adam

def load_data(file_path):
    """Loads data from a CSV file and returns features (x) and target (y)."""
    try:
        df = pd.read_csv(file_path) 
        # Assuming the features and target columns are known
        # Adjusting column names as needed
        features = ['Days_Since_High_Last', 'Days_Since_Low_Last', 'Current_Diff_From_High', 'Current_Diff_From_Low']
        target = ['%_Diff_From_High_Next', '%_Diff_From_Low_Next']
        x = df[features].values
        y = df[target].values
        return x, y
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None, None  # Explicitly returning None for both values on error

dataset = pd.read_csv("/content/metrices_df.csv")

dataset.head(3)

dataset.isnull().sum()

dataset = dataset[["Days_Since_High_Last_7_Days", "%_Diff_From_High_Last_7_Days", "Days_Since_Low_Last_7_Days", "%_Diff_From_Low_Last_7_Days", "%_Diff_From_High_Next_5_Days", "%_Diff_From_Low_Next_5_Days"]]

dataset.isnull().sum()

dataset.fillna(0, inplace=True)

dataset.head()

x = dataset.iloc[:, :-2]
y = dataset.iloc[:, -2:]

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
x = scaler.fit_transform(x)

x = x.reshape((x.shape[0], 1, x.shape[1]))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

def train_model(X_train, y_train, X_test, y_test):
    """Train the LSTM model and evaluate its performance."""
    # Creating LSTM model
    model = Sequential()
    model.add(LSTM(units=64, return_sequences=False, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(2))  # Two output variables
    model.compile(optimizer='adam', loss='mse')

    # Training the model
    model.fit(x_train, y_train, epochs=50, batch_size=32, verbose=1)

    # Evaluating the model
    mse = model.evaluate(x_test, y_test, verbose=0)
    print(f'Model MSE: {mse}')
    return model, mse

def predict_outcomes(model, new_data):
    """Make predictions based on new input values."""
    new_data = scaler.transform(new_data)
    new_data = np.array(new_data).reshape((1, 1, len(new_data)))
    predictions = model.predict(new_data)
    return predictions[0]

if __name__ == "__main__":
    # Load data
    x, y = load_data("metrices_df.csv")

    # Scale features
    x_scaled, scaler = scale_data(x)

    # Reshape data for LSTM
    x_reshaped = reshape_data(x_scaled)

    # Splitting the dataset into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(x_reshaped, y, test_size=0.2, random_state=42)

    # Training the model
    model, mse = train_model(x_train, y_train, x_test, y_test)

    # Example new input for prediction
    new_input = [1, 0.5, 2, -0.5]
    predicted_outcomes = predict_outcomes(model, new_input)

    print(f'Predicted %_Diff_From_High_Next: {predicted_outcomes[0]}, %_Diff_From_Low_Next: {predicted_outcomes[1]}')

