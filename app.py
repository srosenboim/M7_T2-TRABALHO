import streamlit as st
import anthropic
import base64
import json
import re
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuantAI — Quantificação e Orçamento com IA",
    page_icon="📐",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  [data-testid="stAppViewContainer"] { background: #0e0f0e; }
  [data-testid="stHeader"] { background: #0e0f0e; }
  [data-testid="stSidebar"] { background: #161714; border-right: 1px solid #2a2b28; }
  .main .block-container { padding-top: 2rem; max-width: 1000px; }

  h1 { font-size: 2.2rem !important; letter-spacing: -0.03em !important; }
  h2 { font-size: 1.3rem !important; }
  h3 { font-size: 1rem !important; }

  .metric-card {
    background: #161714;
    border: 1px solid #2a2b28;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
  }
  .metric-card .label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #8a8880;
    margin-bottom: 6px;
  }
  .metric-card .value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #b8f060;
    line-height: 1;
  }
  .metric-card .unit {
    font-size: 12px;
    color: #4a4b47;
    margin-top: 4px;
  }

  .obs-box {
    background: #161714;
    border-left: 3px solid #6fa020;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin-top: 1rem;
  }
  .obs-box p { color: #8a8880; font-size: 14px; line-height: 1.7; margin: 0; }

  .stButton > button {
    background: #b8f060 !important;
    color: #0a1a00 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    font-size: 1rem !important;
    width: 100%;
  }
  .stButton > button:hover {
    background: #cef080 !important;
    transform: translateY(-1px);
  }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚡ QuantAI")
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

    currency = st.selectbox(
        "Moeda",
        ["BRL — Real", "USD — Dólar", "EUR — Euro"]
    )

    price_table = st.selectbox(
        "Tabela de preços",
        ["SINAPI (Brasil)", "PINI", "Preços de mercado"]
    )

    analysis_type = st.selectbox(
        "Tipo de análise",
        ["Análise completa", "Só estrutura", "Só acabamentos", "Só instalações"]
    )

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
        placeholder="Ex: Apartamento de 80m² em São Paulo. Reforma de banheiros e cozinha. Padrão médio de acabamento.",
        height=120
    )

# ── Analyze button ────────────────────────────────────────────────────────────
st.markdown("")
analyze = st.button("⚡ Analisar com IA", disabled=not (uploaded_file and api_key))

if uploaded_file and not api_key:
    st.warning("Insira sua API Key da Anthropic na barra lateral para continuar.")

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze and uploaded_file and api_key:

    currency_code = currency.split(" — ")[0]
    symbols = {"BRL": "R$", "USD": "US$", "EUR": "€"}
    symbol = symbols.get(currency_code, "R$")

    prompt = f"""Você é um engenheiro de custos e arquiteto especialista em quantificação de obras e orçamentos de construção civil.

Analise cuidadosamente o arquivo de projeto enviado e gere um orçamento detalhado.

{f'Contexto fornecido pelo usuário: {context}' if context else ''}
Moeda: {currency_code} (símbolo: {symbol})
Tabela de preços de referência: {price_table}
Tipo de análise solicitada: {analysis_type}

Responda APENAS com um JSON válido, sem texto antes ou depois, sem blocos de código markdown. Use exatamente esta estrutura:

{{
  "resumo": {{
    "descricao": "descrição geral do projeto identificado",
    "area_total_m2": 0,
    "num_ambientes": 0,
    "padrao_acabamento": "baixo|médio|alto",
    "custo_total": 0,
    "custo_por_m2": 0,
    "moeda": "{currency_code}",
    "simbolo": "{symbol}"
  }},
  "ambientes": [
    {{
      "nome": "nome do ambiente",
      "area_m2": 0,
      "perimetro_m": 0,
      "pe_direito_m": 0
    }}
  ],
  "quantitativos": [
    {{
      "categoria": "Serviços Preliminares|Estrutura|Alvenaria|Cobertura|Revestimentos|Pavimentação|Esquadrias|Instalações Hidráulicas|Instalações Elétricas|Pintura|Louças e Metais|Outros",
      "item": "nome do item",
      "descricao": "especificação técnica",
      "unidade": "m²|m|un|kg|l|vb",
      "quantidade": 0,
      "custo_unitario": 0,
      "custo_total": 0
    }}
  ],
  "por_categoria": [
    {{
      "categoria": "nome",
      "total": 0,
      "percentual": 0
    }}
  ],
  "observacoes": "Observações importantes sobre limitações da análise, premissas adotadas e recomendações."
}}

Seja preciso e realista nos valores. Use preços de referência {price_table} para {currency_code}."""

    file_bytes = uploaded_file.read()
    file_b64 = base64.standard_b64encode(file_bytes).decode("utf-8")
    is_pdf = uploaded_file.type == "application/pdf"

    with st.spinner("🔍 Analisando o projeto com IA... isso pode levar até 30 segundos."):
        try:
            client = anthropic.Anthropic(api_key=api_key)

            if is_pdf:
                content = [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": file_b64
                        }
                    },
                    {"type": "text", "text": prompt}
                ]
                extra = {"betas": ["pdfs-2024-09-25"]}
            else:
                media_type = uploaded_file.type or "image/jpeg"
                content = [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": file_b64
                        }
                    },
                    {"type": "text", "text": prompt}
                ]
                extra = {}

            if is_pdf:
                response = client.beta.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": content}],
                    betas=["pdfs-2024-09-25"]
                )
            else:
                response = client.messages.create(
                    model="claude-opus-4-5",
                    max_tokens=4000,
                    messages=[{"role": "user", "content": content}]
                )

            raw = response.content[0].text
            cleaned = re.sub(r"```json|```", "", raw).strip()

            try:
                data = json.loads(cleaned)
            except Exception:
                match = re.search(r"\{[\s\S]*\}", cleaned)
                if match:
                    data = json.loads(match.group(0))
                else:
                    st.error("A IA não retornou um JSON válido. Tente novamente.")
                    st.stop()

            st.session_state["result"] = data
            st.session_state["symbol"] = symbol
            st.success("✅ Análise concluída!")

        except anthropic.AuthenticationError:
            st.error("❌ API Key inválida. Verifique sua chave em console.anthropic.com")
            st.stop()
        except anthropic.RateLimitError:
            st.error("❌ Limite de requisições atingido. Aguarde alguns instantes e tente novamente.")
            st.stop()
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")
            st.stop()

# ── Results ───────────────────────────────────────────────────────────────────
if "result" in st.session_state:
    data = st.session_state["result"]
    sym = st.session_state.get("symbol", "R$")
    r = data.get("resumo", {})

    st.divider()
    st.markdown("## 📊 Resultado da Análise")

    if r.get("descricao"):
        st.info(f"**Projeto identificado:** {r['descricao']}")

    # Summary cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Custo Total</div>
            <div class="value">{sym} {r.get('custo_total', 0):,.0f}</div>
            <div class="unit">{r.get('moeda','')}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Área Total</div>
            <div class="value">{r.get('area_total_m2', 0):,.1f}</div>
            <div class="unit">m²</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Custo / m²</div>
            <div class="value">{sym} {r.get('custo_por_m2', 0):,.0f}</div>
            <div class="unit">por metro quadrado</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Ambientes</div>
            <div class="value">{r.get('num_ambientes', len(data.get('ambientes', [])))}</div>
            <div class="unit">identificados</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Ambientes", "🔧 Quantitativos", "💰 Orçamento", "📋 Exportar"])

    with tab1:
        ambientes = data.get("ambientes", [])
        if ambientes:
            rows = []
            for a in ambientes:
                rows.append({
                    "Ambiente": a.get("nome", "—"),
                    "Área (m²)": f"{a.get('area_m2', 0):.2f}",
                    "Perímetro (m)": f"{a.get('perimetro_m', 0):.2f}",
                    "Pé-Direito (m)": f"{a.get('pe_direito_m', 0):.2f}",
                })
            st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum ambiente identificado.")

    with tab2:
        quantitativos = data.get("quantitativos", [])
        if quantitativos:
            grouped = {}
            for q in quantitativos:
                cat = q.get("categoria", "Outros")
                if cat not in grouped:
                    grouped[cat] = []
                grouped[cat].append(q)

            for cat, items in grouped.items():
                cat_total = sum(i.get("custo_total", 0) for i in items)
                with st.expander(f"**{cat}** — {sym} {cat_total:,.2f}", expanded=True):
                    rows = []
                    for q in items:
                        rows.append({
                            "Item": q.get("item", "—"),
                            "Especificação": q.get("descricao", "—"),
                            "Qtd": f"{q.get('quantidade', 0):,.2f}",
                            "Un.": q.get("unidade", "—"),
                            f"C.Unit. ({sym})": f"{q.get('custo_unitario', 0):,.2f}",
                            f"Total ({sym})": f"{q.get('custo_total', 0):,.2f}",
                        })
                    st.dataframe(rows, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum quantitativo gerado.")

    with tab3:
        por_cat = data.get("por_categoria", [])
        if por_cat:
            st.markdown("#### Distribuição por categoria")
            for c in por_cat:
                pct = c.get("percentual", 0)
                total = c.get("total", 0)
                st.markdown(f"**{c.get('categoria','—')}** — {sym} {total:,.2f}")
                st.progress(min(pct / 100, 1.0), text=f"{pct:.1f}%")

            st.divider()
            st.markdown(f"### 💰 Total Geral: {sym} {r.get('custo_total', 0):,.2f}")

        obs = data.get("observacoes", "")
        if obs:
            st.markdown(f"""<div class="obs-box">
                <p>💡 <strong style="color:#b8f060">Observações da IA</strong><br><br>{obs}</p>
            </div>""", unsafe_allow_html=True)

    with tab4:
        st.markdown("#### Exportar resultado")
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        st.download_button(
            label="⬇ Baixar JSON",
            data=json_str,
            file_name=f"orcamento_quantai_{timestamp}.json",
            mime="application/json"
        )

        st.markdown("**Preview do JSON:**")
        st.json(data)
