import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class WorkloadPredictor:
    def __init__(self, input_shape):
        self.model = self._build_model(input_shape)
    
    def _build_model(self, input_shape):
        model = Sequential([
            LSTM(64, input_shape=input_shape, return_sequences=True),
            LSTM(32),
            Dense(16, activation='relu'),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        return model
    
    def train(self, X, y, epochs=100):
        return self.model.fit(X, y, epochs=epochs, validation_split=0.2)
    
    def predict(self, X):
        return self.model.predict(X)