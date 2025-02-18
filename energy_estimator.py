import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib

class EnergyEstimator:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
        # Example energy consumption data (kWh per day)
        self.base_energy_consumption = {
            'rice': 5.5,
            'maize': 4.8,
            'chickpea': 3.2,
            'kidneybeans': 3.5,
            'pigeonpeas': 3.0,
            'mothbeans': 2.8,
            'mungbean': 2.9,
            'blackgram': 3.1,
            'lentil': 2.7,
            'pomegranate': 6.2,
            'banana': 7.1,
            'mango': 6.8,
            'grapes': 5.9,
            'watermelon': 4.7,
            'muskmelon': 4.5,
            'apple': 6.5,
            'orange': 5.8,
            'papaya': 5.2,
            'coconut': 7.5,
            'cotton': 4.9,
            'jute': 4.2,
            'coffee': 6.7
        }
    
    def estimate_energy_consumption(self, crop, duration_days):
        if crop not in self.base_energy_consumption:
            raise ValueError(f"No energy data available for crop: {crop}")
        
        daily_consumption = self.base_energy_consumption[crop]
        total_consumption = daily_consumption * duration_days
        
        # Add some random variation (±10%)
        variation = np.random.uniform(-0.1, 0.1)
        total_consumption *= (1 + variation)
        
        return total_consumption
    
    def get_crop_duration(self, crop):
        # Example crop durations in days
        crop_durations = {
            'rice': 120,
            'maize': 95,
            'chickpea': 100,
            'kidneybeans': 85,
            'pigeonpeas': 120,
            'mothbeans': 75,
            'mungbean': 65,
            'blackgram': 90,
            'lentil': 100,
            'pomegranate': 180,
            'banana': 300,
            'mango': 150,
            'grapes': 150,
            'watermelon': 80,
            'muskmelon': 90,
            'apple': 180,
            'orange': 240,
            'papaya': 300,
            'coconut': 365,
            'cotton': 150,
            'jute': 100,
            'coffee': 270
        }
        
        return crop_durations.get(crop, 120)  # Default to 120 days if crop not found

def main():
    estimator = EnergyEstimator()
    
    # Example usage
    crop = 'chickpea'
    duration = estimator.get_crop_duration(crop)
    energy_consumption = estimator.estimate_energy_consumption(crop, duration)
    
    print(f"Crop: {crop}")
    print(f"Growth Duration: {duration} days")
    print(f"Estimated Total Energy Consumption: {energy_consumption:.2f} kWh")
    print(f"Average Daily Consumption: {energy_consumption/duration:.2f} kWh/day")

if __name__ == "__main__":
    main()