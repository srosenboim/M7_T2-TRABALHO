# QuantAI — Quantificação e Orçamento com Inteligência Artificial

> Aplicação web em Python/Streamlit que utiliza visão computacional via LLM (Claude) para analisar plantas arquitetônicas e gerar automaticamente quantitativos de materiais e orçamentos estimados.

---

## 🎯 Objetivo

Desenvolver uma ferramenta que elimine a etapa manual de leitura e interpretação de plantas para quantificação, utilizando modelos de linguagem multimodais (LLMs com visão) para automatizar o processo de orçamentação na construção civil.

---

## 🧠 Como funciona

```
[PDF ou Imagem do projeto] → [Claude Vision API] → [JSON estruturado] → [Dashboard Streamlit]
```

1. **Upload** — o usuário envia PDF ou imagem da planta
2. **Contexto** — informações complementares opcionais (localização, padrão, escopo)
3. **Análise por IA** — arquivo enviado à API da Anthropic (Claude com visão)
4. **Extração estruturada** — modelo retorna JSON com ambientes, quantitativos e orçamento
5. **Visualização** — dashboard interativo com tabs por categoria
6. **Exportação** — resultado em JSON para uso em outras ferramentas

---

## 🛠️ Stack técnica

| Componente | Tecnologia |
|------------|-----------|
| Frontend/Backend | Python + Streamlit |
| IA / LLM | Anthropic Claude API (claude-opus-4-5 com visão) |
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

1. Suba o repositório no GitHub
2. Acesse **share.streamlit.io**
3. Conecte o repositório
4. Defina `app.py` como arquivo principal
5. Clique em **Deploy**

---

## ⚙️ Configurações disponíveis

| Opção | Valores |
|-------|---------|
| **Moeda** | BRL, USD, EUR |
| **Tabela de preços** | SINAPI, PINI, Mercado |
| **Tipo de análise** | Completa, Estrutura, Acabamentos, Instalações |

---

## 📊 Saída gerada

- **Resumo**: custo total, área, custo/m², padrão de acabamento
- **Ambientes**: lista com área, perímetro e pé-direito estimados
- **Quantitativos**: itens por categoria com unidade, quantidade e custo
- **Orçamento**: distribuição percentual por categoria
- **Observações**: premissas e limitações da análise

---

## ⚠️ Limitações

- Valores são estimativas para estudos de viabilidade
- Precisão depende da qualidade da imagem
- Não substitui orçamento detalhado por profissional habilitado

## 🔄 Evoluções futuras

- [ ] Leitura de arquivos IFC (BIM)
- [ ] Exportação em Excel e PDF
- [ ] Banco de preços editável
- [ ] Comparação entre orçamentos
- [ ] Integração com SINAPI online

---

*Desenvolvido por Sergio Rosenboim — Arquiteto | BIM, Data & AI for Construction*  
*Mestrado em Inteligência Artificial para Arquitetura e Construção*
