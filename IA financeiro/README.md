# Projeto IA Financeiro - DIO

Esta é uma solução digital focada no relacionamento financeiro, integrando uma interface conversacional fundamentada em modelos de inteligência artificial (Gemini API) e boas práticas de UX.

## 🚀 O Desafio
O desafio propõe a criação de uma experiência digital voltada ao relacionamento financeiro, guiada por IA generativa e fundamentada em boas práticas de experiência do usuário. A solução consolida aprendizados em IA, Python, dados e UX, incluindo funcionalidades como:
- Compreensão de linguagem natural.
- Respostas contextualizadas.
- Simulações simples.
- FAQs inteligentes e explicações de produtos.

## 🛠️ Solução Construída
Desenvolvemos o aplicativo **FinAI**, utilizando **Streamlit** (para interface do usuário) e **Google Generative AI (Gemini 1.5 Pro)** para processamento de linguagem natural. Ações da solução:
1. **Gêmeo Financeiro (Chat Bot)**: Assistente persistente com interações claras, seguras e personalizadas. O histórico da conversa é mantido durante a sessão inteira do usuário, mantendo o contexto. Não são realizadas recomendações diretas, mantendo caráter educacional da plataforma.
2. **Simulador Interativo de Juros Compostos**: Ferramenta de visualização de crescimento de patrimônio por meio de gráficos usando Plotly e Pandas.
3. **Catálogo Explicativo e FAQs**: Recursos didáticos no menu interativo (sidebar) para explicar produtos como CDB e Tesouro Direto, servindo de atalho param enviar *prompts* diretos para o modelo (prompt injection dinâmico).

## 📦 Como Usar

1. **Abra o terminal neste diretório**.

2. **Crie um ambiente virtual e instale as dependências recomendadas**:
   ```bash
   python -m venv venv
   # No Windows (PowerShell):
   .\venv\Scripts\activate
   # No Mac/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Configure as Variáveis de Ambiente**:
   - Faça uma cópia do `.env.example` e renomeie para `.env`.
   - Adicione sua API Key do Google AI Studio à variável `GEMINI_API_KEY`:
     ```env
     GEMINI_API_KEY=sua_chave_aqui_sem_aspas
     ```

4. **Inicie o projeto**:
   ```bash
   streamlit run app.py
   ```
   *O aplicativo irá abrir automaticamente no seu navegador padrão (geralmente http://localhost:8501).*

## 🎨 Prints e Navegação
- **Interface Principal**: Aba de bate-papo semelhante ao ChatGPT.
- **Barra Lateral**: Interação guiada, onde é possível alternar entre Chat, Simulações, e Catálogo. As opções do catálogo geram automaticamente requisições complexas no bate-papo, poupando digitação do usuário e gerando engajamento.
