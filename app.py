import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(
    page_title="Classic Car English Companion",
    page_icon="🚘",
    layout="centered"
)

# Título en azul
st.markdown("<h1 style='text-align: center; color: #0066cc;'>🚘 English & Classic Cars 🛠️</h1>", unsafe_allow_html=True)

# --- 2. BARRA LATERAL (MENÚ) ---
with st.sidebar:
    st.header("Opciones / Settings")
    # Selector de tema
    modo = st.radio(
        "Elige el tema de conversación:",
        ["Mecánica y Autos Clásicos", "Charla General (De todo un poco)"]
    )
    st.write("---")
    st.write("ℹ️ *Te corregiré el inglés suavemente mientras charlamos.*")

# --- 3. CONEXIÓN CON GOOGLE ---
api_key = st.text_input("Ingresa tu API Key de Google:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    generation_config = {
      "temperature": 0.7, 
      "top_p": 0.95,
      "max_output_tokens": 2048,
    }

    # --- 4. CEREBRO DEL ROBOT ---
    system_instruction = f"""
    ROL: Eres un compañero de conversación amable para una persona mayor.
    
    MODO ACTUAL ELEGIDO: {modo}
    
    TUS REGLAS DE ORO:
    1. IDIOMA: Habla en INGLÉS. Si el usuario no entiende, explica en español.
    2. CORRECCIÓN: Si el usuario se equivoca en inglés, corrígelo con mucha suavidad.
    3. PERSONALIDAD SEGÚN MODO:
       - Si el modo es "Mecánica y Autos Clásicos": Eres un experto mecánico. Habla de motores, restauraciones y modelos clásicos.
       - Si el modo es "Charla General": Eres un amigo empático. Habla de la vida, el clima, o lo que surja.
    """

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash", 
        generation_config=generation_config,
        system_instruction=system_instruction
    )

    # --- 5. CHAT ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Escribe aquí / Write here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["content"]]} 
                for m in st.session_state.messages
            ])
            response = chat.send_message(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
