import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="AI Meeting Brain", page_icon="🎙️")

st.title("🎙️ AI Meeting Brain")
api_key = st.sidebar.text_input("Cole sua API Key do Google aqui:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Superprompt integrado conforme solicitado
        SYSTEM_PROMPT = """
        Você é um Especialista em Gestão de Reuniões. 
        Analise o áudio e use o Método SPIN Selling para avaliar vendas.
        Gere um resumo, Action Items (Kanban) e mantenha o contexto histórico.
        Identifique oradores e sentimentos.
        """

        st.write("Clique para gravar. Clique novamente para encerrar e analisar.")
        
        audio = mic_recorder(
            start_prompt="🔴 Iniciar Gravação",
            stop_prompt="⏹️ Parar e Analisar",
            key='recorder'
        )

        if audio:
            st.audio(audio['bytes'])
            with st.spinner("O Gemini está analisando a reunião..."):
                # Ajustamos para gemini-1.5-flash que é mais rápido e estável para áudio simples
                model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)
                
                # Mudança na forma de envio para garantir compatibilidade
                contents = [
                    {
                        "parts": [
                            {"mime_type": "audio/wav", "data": audio['bytes']},
                            {"text": "Por favor, analise esta reunião conforme suas instruções de sistema."}
                        ]
                    }
                ]
                
                response = model.generate_content(contents)
                
                st.success("Análise Concluída!")
                st.markdown(response.text)
                
                st.divider()
                if st.button("📲 Compartilhar no WhatsApp"):
                    texto_curto = response.text[:300].replace('\n', ' ')
                    st.write(f"[Enviar para WhatsApp](https://wa.me/?text={texto_curto})")
                    
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
else:
    st.warning("Por favor, insira sua API Key na barra lateral.")
