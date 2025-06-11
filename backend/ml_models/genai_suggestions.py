import os
import secrets
import string
import requests
from pathlib import Path
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Password list (download if missing)
PASSWORD_LIST_URL = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt"
PASSWORD_LIST_PATH = Path("datasets/common_passwords.txt")

def download_password_list():
    if not PASSWORD_LIST_PATH.exists():
        print("🔽 Downloading password list...")
        os.makedirs(PASSWORD_LIST_PATH.parent, exist_ok=True)
        response = requests.get(PASSWORD_LIST_URL)
        if response.status_code == 200:
            with open(PASSWORD_LIST_PATH, "w", encoding="utf-8") as f:
                f.write(response.text)
            print("✅ Password list downloaded.")
        else:
            print("⚠️ Failed to download password list!")

def load_common_passwords():
    download_password_list()
    with open(PASSWORD_LIST_PATH, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

class PasswordSuggestionGenerator:
    def __init__(self):
        self.special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'

        # ✅ Load Mistral API key
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("Mistral AI API key is missing. Set MISTRAL_API_KEY in .env file or system environment variables.")

        # ✅ Optional SSL cert (only for local dev)
        ssl_cert_path = os.getenv("SSL_CERT_FILE")
        if ssl_cert_path:
            os.environ["SSL_CERT_FILE"] = ssl_cert_path

        self.model = "mistral-small"
        self.client = MistralClient(api_key=self.api_key)
        self.common_passwords = load_common_passwords()

    def generate_improved_password(self, original_password):
        """AI-enhanced password generation"""
        if original_password.lower() in self.common_passwords:
            print("⚠️ Warning: Common password detected.")

        ai_suggestion, ai_generated = self._generate_ai_password(original_password)

        suggestions = [
            (ai_suggestion, ai_generated),
            (self._add_complexity(original_password), False),
            (self._substitute_with_symbols(original_password), False),
            (self._randomize_case(original_password), False),
            (self._insert_special_chars(original_password), False)
        ]

        best_password, is_ai_generated = max(suggestions, key=lambda x: self._calculate_entropy(x[0]))

        if is_ai_generated:
            return f"AI-generated Password: {best_password}"
        else:
            return f"AI-generated: No | Suggested Password: {best_password}"

    def _generate_ai_password(self, password):
        """Uses Mistral AI API to generate a stronger password"""
        prompt = (
            f"Generate a strong, unpredictable password based on '{password}', "
            "keeping the length same or short, use a mix of uppercase, lowercase, numbers, Leetspeak, Hexadecimal, Octal, Base64, ROT13 Cipher, Unicode Code Points, Morse Code, MD5 Hash, SHA-256, Gibberish, Emojis, ASCII and special symbols. "
            "Do not repeat the input password. Return only one generated password, with explanation of what is the logic behind new password in very short."
        )

        try:
            response = self.client.chat(
                model=self.model,
                messages=[ChatMessage(role="user", content=prompt)]
            )
            return response.choices[0].message.content.strip(), True
        except Exception as e:
            print(f"⚠️ API Error: {e}\nFalling back to manual suggestions.")
            return self._add_complexity(password), False

    def _add_complexity(self, password):
        """Adds random characters"""
        extra_chars = ''.join(secrets.choice(
            string.ascii_letters + string.digits + self.special_chars
        ) for _ in range(min(4, max(2, len(password) // 3))))
        return password + extra_chars

    def _substitute_with_symbols(self, password):
        """Replaces common letters with symbols"""
        symbol_map = {'a': '@', 'i': '!', 'e': '3', 's': '$', 'o': '0', 't': '+'}
        return ''.join(symbol_map.get(char.lower(), char) for char in password)

    def _randomize_case(self, password):
        """Randomizes case of letters"""
        return ''.join(char.upper() if secrets.randbelow(2) else char for char in password)

    def _insert_special_chars(self, password):
        """Inserts special characters at key positions"""
        insert_positions = [len(password) // 3, len(password) // 2, -1]
        modified_password = list(password)
        for pos in insert_positions:
            modified_password.insert(pos, secrets.choice(self.special_chars))
        return ''.join(modified_password)

    def _calculate_entropy(self, password):
        """Basic entropy approximation"""
        char_set = set(password)
        return len(password) * (len(char_set) / len(password))

# 🔁 Example usage
if __name__ == "__main__":
    password_generator = PasswordSuggestionGenerator()
    print(password_generator.generate_improved_password("mypassword123"))
