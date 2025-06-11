# tests/test_genai_suggestions.py
import unittest
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.ml_models.genai_suggestions import PasswordSuggestionGenerator

class TestPasswordSuggestionGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = PasswordSuggestionGenerator()
    
    def test_generate_improved_password(self):
        test_cases = [
            "summer2024",
            "password123",
            "qwerty"
        ]
        
        for original_password in test_cases:
            improved_password = self.generator.generate_improved_password(original_password)
            
            # Assertions
            self.assertNotEqual(original_password, improved_password, 
                                f"Failed to improve password: {original_password}")
            
            # Check complexity improvements
            self.assertTrue(len(improved_password) > len(original_password), 
                            "Improved password should be longer")
            
            # Check for character diversity
            self.assertTrue(any(c.isupper() for c in improved_password), 
                            "Improved password should have uppercase letters")
            self.assertTrue(any(c.isdigit() for c in improved_password), 
                            "Improved password should have digits")
            self.assertTrue(any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in improved_password), 
                            "Improved password should have special characters")
    
    def test_entropy_calculation(self):
        test_passwords = [
            "simple",
            "Summer2024",
            "C0mpl3x!P@ssw0rd"
        ]
        
        entropies = [
            self.generator._calculate_entropy(pwd) for pwd in test_passwords
        ]
        
        # Ensure entropy increases with complexity
        self.assertTrue(
            entropies[0] < entropies[1] < entropies[2], 
            "Entropy calculation should reflect password complexity"
        )
    
    def test_symbol_substitution(self):
        original = "password"
        substituted = self.generator._substitute_with_symbols(original)
        
        self.assertNotEqual(original, substituted, 
                            "Symbol substitution failed")
    
    def test_case_randomization(self):
        original = "password"
        randomized = self.generator._randomize_case(original)
        
        self.assertNotEqual(original, randomized, 
                            "Case randomization failed")
        self.assertEqual(len(original), len(randomized), 
                         "Case randomization changed password length")

if __name__ == '__main__':
    unittest.main() 
