# Compliance Bot - Sensitive Data Detector

A GDPR-compliant system for automatic detection and anonymization of personal data (PII).

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Azure](https://img.shields.io/badge/Azure-OpenAI-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- ✅ **PII detection** - PESEL (Polish national ID number), email, phone numbers, addresses, bank account numbers
- ✅ **GDPR risk assessment** - automatic risk level classification
- ✅ **Data anonymization** - intelligent replacement of sensitive information
- ✅ **Reporting** - detailed compliance reports
- ✅ **Web interface** - Streamlit dashboard for testing

## Technologies

- **Azure OpenAI (GPT-4)** - personal data detection
- **Azure Content Safety** - content moderation
- **Azure AI Foundry** - AI orchestration
- **Python 3.10+** - backend
- **Flask** - REST API
- **Streamlit** - web interface
- **Prompt Flow** - workflow automation

## Accuracy Metrics

- **Precision**: ~95%
- **Recall**: ~92%
- **F1-Score**: ~93%

## Installation

### Requirements

- Python 3.10+
- Azure account with access to Azure OpenAI
- VS Code (optional)

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR-USERNAME/compliance-bot.git
cd compliance-bot
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**

Create a `config/.env` file:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-key-here
AZURE_OPENAI_DEPLOYMENT=gpt4-compliance

CONTENT_SAFETY_ENDPOINT=https://your-content-safety.cognitiveservices.azure.com/
CONTENT_SAFETY_KEY=your-key-here
```

5. **Run the demo:**
```bash
# Terminal 1 - API
python scripts/api_endpoint.py

# Terminal 2 - Streamlit
streamlit run streamlit_demo.py
```

## Usage

### Document analysis via the API
```python
import requests

response = requests.post(
    "http://localhost:5000/analyze",
    json={"text": "Jan Kowalski, PESEL: 90010112345"}
)

result = response.json()
print(f"PII found: {result['pii_found']}")
print(f"PII count: {len(result['pii_items'])}")
```

### Analysis via the CLI
```bash
python scripts/pii_detector.py
```

### Web interface
```bash
streamlit run streamlit_demo.py
```

Open: http://localhost:8501

## Project Structure
```
ComplianceBot/
├── documents/              # Test documents
├── scripts/               # Main scripts
│   ├── pii_detector.py   # PII detector
│   ├── api_endpoint.py   # REST API
│   ├── evaluate_accuracy.py  # Metrics
│   └── demo.py           # Presentation demo
├── config/               # Configuration
├── results/              # Analysis results
├── streamlit_demo.py     # Web interface
├── requirements.txt      # Dependencies
└── README.md            # Documentation
```

## Use Cases

1. **HR & Recruitment** - scanning CVs and job applications
2. **Compliance** - auditing documents for GDPR compliance
3. **Customer Service** - reviewing correspondence
4. **Legal** - reviewing agreements and contracts
5. **Data Processing** - automated anonymization

## Security

- All data processed locally
- API keys stored in `.env`
- GDPR compliant

## Author

**Katarzyna Majzel-Pośpiech**  
Project: LevelUp

## Screenshots
<img width="2400" height="1151" alt="image" src="https://github.com/user-attachments/assets/b25f3485-3b1d-45d5-9276-e3463df4fa09" />

<img width="2403" height="1184" alt="image" src="https://github.com/user-attachments/assets/4411e881-d184-4f20-873e-2fbfea453924" />

<img width="2085" height="1269" alt="image" src="https://github.com/user-attachments/assets/98834a94-81f9-4603-9176-e442a90fe2b5" />

And the flow builder in Azure:

<img width="2400" height="1119" alt="image" src="https://github.com/user-attachments/assets/29f83c6e-6f61-45cd-8293-ae7f54da760c" />




MIT License

