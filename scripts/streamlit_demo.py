import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Compliance Bot",
    page_icon="🔒",
    layout="wide"
)

# CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🔒 Compliance Bot")
st.markdown("### Wykrywacz Danych Wrażliwych")
st.markdown("**LevelUp**")
st.divider()

# Sidebar
with st.sidebar:
    st.header("ℹ️ Informacje")
    st.info("""
    **System wykrywa:**
    - Imiona i nazwiska
    - Numery PESEL
    - Adresy email
    - Numery telefonów
    - Adresy zamieszkania
    - Numery kont bankowych
    """)
    
    api_status = st.empty()
    
    try:
        health = requests.get("http://127.0.0.1:5000/health", timeout=2)
        api_status.success("✅ API: Online")
    except:
        api_status.error("❌ API: Offline")
        st.warning("Uruchom API: `python scripts/api_endpoint.py`")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Wprowadź Dokument")
    
    # Example button
    if st.button("📝 Załaduj Przykład"):
        st.session_state.text_input = """Jan Kowalski
PESEL: 90010112345
Email: jan.kowalski@example.com
Tel: +48 123 456 789
Adres: ul. Kwiatowa 15/3, 00-001 Warszawa
Nr konta: 12 3456 7890 1234 5678 9012 3456"""
    
    text_input = st.text_area(
        "Tekst do analizy:",
        value=st.session_state.get('text_input', ''),
        height=300,
        placeholder="Wklej tutaj dokument..."
    )
    
    analyze_button = st.button("🔍 Analizuj Dokument", type="primary")

with col2:
    st.subheader("📊 Wyniki Analizy")
    
    if analyze_button and text_input:
        with st.spinner("Analizuję dokument..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:5000/analyze",
                    json={"text": text_input},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Metryki
                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                    
                    with metrics_col1:
                        st.metric(
                            "PII Wykryte",
                            "TAK" if result.get('pii_found') else "NIE",
                            delta="Alert" if result.get('pii_found') else None,
                            delta_color="inverse"
                        )
                    
                    with metrics_col2:
                        st.metric(
                            "Liczba PII",
                            len(result.get('pii_items', []))
                        )
                    
                    with metrics_col3:
                        risk = result.get('risk_level', 'unknown').upper()
                        st.metric("Poziom Ryzyka", risk)
                    
                    st.divider()
                    
                    # Wykryte PII
                    if result.get('pii_items'):
                        st.subheader("🔍 Wykryte Dane Osobowe")
                        for i, item in enumerate(result['pii_items'], 1):
                            with st.expander(f"{i}. {item['type']}", expanded=True):
                                st.code(item['value'])
                                st.caption(f"Pewność: {item['confidence']}")
                    
                    # Anonimizacja
                    if result.get('anonymized_text'):
                        st.subheader("🔒 Tekst Po Anonimizacji")
                        st.code(result['anonymized_text'], language="text")
                    
                    # Rekomendacje
                    if result.get('recommendations'):
                        st.subheader("💡 Rekomendacje")
                        for rec in result['recommendations']:
                            st.info(rec)
                
                else:
                    st.error(f"Błąd API: {response.status_code}")
            
            except Exception as e:
                st.error(f"Błąd połączenia: {e}")
                st.warning("Sprawdź czy Flask API jest uruchomione!")
    
    elif analyze_button:
        st.warning("Proszę wprowadzić tekst do analizy!")