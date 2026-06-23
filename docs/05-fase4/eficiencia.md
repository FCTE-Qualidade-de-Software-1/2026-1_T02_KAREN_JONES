# 5.1 Eficiência de Desempenho

## 5.1.1 Introdução
Resultados do objetivo GQM e das métricas definidas na Fase 2, contextualizando o que foi executado.

Este capítulo apresenta os resultados coletados para a característica de **Eficiência de Desempenho** do modelo Qwen 2.5 3B executado localmente via Ollama. Os dados estão organizados por ambiente operacional e avaliam as métricas de tempo de resposta, throughput e consumo de recursos.

### 5.1.1.1 Alinhamento de Escopo (Carga Concorrente)

Conforme estabelecido e justificado no Plano de Avaliação [(Fase 3, Item 1.1)](../04-fase3/eficiencia.md#11-nota-de-escopo-sobre-metricas-de-carga-concorrente-q4--m4), as métricas de carga concorrente multiusuário, comumente referidas como Q4/M4 (Throughput Concorrente, Degradação de Latência e Taxa de Erros), não fazem parte do escopo de coleta deste relatório. 

## 5.1.2 Resultados Coletados
A seguir estão os resultados coletados através dos scripts da pasta `/scripts/desempenho` para Windows 11 e Zorin OS 18.1 Core.

### Windows 11

**Tabela 1: Resultados das Métricas de Eficiência e Recursos (Windows 11)**

| Característica | ID | Métrica | Critério | Resultado | Veredicto |
|---|---|---|---|---|---|
| Eficiência | ED-1.1 | TTFT (512 tok) | ≤ 5 s | 2,78 s | Aprovado |
| Eficiência | ED-1.2 | TPS (512 tok) | ≤ 5 tokens | 53,2 t | Aprovado |
| Eficiência | ED-1.3 | Load time (512 tok) | ≤ 30 s | 2,31 s | Aprovado |
| Eficiência | ED-2.1 | Consumo de RAM | ≤ 6 GB | 336,16 MB | Aprovado |
| Eficiência | ED-2.2 | Uso de CPU | ≤ 90 % | 0,23 % | Aprovado |
| Eficiência | ED-2.3 | Eficiência de recurso | ≥ 0,5 | 704,54 | Aprovado |

<p align="center"><b>Autores:</b> <a href="https://github.com/GDveAlves">Gabriel Alves</a> e <a href="https://github.com/Matheus-06">Matheus Pinheiro</a>, 2026.</p>

#### Capacidade e escalonamento (Windows 11)

**Tabela 2: Resultados de Capacidade e Escalonamento de Contexto (Windows 11)**

| Característica | ID | Métrica | Critério | Resultado | Veredicto |
|---|---|---|---|---|---|
| Eficiência | ED-3.1 | Escalonamento de contexto 512 t | ≤ 4,0 | 1,015 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 1024 t | ≤ 4,0 | 1,01 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 2048 t | ≤ 4,0 | 1,051 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 4096 t | ≤ 4,0 | 1,058 | Aprovado |
| Eficiência | ED-3.2 | Crescimento KV Cache 512 t | ≤ 1 MB/t | -0,0172 | Aprovado |
| Eficiência | ED-3.2 | Crescimento KV Cache 1024 t | ≤ 1 MB/t | -0,0062 | Aprovado |
| Eficiência | ED-3.2 | Crescimento KV Cache 2048 t | ≤ 1 MB/t | -0,0031 | Aprovado |
| Eficiência | ED-3.2 | Crescimento KV Cache 4096 t | ≤ 1 MB/t | -0,0021 | Aprovado |

<p align="center"><b>Autores:</b> <a href="https://github.com/GDveAlves">Gabriel Alves</a> e <a href="https://github.com/Matheus-06">Matheus Pinheiro</a>, 2026.</p>

### Zorin OS 18.1 Core

**Tabela 3: Resultados das Métricas de Eficiência e Recursos (Zorin OS)**

| Característica | ID | Métrica | Critério | Resultado | Veredicto |
|---|---|---|---|---|---|
| Eficiência | ED-1.1 | TTFT (512 tok) | ≤ 5 s | 2,37 s | Aprovado |
| Eficiência | ED-1.2 | TPS (512 tok) | ≤ 5 tokens | 53,43 t | Aprovado |
| Eficiência | ED-1.3 | Load time (512 tok) | ≤ 30 s | 1,82 s | Aprovado |
| Eficiência | ED-2.1 | Consumo de RAM | ≤ 6 GB | 57,02 MB | Aprovado |
| Eficiência | ED-2.2 | Uso de CPU | ≤ 90 % | 0,18 % | Aprovado |
| Eficiência | ED-2.3 | Eficiência de recurso | ≥ 0,5 | 5421,42 | Aprovado |

<p align="center"><b>Autores:</b> <a href="https://github.com/GDveAlves">Gabriel Alves</a> e <a href="https://github.com/Matheus-06">Matheus Pinheiro</a>, 2026.</p>

#### Capacidade e escalonamento (Zorin OS 18.1 Core)

**Tabela 4: Resultados de Capacidade e Escalonamento de Contexto (Zorin OS)**

| Característica | ID | Métrica | Critério | Resultado | Veredicto |
|---|---|---|---|---|---|
| Eficiência | ED-3.1 | Escalonamento de contexto 512 t | ≤ 4,0 | 0,993 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 1024 t | ≤ 4,0 | 1,029 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 2048 t | ≤ 4,0 | 1,089 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 4096 t | ≤ 4,0 | 1,118 | Aprovado |
| Eficiência | ED-3.2 | Crescimento KV Cache 512 t | ≤ 1 MB/t | 0,0002 | Aprovado |
| Eficiência | ED-3.2 | Crescimento KV Cache 1024 t | ≤ 1 MB/t | 0,0001 | Aprovado |
| Eficiência | ED-3.2 | Crescimento KV Cache 2048 t | ≤ 1 MB/t | 0,0004 | Aprovado |
| Eficiência | ED-3.2 | Crescimento KV Cache 4096 t | ≤ 1 MB/t | 0,0003 | Aprovado |

<p align="center"><b>Autores:</b> <a href="https://github.com/GDveAlves">Gabriel Alves</a> e <a href="https://github.com/Matheus-06">Matheus Pinheiro</a>, 2026.</p>

## 5.1.3 Análise por Questão GQM

Os resultados de TTFT, TPS e Load Time mostram que o modelo atende aos critérios de tempo definidos na Fase 3 em ambos os ambientes. O consumo de recursos também se manteve bem abaixo dos limites previstos para RAM e CPU, especialmente em Linux.

Os testes de capacidade ED-3.1 foram aprovados em todos os tamanhos de contexto analisados, indicando escalonamento aceitável para os limites definidos. Assim como os dados de ED-3.2 que mostraram que o crescimento do contexto (de 256 a 4096) não interfere significativamente no consumo de memória RAM por token.

## 5.1.4 Análise Comparativa entre Ambientes

Comparando os sistemas operacionais observa-se que o Zorin teve:

- Redução de 14,84% no TTFT
- Aumento de 0,43% no TPS
- Redução de 20,97% na latência de carregamento do modelo
- Redução de 83,04% no consumo de RAM
- Redução de 21,74% no consumo de CPU
- Aumento de 669,50% no REI
- Redução de 24,65%


- Apesar do desempenho do Zorin apresentar melhora considerável quando comparado ao Windows11, ambos ainda passam em todas as métricas de desempenho.

## 5.1.5 Interpretação e Discussão

O Qwen 2.5 3B via Ollama se mostrou viável em 16 GB sem GPU em ambos os sistemas. Os resultados indicam que a solução é operável com latência de resposta adequada e consumo de recursos controlado.

A diferença entre sistemas operacionais é perceptível, com Linux entregando menor latência e consumo de recursos, mas ambos os ambientes atingiram aprovação em todas as métricas principais de ED-1, ED-2 e ED-3.

## [Tabelas de dados (CSV)](https://docs.google.com/spreadsheets/d/1u2LjemT9oylyIi0hCg5z5eIDNr50ojhL29X8rfrarIM/edit?usp=sharing)

## Histórico de Versão
 
| Versão | Data | Descrição | Autor | Revisor |
|---|---|---|---|---|
| 1.0 | 12/06/2026 | Criação do documento |[Gabriel](https://github.com/GDevAlves) | [Renata Quadros](https://github.com/RenataKurzawa) | 
| 1.1 | 13/06/2026 | Adição de dados de desempenho |[Matheus Pinheiro](https://github.com/matheus-06) | [Renata Quadros](https://github.com/RenataKurzawa) | 
| 1.2 | 23/06/2026 | Ajuste do critério do CSF, inversão do sinal do REI e padronização visual das tabelas | [Renata Quadros](https://github.com/RenataKurzawa) | [Giovana Barbosa](https://github.com/gio221) |