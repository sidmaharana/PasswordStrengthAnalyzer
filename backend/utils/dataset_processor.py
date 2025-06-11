# backend/utils/dataset_processor.py
import pandas as pd
import re

def clean_rockyou_dataset(input_path, output_path):
    """
    Clean and preprocess RockYou dataset
    """
    # Read raw dataset
    with open(input_path, 'r', encoding='latin-1') as f:
        passwords = f.readlines()
    
    # Clean and process passwords
    cleaned_passwords = []
    for pwd in passwords:
        pwd = pwd.strip()
        
        # Basic cleaning
        if len(pwd) < 8 or len(pwd) > 64:
            continue
        
        # Remove non-printable characters
        pwd = ''.join(char for char in pwd if char.isprintable())
        
        # Add complexity score
        complexity = calculate_complexity(pwd)
        
        cleaned_passwords.append({
            'password': pwd,
            'length': len(pwd),
            'complexity': complexity
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(cleaned_passwords)
    
    # Categorize strength
    df['strength_label'] = pd.cut(
        df['complexity'], 
        bins=[0, 10, 20, 30, 100], 
        labels=['Weak', 'Medium', 'Strong', 'Very Strong']
    )
    
    # Save processed dataset
    df.to_csv(output_path, index=False)
    print(f"Processed dataset saved to {output_path}")

def calculate_complexity(password):
    """
    Calculate password complexity score
    """
    complexity = 0
    
    # Length complexity
    complexity += min(len(password), 10)
    
    # Character type complexity
    if re.search(r'[A-Z]', password):
        complexity += 2
    if re.search(r'[a-z]', password):
        complexity += 2
    if re.search(r'\d', password):
        complexity += 2
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        complexity += 3
    
    # Unique character complexity
    unique_chars = len(set(password))
    complexity += min(unique_chars, 5)
    
    return complexity

if __name__ == '__main__':
    clean_rockyou_dataset(
        'datasets/rockyou.txt', 
        'datasets/rockyou_cleaned.txt'
    ) 
