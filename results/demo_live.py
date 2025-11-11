import requests
import json
import time
from colorama import Fore, Style, init

init(autoreset=True)

API_URL = "http://127.0.0.1:5000/analyze"

def print_header(text):
    print("\n" + "="*70)
    print(Fore.CYAN + Style.BRIGHT + text.center(70))
    print("="*70 + "\n")

def print_step(number, text):
    print(Fore.GREEN + f"\n[KROK {number}] " + Style.RESET_ALL + text)
    time.sleep(0.5)

def analyze_with_animation(text, name):
    print_header(f"📄 {name}")
    
    print(Fore.WHITE + "Dokument:")
    print("-" * 70)
    print(text[:200] + "..." if len(text) > 200 else text)
    print("-" * 70)
    
    input(Fore.YELLOW + "\n⏸️  Naciśnij ENTER aby rozpocząć analizę...")
    
    # Animacja
    print(Fore.CYAN + "\n🔍 Analizuję dokument", end="")
    for i in range(5):
        print(".", end="", flush=True)
        time.sleep(0.3)
    print()
    
    try:
        response = requests.post(API_URL, json={"text": text}, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            display_results(result)
        else:
            print(Fore.RED + f"\n❌ Błąd API: {response.status_code}")
    
    except Exception as e:
        print(Fore.RED + f"\n❌ Błąd: {e}")
        print(Fore.YELLOW + "\n💡 Sprawdź czy Flask API jest uruchomione!")

def display_results(result):
    print(Fore.GREEN + "\n✅ Analiza zakończona!\n")
    
    # Status PII
    if result.get('pii_found'):
        print(Fore.RED + Style.BRIGHT + "⚠️  WYKRYTO DANE OSOBOWE!")
    else:
        print(Fore.GREEN + "✅ Brak danych osobowych")
    
    # Statystyki
    print(f"\n📊 STATYSTYKI:")
    print(f"   • Wykryte PII: {Fore.CYAN}{len(result.get('pii_items', []))}{Style.RESET_ALL}")
    
    risk = result.get('risk_level', 'unknown').upper()
    risk_color = Fore.RED if risk == 'HIGH' else Fore.YELLOW if risk == 'MEDIUM' else Fore.GREEN
    print(f"   • Poziom ryzyka: {risk_color}{risk}{Style.RESET_ALL}")
    
    # Lista PII
    if result.get('pii_items'):
        print(f"\n🔍 WYKRYTE DANE OSOBOWE:")
        for i, item in enumerate(result['pii_items'], 1):
            print(f"   {Fore.RED}{i}. {item['type']}{Style.RESET_ALL}: {Fore.YELLOW}{item['value']}{Style.RESET_ALL}")
    
    # Anonimizacja
    if result.get('anonymized_text'):
        print(f"\n🔒 PRZYKŁAD ANONIMIZACJI:")
        print("-" * 70)
        anon = result['anonymized_text'][:200]
        print(Fore.GREEN + anon + "..." if len(result['anonymized_text']) > 200 else anon)
        print(Style.RESET_ALL + "-" * 70)
    
    # Rekomendacje
    if result.get('recommendations'):
        print(f"\n💡 REKOMENDACJE:")
        for rec in result['recommendations'][:3]:
            print(f"   • {rec}")

def main():
    print_header("🔒 COMPLIANCE BOT - LIVE DEMO")
    print(Fore.YELLOW + "System wykrywania danych wrażliwych (PII)")
    print(Fore.CYAN + "Totalizator Sportowy | AI Manager 2025\n")
    
    # Sprawdź czy API działa
    try:
        health = requests.get("http://127.0.0.1:5000/health", timeout=2)
        print(Fore.GREEN + "✅ API Status: Działa!")
    except:
        print(Fore.RED + "❌ API nie odpowiada!")
        print(Fore.YELLOW + "\n💡 Uruchom API w osobnym terminalu:")
        print(Fore.CYAN + "   python scripts/api_endpoint.py\n")
        return
    
    # Testy
    tests = [
        {
            "name": "Test 1: CV z Danymi Osobowymi",
            "text": """Jan Kowalski
PESEL: 90010112345
Email: jan.kowalski@example.com
Tel: +48 123 456 789
Adres: ul. Kwiatowa 15/3, 00-001 Warszawa
Nr konta: 12 3456 7890 1234 5678 9012 3456"""
        },
        {
            "name": "Test 2: Dokument Bezpieczny",
            "text": """Polityka Bezpieczeństwa Informacji

Niniejszy dokument określa zasady bezpieczeństwa w organizacji.
Dane należy przechowywać zgodnie z RODO."""
        }
    ]
    
    for i, test in enumerate(tests, 1):
        print_step(i, f"Rozpoczynam test: {test['name']}")
        analyze_with_animation(test['text'], test['name'])
        
        if i < len(tests):
            input(Fore.YELLOW + "\n⏭️  Naciśnij ENTER aby przejść do następnego testu...")
    
    print_header("✅ DEMO ZAKOŃCZONE")
    print(Fore.GREEN + "System gotowy do wdrożenia!\n")
    print(Fore.CYAN + "📊 Możliwości:")
    print("   ✓ Wykrywa wszystkie rodzaje PII")
    print("   ✓ Ocenia ryzyko RODO")
    print("   ✓ Automatyczna anonimizacja")
    print("   ✓ REST API gotowe do integracji")
    print("   ✓ Power Automate ready\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⏸️  Demo przerwane przez użytkownika")