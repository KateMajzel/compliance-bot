import os
import time
from pii_detector import PIIDetector
from colorama import Fore, Style, init

# Inicjalizacja kolorów
init(autoreset=True)

def print_header(text):
    print("\n" + "="*70)
    print(Fore.CYAN + Style.BRIGHT + text.center(70))
    print("="*70 + "\n")

def print_step(number, text):
    print(Fore.GREEN + f"\n[KROK {number}] " + Style.RESET_ALL + text)
    time.sleep(1)

def demo_presentation():
    """
    Prezentacja demo compliance bot
    """
    print_header("🔒 COMPLIANCE BOT - DEMO")
    print(Fore.YELLOW + "System wykrywania i anonimizacji danych osobowych\n")
    
    detector = PIIDetector()
    
    # DEMO 1: Analiza CV
    print_step(1, "Analiza dokumentu CV z danymi osobowymi")
    print("Dokument: document1.txt (CV)")
    
    with open('documents/document1.txt', 'r', encoding='utf-8') as f:
        cv_content = f.read()
    
    print(Fore.WHITE + "\nPodgląd dokumentu:")
    print("-" * 70)
    print(cv_content[:200] + "...")
    print("-" * 70)
    
    input(Fore.YELLOW + "\nNaciśnij ENTER aby rozpocząć analizę...")
    
    result1 = detector.detect_pii_with_ai(cv_content)
    
    print(Fore.GREEN + f"\n✓ Wykryto {len(result1['pii_items'])} elementów PII")
    print(Fore.RED + f"⚠️  Poziom ryzyka: {result1['risk_level'].upper()}")
    
    time.sleep(2)
    
    # DEMO 2: Anonimizacja
    print_step(2, "Automatyczna anonimizacja")
    
    anonymized, anon_map = detector.anonymize_pii(cv_content, result1['pii_items'])
    
    print(Fore.WHITE + "\nDokument po anonimizacji:")
    print("-" * 70)
    print(anonymized[:300] + "...")
    print("-" * 70)
    
    time.sleep(2)
    
    # DEMO 3: Porównanie
    print_step(3, "Porównanie dokumentów")
    
    documents = [
        ('document1.txt', 'CV z danymi osobowymi'),
        ('document2.txt', 'Umowa zlecenia'),
        ('document3.txt', 'Polityka bezpieczeństwa'),
        ('document4.txt', 'Lista pracowników')
    ]
    
    print("\n" + Fore.CYAN + "Zestawienie wyników:\n")
    
    for doc_name, desc in documents:
        doc_path = f'documents/{doc_name}'
        if os.path.exists(doc_path):
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = detector.detect_pii_with_ai(content)
            
            if result:
                risk_color = Fore.RED if result['risk_level'] == 'high' else Fore.YELLOW if result['risk_level'] == 'medium' else Fore.GREEN
                
                print(f"📄 {desc:<30} | PII: {len(result['pii_items']):2} | Ryzyko: {risk_color}{result['risk_level'].upper()}")
    
    # DEMO 4: Rekomendacje
    print_step(4, "Rekomendacje działań")
    
    print("\n" + Fore.CYAN + "💡 Zalecane działania:\n")
    for rec in result1.get('recommendations', []):
        print(f"  • {rec}")
    
    print_header("✅ DEMO ZAKOŃCZONE")
    print(Fore.GREEN + "System gotowy do wdrożenia!")
    print(Fore.YELLOW + "\nDostępne funkcje:")
    print("  ✓ Wykrywanie PII (PESEL, email, telefon, adresy)")
    print("  ✓ Ocena ryzyka RODO")
    print("  ✓ Automatyczna anonimizacja")
    print("  ✓ Raportowanie do Power Automate")
    print("  ✓ Integracja z Azure AI services\n")

if __name__ == "__main__":
    # Instalacja colorama jeśli nie ma
    try:
        from colorama import Fore, Style, init
    except ImportError:
        print("Instaluję colorama...")
        os.system("pip install colorama")
        from colorama import Fore, Style, init
    
    demo_presentation()