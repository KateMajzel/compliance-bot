from flask import Flask, request, jsonify
from pii_detector import PIIDetector
import os

app = Flask(__name__)
detector = PIIDetector()

@app.route('/analyze', methods=['POST'])
def analyze_document():
    """
    API endpoint do analizy dokumentów
    Przykład użycia:
    POST /analyze
    {
        "text": "dokument do analizy..."
    }
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Brak tekstu do analizy'}), 400
        
        # Analiza
        result = detector.detect_pii_with_ai(text)
        
        if not result:
            return jsonify({'error': 'Błąd podczas analizy'}), 500
        
        # Anonimizacja jeśli wykryto PII
        if result['pii_found']:
            anonymized, anon_map = detector.anonymize_pii(text, result['pii_items'])
            result['anonymized_text'] = anonymized
            result['anonymization_map'] = anon_map
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Dla testów lokalnych
    app.run(host='0.0.0.0', port=5000, debug=True)