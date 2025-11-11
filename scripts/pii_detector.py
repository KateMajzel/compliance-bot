import os
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
import json

# Ładowanie konfiguracji
load_dotenv('config/.env')

class PIIDetector:
    def __init__(self):
        # Inicjalizacja Content Safety
        self.content_safety_client = ContentSafetyClient(
            endpoint=os.getenv('CONTENT_SAFETY_ENDPOINT'),
            credential=AzureKeyCredential(os.getenv('CONTENT_SAFETY_KEY'))
        )
        
        # Inicjalizacja Azure OpenAI
        self.openai_client = AzureOpenAI(
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_key=os.getenv('AZURE_OPENAI_KEY'),
            api_version="2024-02-15-preview"
        )
    
    def detect_pii_with_ai(self, text):
        """Wykrywa PII używając GPT-4"""
        
        prompt = f"""
        Jesteś ekspertem RODO. Przeanalizuj poniższy tekst i wykryj WSZYSTKIE dane osobowe (PII).
        
        Szukaj:
        - Imion i nazwisk
        - Numerów PESEL
        - Numerów telefonów
        - Adresów email
        - Adresów zamieszkania
        - Numerów kont bankowych
        - Numerów NIP
        - Innych danych identyfikujących osobę
        
        Tekst do analizy:
        {text}
        
        Odpowiedz w formacie JSON:
        {{
            "pii_found": true/false,
            "pii_items": [
                {{
                    "type": "typ_danych",
                    "value": "wykryta_wartość",
                    "confidence": "high/medium/low",
                    "position": "pozycja_w_tekście"
                }}
            ],
            "risk_level": "high/medium/low",
            "recommendations": ["rekomendacja1", "rekomendacja2"]
        }}
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model=os.getenv('AZURE_OPENAI_DEPLOYMENT'),
                messages=[
                    {"role": "system", "content": "Jesteś ekspertem ds. ochrony danych osobowych i RODO."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            result = response.choices[0].message.content
            
            # Parsowanie JSON z odpowiedzi
            # Czasami GPT zwraca markdown, więc czyścimy
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0]
            
            return json.loads(result)
            
        except Exception as e:
            print(f"Błąd podczas analizy AI: {e}")
            return None
    
    def anonymize_pii(self, text, pii_items):
        """Proponuje anonimizację wykrytych PII"""
        
        anonymized_text = text
        anonymization_map = []
        
        for item in pii_items:
            original = item['value']
            pii_type = item['type']
            
            # Różne strategie anonimizacji
            if pii_type == "PESEL":
                anonymized = "***********"
            elif pii_type == "Telefon":
                anonymized = "+48 XXX XXX XXX"
            elif pii_type == "Email":
                parts = original.split('@')
                anonymized = f"{parts[0][:2]}***@{parts[1]}"
            elif pii_type == "Numer konta":
                anonymized = "** **** **** **** **** **** ****"
            elif pii_type in ["Imię i nazwisko", "Nazwisko"]:
                words = original.split()
                anonymized = " ".join([w[0] + "***" for w in words])
            elif pii_type == "Adres":
                anonymized = "[ADRES USUNIĘTY]"
            else:
                anonymized = "[DANE USUNIĘTE]"
            
            anonymized_text = anonymized_text.replace(original, anonymized)
            anonymization_map.append({
                "original": original,
                "anonymized": anonymized,
                "type": pii_type
            })
        
        return anonymized_text, anonymization_map
    
    def analyze_document(self, file_path):
        """Główna funkcja analizująca dokument"""
        
        print(f"\n{'='*60}")
        print(f"Analiza dokumentu: {os.path.basename(file_path)}")
        print(f"{'='*60}\n")
        
        # Wczytanie dokumentu
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Detekcja PII
        print("🔍 Wykrywanie danych osobowych...")
        pii_result = self.detect_pii_with_ai(content)
        
        if not pii_result:
            print("❌ Błąd podczas analizy")
            return None
        
        # Wyświetlenie wyników
        print(f"\n📊 WYNIKI ANALIZY:")
        print(f"PII wykryte: {'TAK' if pii_result['pii_found'] else 'NIE'}")
        print(f"Poziom ryzyka: {pii_result['risk_level'].upper()}")
        print(f"\nLiczba wykrytych elementów PII: {len(pii_result['pii_items'])}")
        
        if pii_result['pii_items']:
            print("\n📝 Wykryte dane osobowe:")
            for idx, item in enumerate(pii_result['pii_items'], 1):
                print(f"  {idx}. {item['type']}: {item['value']}")
                print(f"     Pewność: {item['confidence']}")
        
        # Anonimizacja
        if pii_result['pii_found']:
            print("\n🔒 Propozycja anonimizacji...")
            anonymized_content, anon_map = self.anonymize_pii(
                content, 
                pii_result['pii_items']
            )
            
            # Zapis zanonimizowanego dokumentu
            output_path = file_path.replace('documents/', 'results/anonymized_')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(anonymized_content)
            
            print(f"✅ Zapisano zanonimizowany dokument: {output_path}")
        
        # Rekomendacje
        if pii_result.get('recommendations'):
            print("\n💡 REKOMENDACJE:")
            for rec in pii_result['recommendations']:
                print(f"  • {rec}")
        
        return pii_result


# Funkcja główna
def main():
    detector = PIIDetector()
    
    # Utworzenie folderu results jeśli nie istnieje
    os.makedirs('results', exist_ok=True)
    
    # Analiza wszystkich dokumentów
    documents = [
        'documents/document1.txt',
        'documents/document2.txt',
        'documents/document3.txt',
        'documents/document4.txt'
    ]
    
    all_results = []
    
    for doc in documents:
        if os.path.exists(doc):
            result = detector.analyze_document(doc)
            if result:
                all_results.append({
                    'document': os.path.basename(doc),
                    'result': result
                })
    
    # Zapisanie zbiorczego raportu
    with open('results/full_report.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print("✅ Analiza zakończona!")
    print(f"📄 Raport zapisany w: results/full_report.json")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()