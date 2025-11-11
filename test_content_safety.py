from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions

# WKLEJ SWOJE DANE
endpoint = 
key = 

# Test połączenia
def test_content_safety():
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    
    # Testowy tekst
    test_text = """
    Jan Kowalski
    PESEL: 90010112345
    Email: jan.kowalski@example.com
    """
    
    try:
        # Analiza tekstu
        request = AnalyzeTextOptions(text=test_text)
        response = client.analyze_text(request)
        
        print("✅ Połączenie działa!")
        print(f"Wynik analizy: {response}")
        
    except Exception as e:
        print(f"❌ Błąd: {e}")

if __name__ == "__main__":
    test_content_safety()
