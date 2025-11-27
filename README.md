# Compliance Bot - Wykrywacz Danych Wrażliwych

System automatycznego wykrywania i anonimizacji danych osobowych (PII) zgodny z RODO.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Azure](https://img.shields.io/badge/Azure-OpenAI-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## Funkcjonalności

- ✅ **Wykrywanie PII** - PESEL, email, telefon, adresy, numery kont
- ✅ **Ocena ryzyka RODO** - automatyczna klasyfikacja poziomu zagrożenia
- ✅ **Anonimizacja danych** - inteligentne zastępowanie wrażliwych informacji
- ✅ **Raportowanie** - szczegółowe raporty compliance
- ✅ **Web Interface** - Streamlit dashboard do testowania

## Technologie

- **Azure OpenAI (GPT-4)** - wykrywanie danych osobowych
- **Azure Content Safety** - moderacja treści
- **Azure AI Foundry** - orkiestracja AI
- **Python 3.10+** - backend
- **Flask** - REST API
- **Streamlit** - web interface
- **Prompt Flow** - workflow automation

## Metryki Dokładności

- **Precision**: ~95%
- **Recall**: ~92%
- **F1-Score**: ~93%

## Instalacja

### Wymagania

- Python 3.10+
- Konto Azure z dostępem do Azure OpenAI
- VS Code (opcjonalnie)

### Szybki Start

1. **Sklonuj repozytorium:**
```bash
git clone https://github.com/TWOJ-USERNAME/compliance-bot.git
cd compliance-bot
```

2. **Utwórz środowisko wirtualne:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. **Zainstaluj zależności:**
```bash
pip install -r requirements.txt
```

4. **Skonfiguruj zmienne środowiskowe:**

Utwórz plik `config/.env`:
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-key-here
AZURE_OPENAI_DEPLOYMENT=gpt4-compliance

CONTENT_SAFETY_ENDPOINT=https://your-content-safety.cognitiveservices.azure.com/
CONTENT_SAFETY_KEY=your-key-here
```

5. **Uruchom demo:**
```bash
# Terminal 1 - API
python scripts/api_endpoint.py

# Terminal 2 - Streamlit
streamlit run streamlit_demo.py
```

## Użycie

### Analiza dokumentu przez API
```python
import requests

response = requests.post(
    "http://localhost:5000/analyze",
    json={"text": "Jan Kowalski, PESEL: 90010112345"}
)

result = response.json()
print(f"PII wykryte: {result['pii_found']}")
print(f"Liczba PII: {len(result['pii_items'])}")
```

### Analiza przez CLI
```bash
python scripts/pii_detector.py
```

### Web Interface
```bash
streamlit run streamlit_demo.py
```

Otwórz: http://localhost:8501

## Struktura Projektu
```
ComplianceBot/
├── documents/              # Dokumenty testowe
├── scripts/               # Skrypty główne
│   ├── pii_detector.py   # Detektor PII
│   ├── api_endpoint.py   # REST API
│   ├── evaluate_accuracy.py  # Metryki
│   └── demo.py           # Demo prezentacyjne
├── config/               # Konfiguracja 
├── results/              # Wyniki analiz
├── streamlit_demo.py     # Web interface
├── requirements.txt      # Zależności
└── README.md            # Dokumentacja
```

## Przypadki Użycia

1. **HR & Rekrutacja** - skanowanie CV i aplikacji
2. **Compliance** - audyt dokumentów pod kątem RODO
3. **Customer Service** - weryfikacja korespondencji
4. **Legal** - przegląd umów i kontraktów
5. **Data Processing** - automatyczna anonimizacja

## Bezpieczeństwo

- Wszystkie dane przetwarzane lokalnie
- Klucze API przechowywane w `.env` (nie commitowane)
- Zgodność z RODO
- Szyfrowanie połączeń (HTTPS w produkcji)

## Autor

**Katarzyna Majzel-Pośpiech** 
Projekt: LevelUp

## Zrzuty z aplikacji
<img width="2400" height="1151" alt="image" src="https://github.com/user-attachments/assets/b25f3485-3b1d-45d5-9276-e3463df4fa09" />

<img width="2403" height="1184" alt="image" src="https://github.com/user-attachments/assets/4411e881-d184-4f20-873e-2fbfea453924" />

<img width="2085" height="1269" alt="image" src="https://github.com/user-attachments/assets/98834a94-81f9-4603-9176-e442a90fe2b5" />

oraz flow builder w Azure

<img width="2400" height="1119" alt="image" src="https://github.com/user-attachments/assets/29f83c6e-6f61-45cd-8293-ae7f54da760c" />





## Licencja

MIT License

