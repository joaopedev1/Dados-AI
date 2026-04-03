import streamlit as st
import google.generativeai as genai
import os
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da Página
st.set_page_config(
    page_title="FinAI - Assitente Financeiro",
    page_icon="🤖💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização básica UX
st.markdown("""
<style>
    .stChatFloatingInputContainer {
        padding-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Configuração API do Gemini
API_KEY = os.getenv("GEMINI_API_KEY")
model = None

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        
        system_instruction = """Você é o FinAI, um assistente financeiro inteligente, educado, e focado em experiência do usuário (UX). 
Sua função é ajudar os usuários a entender finanças pessoais, planejamento de aposentadoria e produtos de investimento de forma simples.
Diretrizes:
1. Seja sempre claro, objetivo e use linguagem acessível. Explique os jargões se necessário.
2. NUNCA ofereça recomendações definitivas de investimento, seja ético. Informe que você provê conteúdos educacionais.
3. Formate suas respostas com marcadores, listas ou em pequenos blocos para facilitar a leitura.
4. Estimule a educação financeira, focando no longo prazo e responsabilidade.
"""
        # Suporta system instructions no gemini-1.5-pro
        model = genai.GenerativeModel(model_name="gemini-1.5-pro",
                                      system_instruction=system_instruction)
    except Exception as e:
        # Fallback
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Inicialização de estado para o Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Eu sou o **FinAI**, seu Gêmeo Financeiro Digital. Estou aqui para ajudar a organizar suas finanças, explicar conceitos ou planejar seu futuro. O que deseja saber hoje?"}
    ]

# Guardar sessão ativa com histórico no SDK do Gemini para que haja contexto
if "chat_session" not in st.session_state and model:
    st.session_state.chat_session = model.start_chat(history=[])


def render_sidebar():
    with st.sidebar:
        st.title("🧮 Menu Interativo")
        st.markdown("Explore ferramentas focadas na sua jornada.")
        
        opcao = st.radio("Selecione a Ferramenta:", 
                         ["Chat Relacionamento", "Simulador (Juros Compostos)", "Catálogo de Produtos"])
        
        st.markdown("---")
        
        if opcao == "Simulador (Juros Compostos)":
            st.subheader("📈 Juros Compostos")
            st.markdown("Simule a evolução do seu dinheiro.")
            capital = st.number_input("Capital Inicial (R$):", min_value=0.0, value=1000.0, step=100.0)
            aporte = st.number_input("Aporte Mensal (R$):", min_value=0.0, value=200.0, step=50.0)
            taxa_anual = st.number_input("Taxa de Juros Anual (%):", min_value=0.0, value=10.0, step=0.5)
            meses = st.slider("Prazo (meses):", min_value=1, max_value=360, value=60)
            
            if st.button("Calcular"):
                taxa_mensal = (1 + taxa_anual/100)**(1/12) - 1
                saldo = capital
                
                meses_lista = [0]
                saldo_lista = [capital]
                
                for i in range(1, meses + 1):
                    saldo = saldo * (1 + taxa_mensal) + aporte
                    meses_lista.append(i)
                    saldo_lista.append(saldo)
                    
                df = pd.DataFrame({"Mês": meses_lista, "Patrimônio Total (R$)": saldo_lista})
                
                st.success(f"Saldo Estimado: R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                
                fig = px.line(df, x="Mês", y="Patrimônio Total (R$)", title="Crescimento Patrimonial")
                fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=300)
                st.plotly_chart(fig, use_container_width=True)
                
        elif opcao == "Catálogo de Produtos":
            st.subheader("📚 Entenda os Produtos")
            st.markdown("Escolha para aprender o básico.")
            produto = st.selectbox("Produto Financeiro", ["Reserva de Emergência", "CDB", "Tesouro Direto", "Ações"])
            
            if produto == "Reserva de Emergência":
                st.info("**Reserva de Emergência**\nDinheiro guardado para imprevistos. O ideal é ter de 6 a 12 meses do seu custo de vida mensal de fácil acesso (liquidez diária).")
            elif produto == "CDB":
                st.info("**CDB**\nEmpréstimo que você faz ao banco. Seguro (FGC) e com opções atreladas ao CDI.")
            elif produto == "Tesouro Direto":
                st.info("**Tesouro Direto**\nTítulos públicos. Você financia o governo. Várias opções: Selic (emergência), IPCA+ (contra inflação).")
            elif produto == "Ações":
                st.info("**Ações**\nPedaços de uma empresa. Ao comprar, você vira sócio. Renda variável, pode ter altos ganhos ou perdas no curto prazo.")
                
            if st.button(f"Saber mais sobre {produto} no chat"):
                st.session_state.messages.append({"role": "user", "content": f"Pode me explicar detalhadamente sobre {produto}? Vantagens e riscos?"})

        st.markdown("---")
        st.subheader("💡 FAQ Rápido")
        if st.button("Por que investir?"):
             st.session_state.messages.append({"role": "user", "content": "Por que devo investir meu dinheiro e não deixar na conta corrente?"})
        if st.button("Inflação e Investimentos"):
             st.session_state.messages.append({"role": "user", "content": "Como a inflação prejudica meu dinheiro se eu não investir corretamente?"})

def render_chat():
    st.title("🤖 FinAI - Seu Gêmeo Financeiro")
    st.markdown("Olá! Eu trago uma **experiência digital personalizada**. Pode me consultar livremente para entender seu dinheiro de forma inteligente e segura. *Você também pode interagir com o menu à esquerda para atalhos!*")
    
    if not API_KEY:
        st.error("⚠️ **API Key do Gemini não encontrada**. Adicione o seu GEMINI_API_KEY no arquivo gerador de variáveis de ambiente (`.env`).")
        return
        
    # Exibir histórico na tela principal
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input do Chat
    if prompt := st.chat_input("Ex: Como começar a investir 100 reais?"):
        # Repassa o input do usuario para a interface
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Envia ao LLM e Exibe Resposta
        with st.chat_message("assistant"):
            try:
                with st.spinner("Refletindo em suas finanças..."):
                    response = st.session_state.chat_session.send_message(prompt)
                    resposta_final = response.text
                    st.markdown(resposta_final)
                    
                st.session_state.messages.append({"role": "assistant", "content": resposta_final})
            except Exception as e:
                erro = f"Desculpe, ocorreu um erro na comunicação com a API: {e}"
                st.error(erro)
                st.session_state.messages.append({"role": "assistant", "content": erro})


def main():
    render_sidebar()
    render_chat()

if __name__ == "__main__":
    main()
