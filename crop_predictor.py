import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import serial
import time

class CropPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
    def load_data(self, file_path):
        self.data = pd.read_csv(file_path)
        return self.data
    
    def preprocess_data(self):
        X = self.data.drop('label', axis=1)
        y = self.data['label']
        
        # Scale the features
        X_scaled = self.scaler.fit_transform(X)
        
        return train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    def train_model(self):
        X_train, X_test, y_train, y_test = self.preprocess_data()
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy:.2f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
    def save_model(self, model_path='crop_predictor_model.pkl'):
        if self.model is not None:
            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, 'scaler.pkl')
            print(f"Model saved to {model_path}")
    
    def predict_crop(self, features):
        if self.model is None:
            raise Exception("Model not trained yet!")
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)
        probabilities = self.model.predict_proba(features_scaled)
        
        return prediction[0], probabilities[0]

def main():
    predictor = CropPredictor()
    
    # Load and train model
    data = predictor.load_data('Crop_recommendation.csv')
    predictor.train_model()
    predictor.save_model()
    
    # Initialize serial connection with Arduino
    try:
        arduino = serial.Serial('COM3', 9600, timeout=1)  # Adjust COM port as needed
        time.sleep(2)  # Wait for connection to establish
        
        # Read sensor values from Arduino
        if arduino.in_waiting:
            sensor_data = arduino.readline().decode('utf-8').strip().split(',')
            if len(sensor_data) >= 7:  # Make sure we have all required values
                N = float(sensor_data[0])  # N value
                P = float(sensor_data[1])  # P value
                K = float(sensor_data[2])  # K value
                temperature = float(sensor_data[3])
                humidity = float(sensor_data[4])
                ph = float(sensor_data[5])
                rainfall = float(sensor_data[6])
                
                sample_features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
                prediction, probabilities = predictor.predict_crop(sample_features)
                print(f"\nPredicted crop: {prediction}")
                print("Prediction probabilities:")
                for crop, prob in zip(predictor.model.classes_, probabilities):
                    print(f"{crop}: {prob:.2f}")
        
        arduino.close()
    except serial.SerialException as e:
        print(f"Error connecting to Arduino: {e}")
        print("Using default values for testing:")
        # Fallback to default values if Arduino connection fails
        sample_features = np.array([[26,73,21,31.33170829,57.97429171,4.946263888,161.7820226]])
        prediction, probabilities = predictor.predict_crop(sample_features)
        print(f"\nPredicted crop: {prediction}")
        print("Prediction probabilities:")
        for crop, prob in zip(predictor.model.classes_, probabilities):
            print(f"{crop}: {prob:.2f}")

if __name__ == "__main__":
    main()