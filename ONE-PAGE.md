# QuantAI — Resumo do Processo de Trabalho

**Aluno:** Sergio Rosenboim
**Disciplina:** Aplicações Web com Inteligência Artificial
**Entrega:** Aplicação Web — Quantificação/Orçamentação de Projeto
**Data:** 2025

---

## 🎯 Problema identificado

A quantificação e orçamentação de projetos de arquitetura é um processo manual, repetitivo e sujeito a erro humano. Requer leitura cuidadosa de plantas, cálculo de áreas e volumes, e pesquisa de preços em tabelas de referência (como SINAPI). Para estudos de viabilidade rápidos, esse processo pode levar horas de trabalho especializado.

---

## 💡 Solução proposta

Desenvolver uma aplicação web que utilize um **LLM multimodal com visão computacional** (Claude da Anthropic) para interpretar automaticamente imagens de projetos e retornar:
- Lista de ambientes identificados com estimativas de dimensão
- Quantitativos de materiais organizados por categoria (ABNT)
- Orçamento estimado com base em tabelas de referência

---

## 🔄 Processo de desenvolvimento

### 1. Definição do escopo (30 min)
- Análise do briefing: aplicação web funcional com IA para orçamentação
- Decisão de tecnologia: HTML/CSS/JS vanilla + Claude API (sem framework, máxima portabilidade)
- Modelagem do output: definição da estrutura JSON que a IA deve retornar

### 2. Engenharia de prompt (45 min)
O passo mais crítico. O prompt instrui o modelo a:
- Agir como engenheiro de custos e arquiteto especialista
- Identificar ambientes e estimar dimensões a partir da imagem
- Retornar JSON estruturado com categorias ABNT (Alvenaria, Revestimentos, Instalações, etc.)
- Considerar a tabela de preços e moeda selecionada pelo usuário
- Incluir observações sobre premissas e limitações

Técnicas aplicadas: role prompting, output formatting, chain-of-thought implícito na estrutura JSON, contextual grounding via parâmetros do usuário.

### 3. Desenvolvimento da interface (2 h)
- Upload de arquivo com drag-and-drop
- Preview da imagem antes do envio
- Controles de configuração (moeda, tabela de preços, tipo de análise)
- Feedback visual de progresso em 4 etapas (loading states)
- Renderização dinâmica dos resultados: cards de resumo, tabelas por categoria, barra de progresso por percentual, caixa de observações da IA
- Exportação do resultado em JSON

### 4. Integração com Claude API (30 min)
- Uso do endpoint `/v1/messages` com suporte a visão (`image` content block)
- Conversão da imagem para base64 no browser (FileReader API)
- Parsing robusto do JSON retornado pelo modelo (com fallback via regex)
- Tratamento de erros de API com mensagens claras ao usuário

### 5. Testes e refinamento (45 min)
- Testes com diferentes tipos de planta (baixa, corte, perspectiva)
- Ajustes no prompt para melhorar consistência do JSON
- Refinamento do CSS para legibilidade dos resultados

---

## 🧠 Papel da IA na aplicação

A IA não é um "acessório" — é o **motor central** da aplicação:

| Função | Tecnologia |
|--------|-----------|
| Interpretação visual da planta | Claude Vision (multimodal) |
| Identificação de ambientes | LLM (raciocínio espacial) |
| Cálculo de quantitativos | LLM (conhecimento técnico de engenharia) |
| Composição do orçamento | LLM (preços de referência SINAPI/PINI) |
| Observações técnicas | LLM (raciocínio crítico sobre limitações) |

---

## ✅ Resultados alcançados

- Aplicação funcional em arquivo único (zero dependências, zero backend)
- Deploy imediato via GitHub Pages
- Resposta em menos de 15 segundos para análise completa
- Output estruturado e exportável em JSON
- Interface profissional com dark theme e tipografia especializada

---

## 📚 Aprendizados

- **Prompt engineering é design de produto**: a qualidade do output depende diretamente da clareza e estrutura do prompt, não apenas do modelo
- **LLMs têm conhecimento técnico real**: o modelo demonstrou sólido conhecimento de orçamentação de obras, normas e unidades de medida
- **Visão computacional via LLM supera OCR**: o modelo não apenas lê texto da planta, mas interpreta espacialmente os ambientes
- **Single-file apps têm valor real**: para protótipos acadêmicos e MVPs, a simplicidade de deploy é uma vantagem competitiva

---

*"A IA mais útil é aquela que resolve um problema real de quem usa, não a mais tecnicamente complexa."*
