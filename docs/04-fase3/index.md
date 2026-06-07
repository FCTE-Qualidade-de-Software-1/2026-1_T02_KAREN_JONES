# Fase 3 — Projetar a Avaliação

## 1. Introdução

Esta Fase 3 marca a transição da especificação teórica para a preparação prática da avaliação de qualidade do Ollama executando o modelo Qwen 2.5 3B. Com base nas metas, questões e métricas GQM definidas nas fases anteriores para os atributos de **Eficiência de Desempenho** e **Portabilidade**, o objetivo deste artefato é formalizar o **Plano de Avaliação**.

O plano detalha:

- **Ambientes de Teste**: hardware, sistemas operacionais e ferramentas
- **Instrumentos de Medição**: scripts, logs, cronometragem e monitoramento de recursos
- **Procedimento Passo a Passo**: protocolo a ser executado na Fase 4 para coletar dados de maneira objetiva e reproduzível

---

## 2. Contexto da Avaliação

Conforme estabelecido no cenário de avaliação da Fase 1:

> "Uma estudante universitária com acesso instável à internet e um notebook básico (Windows 11, 8GB RAM, sem GPU) precisa de um assistente para estudos. Um colega utiliza a mesma ferramenta no Linux (Ubuntu). Eles buscam uma solução gratuita, privada e offline."

A avaliação visa verificar se o Qwen 2.5 3B via Ollama entrega um tempo de resposta aceitável nesse hardware e se a experiência de instalação e adaptação é equivalente entre os dois sistemas operacionais.

---

## 3. Escopo das Características Avaliadas

| Característica | Subcaracterísticas Avaliadas | Prioridade |
|----------------|------------------------------|------------|
| **Eficiência de Desempenho** | Comportamento Temporal, Utilização de Recursos, Capacidade | 5 (alta) |
| **Portabilidade** | Adaptabilidade, Instalabilidade | 5 (alta) |

---

## 4. Estrutura dos Artefatos

O plano de avaliação está organizado em dois documentos complementares:

1. **Plano de Avaliação - Eficiência de Desempenho**: detalha métricas, instrumentos e procedimentos para medir TTFT, uso de RAM/CPU e comportamento sob diferentes cargas de tokens.

2. **Plano de Avaliação - Portabilidade**: detalha métricas, instrumentos e procedimentos para medir tempo de instalação, taxa de sucesso e paridade funcional entre Windows e Linux.

---

## 5. Decisões a Serem Apoiadas

Os dados coletados fundamentarão as seguintes decisões:

| Decisão | Característica Relacionada |
|---------|---------------------------|
| Definir se 8GB de RAM são suficientes para execução estável | Eficiência de Desempenho |
| Determinar se há paridade de desempenho entre Windows e Linux | Eficiência de Desempenho / Portabilidade |
| Validar se o método de instalação é acessível para usuários leigos | Portabilidade |
| Decidir se o limite de contexto de tokens precisa ser ajustado | Eficiência de Desempenho |

---

# Bibliografia

> 1. ISO/IEC. *ISO/IEC TR 25021:2007: Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — Quality measure elements*. 1. ed. Genebra: International Organization for Standardization / International Electrotechnical Commission, 2007.

> 2. RAMOS, Cristiane Soares. *Medição baseada em objetivos: “Determinando o que medir”*. Material da disciplina FGA0278 - Qualidade de Software 1. Faculdade do Gama (FGA), Universidade de Brasília (UnB), 2024.

> 3. QWEN. *Qwen/Qwen2.5-3B-Instruct*. Repositório de modelos Hugging Face, 2024. Disponível em: <https://ollama.com/library/qwen2.5:3b>. Acesso em: 13 maio 2026.

> 4. QWEN TEAM. *Qwen2 Technical Report*. 2024. Disponível em: <https://arxiv.org/abs/2407.10671>. Acesso em: 13 maio 2026.

> 5. OLLAMA INC. *Ollama: The easiest way to build with open models*. Portal oficial de documentação, 2026. Disponível em: <https://ollama.com>. Acesso em: 13 maio 2026.


---

## Histórico de Versões

| Versão | Data | Descrição | Autor | Revisor |
|---|---|---|---|---|
| 1.0 | 04/06/2026 | Criação do documento | [Renata Quadros](https://github.com/RenataKurzawa) |[Giovana Barbosa](https://github.com/gio221) |
