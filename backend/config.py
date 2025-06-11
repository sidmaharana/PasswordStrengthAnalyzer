# backend/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here')
    DEBUG = True
    
    # Dataset paths
    ROCKYOU_DATASET = os.path.join('..', 'datasets', 'rockyou_cleaned.txt')
    COMMON_PASSWORDS = os.path.join('..', 'datasets', 'common_passwords.txt')
    
    # Model paths
    MODEL_SAVE_PATH = os.path.join('ml_models', 'password_strength_model.joblib')
    
    # Breach checking configuration
    HAVEIBEENPWNED_API = "https://api.pwnedpasswords.com/range/"