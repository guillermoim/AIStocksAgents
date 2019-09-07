import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout


def __init__():
    pass


def build_and_train(input, mem_size):

    train_dataset = np.array(input).reshape(-1,1)

    scaler = MinMaxScaler(feature_range=(0, 1))
    training_scaled = scaler.fit_transform(train_dataset)

    features_set = []
    labels = []

    for i in range(mem_size, len(training_scaled)):
        features_set.append(training_scaled[i - mem_size:i, 0])
        labels.append(training_scaled[i, 0])

    features_set, labels = np.array(features_set), np.array(labels)
    features_set = np.reshape(features_set, (features_set.shape[0], features_set.shape[1], 1))

    # Instantiate the model with Keras
    model = Sequential()

    model.add(LSTM(units=256, return_sequences=True, input_shape=(features_set.shape[1], 1)))
    model.add(Dropout(0.25))

    model.add(LSTM(units=50))
    model.add(Dropout(0.3))

    # Por ultimo, anyadimos una Capa Densa al final de modelo.
    model.add(Dense(units=1))

    model.compile(optimizer='adam', loss='mse')

    return scaler, train_dataset, labels, features_set, model


def train(scaler, train_dataset, labels_train, features_train, model, test_dataset, mem_size, iterations):

    model.fit(features_train, labels_train, epochs=iterations, batch_size=32)

    total_values = pd.concat((pd.DataFrame(train_dataset), pd.DataFrame(test_dataset)), axis=0)

    test_inputs = total_values[len(total_values) - len(test_dataset) - mem_size:].values

    test_inputs = test_inputs.reshape(-1, 1)
    test_inputs = scaler.transform(test_inputs)

    test_features = []
    for i in range(mem_size, len(test_inputs)):
        test_features.append(test_inputs[i - mem_size:i, 0])

    test_features = np.array(test_features)
    test_features = np.reshape(test_features, (test_features.shape[0], test_features.shape[1], 1))

    predictions = model.predict(test_features)
    predictions = scaler.inverse_transform(predictions)

    return predictions
