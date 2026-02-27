import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="AI Meeting Brain", page_icon="🎙️")

st.title("🎙️ AI Meeting Brain")
api_key = st.sidebar.text_input("Cole sua API Key do Google aqui:", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Superprompt integrado com as suas necessidades
        SYSTEM_PROMPT = """
        Você é um Especialista em Gestão de Reuniões. 
        Analise o áudio e use o Método SPIN Selling para avaliar vendas.
        Gere um resumo, Action Items (Kanban) e destaque pontos recorrentes.
        Identifique oradores e sentimentos.
        """

        st.write("Clique para gravar. Clique novamente para parar e analisar.")
        
        audio = mic_recorder(
            start_prompt="🔴 Iniciar Gravação",
            stop_prompt="⏹️ Parar e Analisar",
            key='recorder'
        )

        if audio:
            st.audio(audio['bytes'])
            with st.spinner("O Gemini está analisando a reunião..."):
                # Usando a nomenclatura mais estável para evitar o erro 404
                model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)
                
                # Envio simplificado de áudio
                response = model.generate_content([
                    "Por favor, analise este áudio seguindo as instruções de sistema.",
                    {"mime_type": "audio/wav", "data": audio['bytes']}
                ])
                
                st.success("Análise Concluída!")
                st.markdown(response.text)
                
                st.divider()
                if st.button("📲 Compartilhar no WhatsApp"):
                    # Prepara um resumo curto para o link do WhatsApp
                    texto_resumo = response.text[:200].replace('\n', ' ')
                    st.write(f"[Enviar Resumo para WhatsApp](https://wa.me/?text={texto_resumo})")
                    
    except Exception as e:
        st.error(f"Erro ao processar: {e}")
        st.info("Dica: Verifique se sua chave API está correta e se o modelo gemini-1.5-flash está habilitado no seu painel.")
else:
    st.warning("Por favor, insira sua API Key na barra lateral.")
