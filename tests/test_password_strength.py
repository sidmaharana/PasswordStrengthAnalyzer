# tests/test_password_strength.py
import unittest
from backend.ml_models.password_strength_model import PasswordStrengthModel

class TestPasswordStrengthModel(unittest.TestCase):
    def setUp(self):
        self.model = PasswordStrengthModel()
    
    def test_password_features(self):
        password = "Summer2024!"
        features = self.model.extract_features(password)
        
        self.assertTrue(features['has_uppercase'])
        self.assertTrue(features['has_lowercase'])
        self.assertTrue(features['has_digit'])
        self.assertTrue(features['has_special_char'])
    
    def test_time_to_crack(self):
        weak_password = "password123"
        strong_password = "C0mpl3x!P@ssw0rd2024"
        
        weak_time = self.model.estimate_time_to_crack(weak_password)
        strong_time = self.model.estimate_time_to_crack(strong_password)
        
        self.assertLess(float(weak_time.split()[0]), float(strong_time.split()[0]))

# tests/test_genai_suggestions.py
import unittest
from backend.ml_models.genai_suggestions import PasswordSuggestionGenerator

class TestPasswordSuggestionGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = PasswordSuggestionGenerator()
    
    def test_generate_improved_password(self):
        original = "Summer2024"
        improved = self.generator.generate_improved_password(original)
        
        self.assertNotEqual(original, improved)
        self.assertTrue(len(improved) > len(original))
    
    def test_entropy_calculation(self):
        passwords = ["simple", "C0mpl3x!P@ss", "VeryC0mpl3xP@ssw0rd!"]
        entropies = [
            self.generator._calculate_entropy(pwd) for pwd in passwords
        ]
        
        # Ensure entropy increases with complexity
        self.assertTrue(entropies[0] < entropies[1] < entropies[2])

if __name__ == '__main__':
    unittest.main() 
