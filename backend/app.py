from flask import Flask, render_template, request, jsonify
from ml_models.password_strength_model import PasswordStrengthModel
from ml_models.genai_suggestions import PasswordSuggestionGenerator
from utils.breach_checker import BreachChecker

app = Flask(__name__, 
            static_folder='../frontend/static', 
            template_folder='../frontend/templates')

# Initialize models
strength_model = PasswordStrengthModel()
suggestion_generator = PasswordSuggestionGenerator()
breach_checker = BreachChecker()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze_password', methods=['POST'])
def analyze_password():
    password = request.json.get('password', '')

    # Comprehensive password analysis
    breach_status = breach_checker.check_password_breach(password)  # Get breach status

    results = {
        'strength_features': strength_model.extract_features(password),
        'time_to_crack': strength_model.estimate_time_to_crack(password),
        'suggested_password': suggestion_generator.generate_improved_password(password),
        'breach_status': breach_status  # Include breach status in response
    }

    return jsonify(results)  # Send JSON response to frontend

if __name__ == '__main__':
    app.run(debug=True)
