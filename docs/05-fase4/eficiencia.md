# 5.1 Eficiência de Desempenho

## 5.1.1 Introdução
Resultados do objetivo GQM e das métricas definidas na Fase 2, contextualizando o que foi executado.

Este capítulo apresenta os resultados coletados para a característica de **Eficiência de Desempenho** do modelo Qwen 2.5 3B executado localmente via Ollama. Os dados estão organizados por ambiente operacional e avaliam as métricas de tempo de resposta, throughput e consumo de recursos.


## 5.1.2 Resultados Coletados
A seguir estão os resultados coletados através dos scripts da pasta `/scripts/desempenho` para Windows 11 e Zorin OS 18.1 Core.

### Windows 11

**Tabela 1: Resultados das Métricas de Eficiência e Recursos (Windows 11)**

| Característica | ID | Métrica | Critério | Resultado | Veredicto |
|---|---|---|---|---|---|
| Eficiência | **[ED-1.1](../04-fase3/eficiencia.md#ref-ed11)**| TTFT (~256 tok) | ≤ 5 s | 166,0 ms | Aprovado |
| Eficiência | **[ED-1.2](../04-fase3/eficiencia.md#ref-ed12)** | TPS (~256 tok) | ≥ 5 tokens/s | 52,18 t/s | Aprovado |
| Eficiência | **[ED-1.3](../04-fase3/eficiencia.md#ref-ed13)**| Load time (~256 tok) | ≤ 30 s | 138,66 ms | Aprovado |
| Eficiência | **[ED-2.1](../04-fase3/eficiencia.md#ref-ed21)** | Consumo de RAM | ≤ 6 GB | 761,46 MB | Aprovado |
| Eficiência | **[ED-2.2](../04-fase3/eficiencia.md#ref-ed22)**| Uso de CPU | ≤ 90 % | 8,27 % | Aprovado |
| Eficiência | **[ED-2.3](../04-fase3/eficiencia.md#ref-ed23)** | Eficiência de recurso | ≥ 0,5 | 8,49 | Aprovado |

<p align="center"><b>Autores:</b> <a href="https://github.com/GDveAlves">Gabriel Alves</a> e <a href="https://github.com/Matheus-06">Matheus Pinheiro</a>, 2026.</p>

#### Capacidade e escalonamento (Windows 11)

**Tabela 2: Resultados de Capacidade e Escalonamento de Contexto (Windows 11)**

| Característica | ID | Métrica | Critério | Resultado | Veredicto |
|---|---|---|---|---|---|
| Eficiência | **[ED-3.1](../04-fase3/eficiencia.md#ref-ed31)**| Escalonamento de contexto 512 t | ≤ 4,0 | 1,1504 | Aprovado |
| Eficiência | **[ED-3.1](../04-fase3/eficiencia.md#ref-ed31)**| Escalonamento de contexto 1024 t | ≤ 4,0 | 1,0588 | Aprovado |
| Eficiência | **[ED-3.1](../04-fase3/eficiencia.md#ref-ed31)**| Escalonamento de contexto 2048 t | ≤ 4,0 | 1,23 | Aprovado |
| Eficiência | **[ED-3.1](../04-fase3/eficiencia.md#ref-ed31)**| Escalonamento de contexto 4096 t | ≤ 4,0 | 1,2742 | Aprovado |
| Eficiência | **[ED-3.2](../04-fase3/eficiencia.md#ref-ed32)**| Crescimento KV Cache 512 t (~477 tok) | ≤ 0,5 MB/token | 0,0067 MB/token | Aprovado |
| Eficiência | **[ED-3.2](../04-fase3/eficiencia.md#ref-ed32)**| Crescimento KV Cache 1024 t (~925 tok) | ≤ 0,5 MB/token | 0,0029 MB/token | Aprovado |
| Eficiência | **[ED-3.2](../04-fase3/eficiencia.md#ref-ed32)**| Crescimento KV Cache 2048 t (~1821 tok) | ≤ 0,5 MB/token | 0,0014 MB/token | Aprovado |
| Eficiência | **[ED-3.2](../04-fase3/eficiencia.md#ref-ed32)**| Crescimento KV Cache 4096 t (~3613 tok) | ≤ 0,5 MB/token | 0,0004 MB/token | Aprovado |

<p align="center"><b>Autores:</b> <a href="https://github.com/GDveAlves">Gabriel Alves</a> e <a href="https://github.com/Matheus-06">Matheus Pinheiro</a>, 2026.</p>

### Zorin OS 18.1 Core

**Tabela 3: Resultados das Métricas de Eficiência e Recursos (Zorin OS)**

| Característica | ID | Métrica | Critério | Resultado | Veredicto |
|---|---|---|---|---|---|
| Eficiência | **[ED-1.1](../04-fase3/eficiencia.md#ref-ed11)** | TTFT (~256 tok) | ≤ 5 s | 216,28 ms | Aprovado |
| Eficiência | **[ED-1.2](../04-fase3/eficiencia.md#ref-ed12)**| TPS (~256 tok) | ≥ 5 tokens/s | 50,52 t/s | Aprovado |
| Eficiência | **[ED-1.3](../04-fase3/eficiencia.md#ref-ed13)** | Load time (~256 tok) | ≤ 30 s | 1,62 s | Aprovado |
| Eficiência | **[ED-2.1](../04-fase3/eficiencia.md#ref-ed21)** | Consumo de RAM | ≤ 6 GB | 755,16 MB | Aprovado |
| Eficiência | **[ED-2.2](../04-fase3/eficiencia.md#ref-ed22)**| Uso de CPU | ≤ 90 % | 3,46 % | Aprovado |
| Eficiência | **[ED-2.3](../04-fase3/eficiencia.md#ref-ed23)**| Eficiência de recurso | ≥ 0,5 | 19,02 | Aprovado |

<p align="center"><b>Autores:</b> <a href="https://github.com/GDveAlves">Gabriel Alves</a> e <a href="https://github.com/Matheus-06">Matheus Pinheiro</a>, 2026.</p>

#### Capacidade e escalonamento (Zorin OS 18.1 Core)

**Tabela 4: Resultados de Capacidade e Escalonamento de Contexto (Zorin OS)**

| Característica | ID | Métrica | Critério | Resultado | Veredicto |
|---|---|---|---|---|---|
| Eficiência | **[ED-3.1](../04-fase3/eficiencia.md#ref-ed31)** | Escalonamento de contexto 512 t | ≤ 4,0 | 0.9996 | Aprovado |
| Eficiência | **[ED-3.1](../04-fase3/eficiencia.md#ref-ed31)**| Escalonamento de contexto 1024 t | ≤ 4,0 | 0.9855 | Aprovado |
| Eficiência | **[ED-3.1](../04-fase3/eficiencia.md#ref-ed31)**| Escalonamento de contexto 2048 t | ≤ 4,0 | 0.9969 | Aprovado |
| Eficiência | **[ED-3.1](../04-fase3/eficiencia.md#ref-ed31)** | Escalonamento de contexto 4096 t | ≤ 4,0 | 1.0061 | Aprovado |
| Eficiência | **[ED-3.2](../04-fase3/eficiencia.md#ref-ed32)** | Crescimento KV Cache 1024 t (~925 tok) | ≤ 0,5 MB/token | 0,0064 MB/token | Aprovado |
| Eficiência | **[ED-3.2](../04-fase3/eficiencia.md#ref-ed32)** | Crescimento KV Cache 2048 t (~1821 tok) | ≤ 0,5 MB/token | 0,1031 MB/token | Aprovado |
| Eficiência | **[ED-3.2](../04-fase3/eficiencia.md#ref-ed32)** | Crescimento KV Cache 4096 t (~3613 tok) | ≤ 0,5 MB/token | 0,0216 MB/token | Aprovado |

<p align="center"><b>Autores:</b> <a href="https://github.com/GDveAlves">Gabriel Alves</a> e <a href="https://github.com/Matheus-06">Matheus Pinheiro</a>, 2026.</p>

## 5.1.3 Análise por Questão GQM

Os resultados de TTFT, TPS e Load Time mostram que o modelo atende aos critérios de tempo definidos na Fase 3 em ambos os ambientes. O consumo de recursos também se manteve bem abaixo dos limites previstos para RAM e CPU.

Os testes de capacidade ED-3.1 foram aprovados em todos os tamanhos de contexto analisados em ambos os ambientes, indicando escalonamento aceitável para os limites definidos.

A métrica **ED-3.2 (Taxa de Crescimento do KV Cache - KVCGR)** foi válida e aprovada sob **ambos os sistemas**, com valores positivos e crescimento muito abaixo do limiar de referência (≤ 0,5 MB/token), evidenciando que o gerenciamento de memória do KV Cache é estável mesmo com aumento de contexto.

**Tabela 4.5: Análise por Questão GQM (Q1–Q4)**

| Questão | Métrica Principal | Critério | Status |
| :--- | :--- | :--- | :--- |
| Q1 — Latência interativa | TTFT mediana | ≤ 3s (CPU) | Aprovada |
| Q1 — Geração em tempo real | TPS | ≥ 10 tok/s | Aprovada |
| Q2 — Consumo de RAM | RAM_inferência | ≤ 4 GB | Aprovada |
| Q2 — Consumo de CPU | CPU_uso | ≤ 90% | Aprovada |
| Q3 — Escalonamento de contexto | CSF | ≤ 4,0 para 4096 tok | Aprovado |

<p align="center"><b>Autores:</b> <a href="https://github.com/GDveAlves">Gabriel Alves</a> e <a href="https://github.com/Matheus-06">Matheus Pinheiro</a>, 2026.</p>

## 5.1.4 Análise Comparativa entre Ambientes

Comparação direta por métrica, calculando o desvio relativo de desempenho entre os dois ambientes. Responde à questão central: há diferença significativa entre os sistemas operacionais?

**Tabela 5: Análise Comparativa Windows × Linux**

| Métrica | Windows 11 | Linux (Zorin OS) | Desvio (%) | Critério |
| :--- | :---: | :---: | :---: | :---: |
| TTFT (~256 tok) | 166,0 ms | 216,28 ms | 23,25% | ≤ 20% |
| TPS | 52,18 t/s | 50,52 t/s | 3,18% | Desvio ≤ 20% |
| RAM pico | 761,46 MB | 755,16 MB | 0,83% | ≤ 6 GB |
| CPU médio (%) | 8,27% | 3,46% | 58,16% | ≤ 90% |

> Desvio calculado como `|W − L| / max(W, L) × 100`.

<p align="center"><b>Autores:</b> <a href="https://github.com/GDveAlves">Gabriel Alves</a> e <a href="https://github.com/Matheus-06">Matheus Pinheiro</a>, 2026.</p>

- Windows 11 apresentou menor latência de resposta (TTFT 166 ms vs 216 ms) e consumo de RAM praticamente idêntico entre os ambientes (761 MB vs 755 MB). No entanto, o uso de CPU foi consideravelmente maior no Windows (8,27% vs 3,46%), refletindo diferenças no agendador de processos e na integração do Ollama com cada sistema operacional. Ambos os ambientes passam em todas as métricas de desempenho.

## 5.1.5 Interpretação e Discussão

O Qwen 2.5 3B via Ollama se mostrou viável em 16 GB sem GPU em ambos os sistemas. Os resultados indicam que a solução é operável com latência de resposta adequada e consumo de recursos controlado.

As diferenças entre os ambientes são perceptíveis mas não determinantes: Windows 11 apresentou TTFT ligeiramente inferior, enquanto Zorin OS demonstrou uso de CPU mais eficiente. O consumo de RAM foi equivalente entre os ambientes. Ambos atingiram aprovação em todas as métricas principais de ED-1, ED-2 e ED-3.

## [Tabelas de dados (CSV)](https://docs.google.com/spreadsheets/d/1u2LjemT9oylyIi0hCg5z5eIDNr50ojhL29X8rfrarIM/edit?usp=sharing)

## Histórico de Versão
 
| Versão | Data | Descrição | Autor | Revisor |
|---|---|---|---|---|
| 1.0 | 12/06/2026 | Criação do documento |[Gabriel](https://github.com/GDevAlves) | [Renata Quadros](https://github.com/RenataKurzawa) | 
| 1.1 | 13/06/2026 | Adição de dados de desempenho |[Matheus Pinheiro](https://github.com/matheus-06) | [Renata Quadros](https://github.com/RenataKurzawa) | 
| 1.2 | 23/06/2026 | Ajuste do critério do CSF, inversão do sinal do REI e padronização visual das tabelas | [Renata Quadros](https://github.com/RenataKurzawa) | [Giovana Barbosa](https://github.com/gio221) |
| 1.3 | 23/06/2026 | Correção do TTFT (s para ms) e classificação da métrica ED-3.2 (KVCGR) como Inconclusiva/Inválida | [Johnnatan Salles](https://github.com/jsalless) | [Renata Quadros](https://github.com/RenataKurzawa) |
| 1.4 | 23/06/2026 | Atualização dos dados Windows; correção de labels de contexto e Tabela 5 | [Matheus Pinheiro](https://github.com/matheus-06) | ()[] |