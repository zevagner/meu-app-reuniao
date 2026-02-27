import streamlit as st
import google.generativeai as genai

# Configuração da Página
st.set_page_config(page_title="AI Meeting Brain", page_icon="🎙️")

# --- INTERFACE ---
st.title("🎙️ AI Meeting Brain")
st.markdown("### Gravador Inteligente com Memória e SPIN Selling")

# Campo para você colar sua chave de forma segura no app
api_key = st.sidebar.text_input("Cole sua API Key do Google aqui:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # --- O SUPERPROMPT (O cérebro que você definiu) ---
    SYSTEM_PROMPT = """
    Você é um Especialista em Gestão de Reuniões e Memória Organizacional.
    DIRETRIZES:
    1. DIARIZAÇÃO: Separe as falas por oradores.
    2. RESUMO EXECUTIVO: 3 frases sobre o objetivo.
    3. CONTEXTO HISTÓRICO: Compare com o que foi dito antes.
    4. SPIN SELLING: Se for venda, avalie (Situação, Problema, Implicação, Necessidade).
    5. ACTION ITEMS: Liste [Responsável] | [Tarefa] | [Prazo].
    SAÍDA: Gere um bloco formatado para WhatsApp (curto) e um para E-mail (formal).
    """

    # --- BOTÕES DE CONTROLE ---
    st.write("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔴 Gravar"):
            st.session_state.status = "Gravando..."
            st.success("O sistema está captando o áudio...")

    with col2:
        if st.button("⏸️ Pausar"):
            st.session_state.status = "Pausado"
            st.warning("Gravação pausada temporariamente.")

    with col3:
        if st.button("⏹️ Encerrar e Analisar"):
            with st.spinner("O Gemini está analisando a reunião e o histórico..."):
                # Simulação da análise (Para áudio real, usaríamos upload_file)
                model = genai.GenerativeModel("gemini-1.5-pro", system_instruction=SYSTEM_PROMPT)
                st.success("Análise Concluída!")
                st.markdown("### 📋 Relatório da Reunião")
                st.write("Aqui aparecerá o resumo formatado conforme o Superprompt.")

    # --- COMPARTILHAMENTO ---
    st.divider()
    if st.button("📲 Preparar para WhatsApp"):
        texto_wa = "Resumo da Reunião: Decidimos avançar com o projeto..."
        st.write(f"[Clique aqui para enviar](https://wa.me/?text={texto_wa})")

else:
    st.warning("Por favor, insira sua API Key na barra lateral para começar.")
