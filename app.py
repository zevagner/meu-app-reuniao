import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="AI Meeting Brain", page_icon="🎙️")

st.title("🎙️ AI Meeting Brain")
api_key = st.sidebar.text_input("Cole sua API Key do Google aqui:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    SYSTEM_PROMPT = """
    Você é um Especialista em Gestão de Reuniões. 
    Analise o áudio e use o Método SPIN Selling para avaliar vendas.
    Gere um resumo, Action Items (Kanban) e mantenha o contexto histórico.
    """

    st.write("Clique no botão abaixo para gravar. Clique novamente para parar.")
    
    # Este componente substitui os botões de gravar/pausar por um que funciona na web
    audio = mic_recorder(
        start_prompt="🔴 Iniciar Gravação",
        stop_prompt="⏹️ Parar e Analisar",
        key='recorder'
    )

    if audio:
        st.audio(audio['bytes'])
        with st.spinner("O Gemini está analisando a reunião..."):
            model = genai.GenerativeModel("gemini-1.5-pro", system_instruction=SYSTEM_PROMPT)
            
            # Envia os bytes do áudio gravado para a IA
            response = model.generate_content([
                {"mime_type": "audio/wav", "data": audio['bytes']}
            ])
            
            st.success("Análise Concluída!")
            st.markdown(response.text)
            
            # Botão de WhatsApp com o resumo gerado
            st.divider()
            if st.button("📲 Compartilhar no WhatsApp"):
                texto = response.text[:500] # Pega o início do resumo
                st.write(f"[Enviar para WhatsApp](https://wa.me/?text={texto})")
else:
    st.warning("Por favor, insira sua API Key na barra lateral.")
