import hashlib
import requests

class BreachChecker:
    def __init__(self):
        self.haveibeenpwned_api = "https://api.pwnedpasswords.com/range/"
        self.headers = {'User-Agent': 'PasswordStrengthAnalyzer'}

    def check_password_breach(self, password):
        """
        Check if the password has been exposed in a data breach.
        Uses the Have I Been Pwned API (HIBP) with the k-Anonymity method.
        """
        # Hash password using SHA-1 (HIBP requires this)
        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_password[:5], sha1_password[5:]

        try:
            response = requests.get(f"{self.haveibeenpwned_api}{prefix}", headers=self.headers)
            response.raise_for_status()  # Raises an error for HTTP failures

            breached_hashes = response.text.splitlines()
            for hash_count in breached_hashes:
                hash_suffix, count = hash_count.split(':')
                if suffix == hash_suffix:
                    return {
                        'breached': True,
                        'breach_count': int(count),
                        'message': f"⚠️ Password found in {count} breaches! Consider changing it."
                    }

            return {
                'breached': False,
                'message': "✅ Password not found in known breaches. Still, use strong passwords!"
            }

        except requests.RequestException as e:
            return {
                'error': True,
                'message': f"❌ API request failed: {str(e)}",
                'breached': None
            }
