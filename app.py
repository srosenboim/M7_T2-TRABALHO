import streamlit as st
import anthropic
import base64

st.set_page_config(
    page_title="QuantAI — Quantificação e Orçamento com IA",
    page_icon="📐",
    layout="wide",
)

st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #ffffff; }
  [data-testid="stHeader"] { background: #ffffff; }
  [data-testid="stSidebar"] {
    background: #fff8f3;
    border-right: 2px solid #ff8c3a;
  }
  .main .block-container { padding-top: 2rem; max-width: 1100px; }

  h1, h2, h3, h4, h5 { color: #1a1a1a !important; }
  p, li, label { color: #1a1a1a !important; }

  [data-testid="stMarkdownContainer"] h1 { color: #ff6b00 !important; }
  [data-testid="stMarkdownContainer"] h2 { color: #ff8c3a !important; }
  [data-testid="stMarkdownContainer"] h3 { color: #1a1a1a !important; }

  .stButton > button {
    background: #ff6b00 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    font-size: 1rem !important;
    width: 100%;
  }
  .stButton > button:hover { background: #ff8c3a !important; }
  .stButton > button:disabled { background: #ffcca0 !important; color: #fff !important; }

  [data-testid="stFileUploader"] {
    border: 2px dashed #ff8c3a !important;
    border-radius: 10px !important;
    background: #fff8f3 !important;
  }

  [data-testid="stTextArea"] textarea {
    border: 1.5px solid #ffcca0 !important;
    border-radius: 8px !important;
    background: #fff8f3 !important;
    color: #1a1a1a !important;
  }

  [data-testid="stSelectbox"] > div {
    border: 1.5px solid #ffcca0 !important;
    border-radius: 8px !important;
    background: #fff8f3 !important;
  }

  [data-testid="stPasswordInput"] input {
    border: 1.5px solid #ffcca0 !important;
    background: #fff8f3 !important;
    color: #1a1a1a !important;
  }

  .stSuccess { background: #fff3e8 !important; border-left: 4px solid #ff6b00 !important; color: #1a1a1a !important; }
  .stWarning { background: #fff8f3 !important; }
  .stAlert { color: #1a1a1a !important; }

  table { border-collapse: collapse; width: 100%; }
  thead tr { background: #ff6b00 !important; color: white !important; }
  thead th { color: white !important; padding: 10px 14px !important; font-weight: 600 !important; }
  tbody tr:nth-child(even) { background: #fff8f3; }
  tbody tr:nth-child(odd) { background: #ffffff; }
  tbody td { padding: 8px 14px !important; color: #1a1a1a !important; border-bottom: 1px solid #ffe0c8 !important; }

  .sidebar-title { color: #ff6b00 !important; font-size: 1.3rem; font-weight: 700; }
  footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="sidebar-title">⚡ QuantAI</p>', unsafe_allow_html=True)
    st.markdown("Quantificação e orçamento de projetos com Inteligência Artificial.")
    st.divider()

    api_key = st.text_input(
        "🔑 API Key (Anthropic)",
        type="password",
        placeholder="sk-ant-...",
        help="Obtenha sua chave em console.anthropic.com"
    )

    st.divider()
    st.markdown("**Configurações**")

    currency = st.selectbox("Moeda", ["BRL — Real", "USD — Dólar", "EUR — Euro"])
    price_table = st.selectbox("Tabela de preços", ["SINAPI (Brasil)", "PINI", "Preços de mercado"])
    analysis_type = st.selectbox("Tipo de análise", ["Análise completa", "Só estrutura", "Só acabamentos", "Só instalações"])

    st.divider()
    st.caption("Desenvolvido por Sergio Rosenboim\nArquiteto | BIM, Data & AI")

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown("# 📐 QuantAI")
st.markdown("##### Quantificação e Orçamento com Inteligência Artificial")
st.markdown("Envie a planta do seu projeto e receba automaticamente os quantitativos de materiais e o orçamento estimado.")
st.divider()

col1, col2 = st.columns([3, 2])
with col1:
    uploaded_file = st.file_uploader(
        "📁 Envie a planta do projeto",
        type=["pdf", "png", "jpg", "jpeg", "webp"],
        help="Planta baixa, corte, fachada ou qualquer imagem do projeto"
    )
with col2:
    context = st.text_area(
        "💬 Contexto adicional (opcional)",
        placeholder="Ex: Apartamento de 80m² em SP. Reforma de banheiros e cozinha. Padrão médio.",
        height=120
    )

# ── Visualizador ──────────────────────────────────────────────────────────────
if uploaded_file is not None:
    is_pdf = uploaded_file.type == "application/pdf"
    file_bytes = uploaded_file.read()

    with col1:
        if is_pdf:
            b64 = base64.b64encode(file_bytes).decode("utf-8")
            pdf_display = f'''<iframe src="data:application/pdf;base64,{b64}" width="100%" height="260px" style="border: 2px solid #ff8c3a; border-radius: 10px; margin-top: 8px;"></iframe>'''
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.image(file_bytes, use_container_width=True)

    uploaded_file.seek(0)

st.markdown("")
analyze = st.button("⚡ Analisar com IA", disabled=not (uploaded_file and api_key))

if uploaded_file and not api_key:
    st.warning("Insira sua API Key da Anthropic na barra lateral para continuar.")

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze and uploaded_file and api_key:

    currency_code = currency.split(" — ")[0]
    symbols = {"BRL": "R$", "USD": "US$", "EUR": "€"}
    sym = symbols.get(currency_code, "R$")

    prompt = f"""Você é um engenheiro de custos especialista em orçamentos de construção civil no Brasil.

Analise o projeto enviado e gere um orçamento detalhado.

{f'Contexto: {context}' if context else ''}
Moeda: {currency_code} ({sym})
Tabela de referência: {price_table}
Escopo: {analysis_type}

Responda em markdown com estas seções exatamente nesta ordem:

## 📋 Resumo do Projeto
Uma descrição curta do projeto identificado, área estimada, número de ambientes e padrão de acabamento.

## 🏠 Ambientes Identificados
Uma tabela markdown com colunas: Ambiente | Área (m²) | Perímetro (m) | Pé-direito (m)

## 💰 Quantitativos e Orçamento
Uma tabela markdown com colunas: Categoria | Item | Especificação | Qtd | Un | Custo Unit. ({sym}) | Total ({sym})
Ao final da tabela, adicione uma linha de TOTAL GERAL em negrito.

## 💡 Observações
Premissas adotadas e recomendações importantes.

Use valores realistas baseados em {price_table}. Se não conseguir identificar dimensões exatas, estime com base nas proporções visíveis."""

    file_bytes = uploaded_file.read()
    file_b64 = base64.standard_b64encode(file_bytes).decode("utf-8")
    is_pdf = uploaded_file.type == "application/pdf"

    with st.spinner("🔍 Analisando o projeto com IA... isso pode levar até 30 segundos."):
        try:
            client = anthropic.Anthropic(api_key=api_key)

            if is_pdf:
                content_blocks = [
                    {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": file_b64}},
                    {"type": "text", "text": prompt}
                ]
                response = client.beta.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=8000,
                    messages=[{"role": "user", "content": content_blocks}],
                    betas=["pdfs-2024-09-25"]
                )
            else:
                media_type = uploaded_file.type or "image/jpeg"
                content_blocks = [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": file_b64}},
                    {"type": "text", "text": prompt}
                ]
                response = client.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=8000,
                    messages=[{"role": "user", "content": content_blocks}]
                )

            result = response.content[0].text
            st.session_state["result"] = result

        except anthropic.AuthenticationError:
            st.error("❌ API Key inválida. Verifique sua chave em console.anthropic.com")
            st.stop()
        except anthropic.RateLimitError:
            st.error("❌ Limite de requisições atingido. Aguarde e tente novamente.")
            st.stop()
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")
            st.stop()

# ── Results ───────────────────────────────────────────────────────────────────
if "result" in st.session_state:
    st.divider()
    st.success("✅ Análise concluída!")
    st.markdown(st.session_state["result"])
    st.divider()
    st.download_button(
        label="⬇ Baixar resultado (.md)",
        data=st.session_state["result"],
        file_name="orcamento_quantai.md",
        mime="text/markdown"
    )
