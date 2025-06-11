import re
import os

class PasswordStrengthModel:
    def __init__(self, rockyou_path=r"C:\\Windows\\System32\\password-strength-analyzer\\datasets\\rockyou.txt"):
        self.rockyou_path = rockyou_path
        self.common_passwords = self._load_common_passwords()

    def _load_common_passwords(self):
        """ Load RockYou dataset into a set for fast lookup. """
        try:
            with open(self.rockyou_path, encoding="latin-1") as file:
                return {line.strip() for line in file}
        except FileNotFoundError:
            print("Warning: RockYou dataset not found! Dictionary attack results may be inaccurate.")
            return set()

    def extract_features(self, password):
        """ Extracts characteristics of the password. """
        return {
            "length": len(password),
            "uppercase": any(c.isupper() for c in password),
            "lowercase": any(c.islower() for c in password),
            "digits": any(c.isdigit() for c in password),
            "special_chars": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        }

    def estimate_time_to_crack(self, password):
        """ Computes estimated time to crack the password using multiple attack methods. """
        brute_force = self._estimate_brute_force_time(password)
        dictionary_attack = self._estimate_dictionary_attack_time(password)
        rainbow_table = self._estimate_rainbow_table_time(password)
        offline_crack = self._estimate_offline_crack_time(password, 'bcrypt')

        return {
            "Brute Force": self._format_time(brute_force),
            "Dictionary Attack": self._format_time(dictionary_attack),
            "Rainbow Table Attack": self._format_time(rainbow_table),
            "Offline Cracking (bcrypt)": self._format_time(offline_crack),
        }

    def _estimate_brute_force_time(self, password):
        """ Estimates time to crack using brute force. """
        char_sets = 0
        if any(c.islower() for c in password):
            char_sets += 26  # a-z
        if any(c.isupper() for c in password):
            char_sets += 26  # A-Z
        if any(c.isdigit() for c in password):
            char_sets += 10  # 0-9
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            char_sets += 32  # Special chars

        total_combinations = char_sets ** len(password)
        guesses_per_second = 300_000_000_000  # High-end GPU speed

        return total_combinations / guesses_per_second

    def _estimate_dictionary_attack_time(self, password):
        """ Checks if the password exists in RockYou dataset. """
        if password in self.common_passwords:
            return 0.001  # Instantly compromised
        else:
            # If password is not in RockYou, assume a dictionary attack is slower
            attack_speed = 100_000_000  # Dictionary attempts per second
            return len(password) * 1_000_000 / attack_speed  # Adjusted time estimation

    def _estimate_rainbow_table_time(self, password):
        """ Estimates time to crack using a rainbow table. """
        if len(password) < 8:
            return 0.01  # Instantly compromised for weak hashes
        return 1_000  # Assume it takes at least some time for strong hashes

    def _estimate_offline_crack_time(self, password, hash_type='bcrypt'):
        """ Estimates offline cracking time based on hashing algorithm. """
        hash_speeds = {
            'md5': 1_000_000_000,  # Hashes per second
            'sha256': 500_000_000,
            'bcrypt': 300,  # Bcrypt is slow
            'argon2': 50  # Argon2id is even slower
        }
        total_combinations = 26 ** len(password)
        guesses_per_second = hash_speeds.get(hash_type, 1_000_000)
        return total_combinations / guesses_per_second

    def _format_time(self, seconds):
        """ Converts seconds into a human-readable format. """
        if seconds < 0.001:
            return "Instantly compromised"
        elif seconds < 1:
            return f"{seconds * 1000:.2f} milliseconds"
        elif seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.2f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.2f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.2f} days"
        else:
            return f"{seconds/31536000:.2f} years"
