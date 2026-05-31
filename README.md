# QuantAI — Quantificação e Orçamento com Inteligência Artificial

> Aplicação web em Python/Streamlit que utiliza visão computacional via LLM (Claude) para analisar plantas arquitetônicas e gerar automaticamente quantitativos de materiais e orçamentos estimados.

**Zigurat — Trabalho M7_T2**

---

## 🎯 Objetivo

Eliminar a etapa manual de leitura e interpretação de plantas para quantificação, utilizando modelos de linguagem multimodais (LLMs com visão) para automatizar o processo de orçamentação na construção civil.

---

## 🧠 Como funciona

```
[PDF ou Imagem] → [Visualização prévia] → [Claude Vision API] → [Tabelas em markdown] → [Export Excel]
```

1. **Upload** — usuário envia PDF ou imagem da planta
2. **Preview** — primeira página do PDF é renderizada como imagem
3. **Contexto** — informações complementares opcionais
4. **Análise por IA** — Claude interpreta o projeto e gera orçamento em markdown
5. **Visualização** — tabelas de ambientes, quantitativos e orçamento
6. **Exportação** — resultado em Excel (.xlsx) formatado

---

## 🛠️ Stack técnica

| Componente | Tecnologia |
|------------|-----------|
| Frontend/Backend | Python + Streamlit |
| IA / LLM | Anthropic Claude API (claude-opus-4-5 com visão) |
| Visualização PDF | PyMuPDF (fitz) |
| Exportação | openpyxl (Excel .xlsx) |
| Hospedagem | Streamlit Cloud (gratuito) |
| Repositório | GitHub (privado) |

---

## 📦 Estrutura do projeto

```
quant-ai/
├── app.py              # Aplicação principal
├── requirements.txt    # Dependências Python
├── README.md           # Esta documentação
└── ONE-PAGE.md         # Resumo do processo de trabalho
```

---

## 🚀 Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy no Streamlit Cloud

1. Suba o repositório no GitHub (privado)
2. Acesse **share.streamlit.io**
3. Conecte o repositório e autorize acesso privado
4. Defina `app.py` como arquivo principal
5. Clique em **Deploy**

**URL pública:** `https://quantai-m4t2-sergio.streamlit.app`

---

## ⚙️ Configurações disponíveis

| Opção | Valores |
|-------|---------|
| **Moeda** | BRL, USD, EUR |
| **Tabela de preços** | SINAPI, PINI, Mercado |
| **Tipo de análise** | Completa, Estrutura, Acabamentos, Instalações |
| **Contexto** | Texto livre com informações do projeto |

---

## 📊 Saída gerada

- **Resumo do projeto** — descrição, área, ambientes, padrão
- **Tabela de ambientes** — área, perímetro e pé-direito estimados
- **Tabela de quantitativos** — itens por categoria com unidade, quantidade e custo
- **Total geral** — soma de todos os itens
- **Observações** — premissas e limitações da análise
- **Export Excel** — arquivo `.xlsx` formatado com cores

---

## ⚠️ Limitações

- Valores são estimativas para estudos de viabilidade
- Precisão depende da qualidade e legibilidade do arquivo
- Não substitui orçamento detalhado por profissional habilitado

## 🔄 Evoluções futuras

- [ ] Leitura de arquivos IFC (BIM)
- [ ] Banco de preços editável pelo usuário
- [ ] Comparação entre orçamentos
- [ ] Integração com SINAPI online
- [ ] Relatório em PDF

---

*Zigurat — Trabalho M7_T2*
*Sergio Rosenboim — Arquiteto | BIM, Data & AI for Construction*
