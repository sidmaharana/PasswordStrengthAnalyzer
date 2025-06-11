# 🔐 Password Strength Analyzer

An intelligent tool for analyzing the strength of passwords using traditional and AI-powered methods. It evaluates password robustness, detects weaknesses, and suggests stronger alternatives using machine learning and GenAI (Mistral API).

---

## 📁 Project Structure

```
password-strength-analyzer/
├── backend/
│   ├── app.py                  # Flask app entry point
│   ├── config.py               # Configuration file
│   ├── ml_models/              # ML models & suggestion engines
│   │   ├── password_strength_model.py
│   │   ├── genai_suggestions.py
│   │   └── .env                # API keys and SSL path
├── frontend/                   # Frontend code (React/HTML/CSS)
├── tests/                      # Test cases and mock inputs
├── venv/                       # Virtual environment (excluded from Git)
├── password_strength_model.joblib
├── requirements.txt
└── README.md
```

---

## 🚀 Features

- ✅ Machine Learning model to score password strength
- ✅ Dictionary-based analysis (RockYou dataset support)
- ✅ AI-generated password suggestions using Mistral AI
- ✅ Flask-based backend
- ✅ Optional SSL certificate support
- ✅ Easily extendable and testable

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/password-strength-analyzer.git
cd password-strength-analyzer
```

### 2. Set up the Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file inside `backend/ml_models/` with the following content:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
SSL_CERT_PATH=C:\Path\To\cacert.pem
```

---

## 💡 Notes

- If the **RockYou** dataset is missing, dictionary-based suggestions will not be fully accurate.
- Mistral AI API is required for GenAI-based password suggestions. You can get your API key from [Mistral's Developer Portal](https://mistral.ai/).
- The `venv/` folder and `.env` file are excluded from version control using `.gitignore`.

---

## 🧪 Testing

You can add and run tests in the `tests/` directory. Example framework: `pytest`.

---

## 📜 License

MIT License

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📫 Contact

Made with ❤️ by Sidharth Maharana
