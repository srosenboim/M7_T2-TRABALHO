# QuantAI — Resumo do Processo de Trabalho

**Aluno:** Sergio Rosenboim
**Curso:** Zigurat — Mestrado em Inteligência Artificial para Arquitetura e Construção
**Trabalho:** M7_T2 — Aplicação Web com IA para Quantificação e Orçamentação
**URL:** https://quantai-m4t2-sergio.streamlit.app

---

## 🎯 Problema identificado

A quantificação e orçamentação de projetos de arquitetura é um processo manual, repetitivo e sujeito a erro humano. Requer leitura cuidadosa de plantas, cálculo de áreas e volumes, e pesquisa de preços em tabelas de referência (SINAPI). Para estudos de viabilidade rápidos, esse processo pode levar horas de trabalho especializado.

---

## 💡 Solução desenvolvida

Aplicação web em Python/Streamlit que usa um **LLM multimodal com visão computacional** (Claude da Anthropic) para interpretar automaticamente PDFs e imagens de projetos e retornar:

- Preview visual da planta enviada
- Lista de ambientes com dimensões estimadas
- Quantitativos de materiais por categoria
- Orçamento com custo total e por item
- Exportação em Excel formatado

---

## 🔄 Processo de desenvolvimento

### 1. Definição do escopo
- Tema: Quantificação/Orçamentação de projeto
- Decisão: Python + Streamlit (resolve CORS, fácil deploy, linguagem do curso)
- IA como motor central, não acessório

### 2. Engenharia de prompt
O prompt instrui o modelo a:
- Agir como engenheiro de custos especialista
- Retornar markdown estruturado com tabelas (não JSON — mais robusto)
- Considerar tabela de preços e moeda selecionada
- Incluir observações sobre premissas e limitações

Técnicas: role prompting, output formatting, contextual grounding.

### 3. Desenvolvimento iterativo
- **v1:** HTML puro + Claude API → problema de CORS no browser local
- **v2:** Streamlit + JSON → truncamento em PDFs grandes
- **v3:** Streamlit + markdown/tabelas → robusto, sem truncamento
- **v4 (final):** + visualizador de PDF (PyMuPDF) + export Excel (openpyxl)

### 4. Deploy
- Repositório privado no GitHub
- Streamlit Cloud com autorização de acesso privado
- URL pública para acesso do professor

---

## 🧠 Papel da IA

A IA é o **motor central** da aplicação:

| Função | Tecnologia |
|--------|-----------|
| Interpretação visual da planta | Claude Vision (multimodal) |
| Identificação de ambientes | LLM (raciocínio espacial) |
| Cálculo de quantitativos | LLM (conhecimento técnico) |
| Composição do orçamento | LLM (preços SINAPI/PINI) |
| Observações técnicas | LLM (raciocínio crítico) |

---

## ✅ Resultado final

- App funcional hospedada no Streamlit Cloud
- Aceita PDF e imagens de qualquer tamanho
- Visualiza a planta antes da análise
- Gera tabelas de ambientes, quantitativos e orçamento
- Exporta resultado em Excel formatado com cores
- Professor insere a própria API key e usa livremente

---

## 📚 Aprendizados

- **Markdown > JSON para outputs de LLM:** mais robusto, sem risco de truncamento
- **Iteração é o método:** 4 versões até chegar na solução certa
- **Stack simples vence:** Streamlit resolveu em 1 arquivo o que levaria dias em outra stack
- **Prompt engineering é design de produto:** a qualidade do output depende diretamente da clareza do prompt

---

*"A melhor solução técnica é a que resolve o problema real do usuário — não a mais complexa."*

*Zigurat — Trabalho M7_T2 | Sergio Rosenboim*
