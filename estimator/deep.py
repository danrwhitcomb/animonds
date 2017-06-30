from keras.layers import Dense
from keras.layers.core import Dropout
from keras.layers.recurrent import LSTM
from keras.layers.advanced_activations import LeakyReLU
from keras.models import Sequential
from keras.optimizers import Adam

RELU_E = 0.001
DROPOUT = 0.5

def deep_estimator(input_dim, output_dim, lr, epsilon=RELU_E, dropout=DROPOUT):
    model = Sequential([
        Dense(64, input_dim = input_dim),
        LeakyReLU(epsilon),
        Dropout(dropout),
        Dense(128, input_dim = 64),
        LeakyReLU(epsilon),
        Dropout(epsilon),
        Dense(256, input_dim = 128),
        LeakyReLU(RELU_E),
        Dropout(epsilon),
        Dense(96, input_dim = 256),
        LeakyReLU(epsilon),
        Dense(output_dim, input_dim = 96)
    ])

    optimizer = Adam(lr)
    model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['accuracy'])

    return model

def recurrent_estimator(input_dim, output_dim, lr, dropout=DROPOUT):

    model = Sequential()
    model.add(LSTM(64, input_shape=input_dim, return_sequences=True, dropout=dropout))
    model.add(LSTM(32, return_sequences=True, dropout=dropout))
    model.add(LSTM(output_dim, dropout=dropout))

    optimizer = Adam(lr)
    model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['accuracy'])

    return model
