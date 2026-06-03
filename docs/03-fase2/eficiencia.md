# 3.1 Eficiência de Desempenho

# Introdução

Este artefato aplica o método GQM (Goal-Question-Metric) para analisar o Ollama em conjunto com a LLM Qwen 2.5 3B sob o critério de Eficiência de Desempenho, conforme definido pela norma ISO/IEC 25010:2011. A proposta é definir metas, perguntas e métricas que permitam examinar a capacidade do sistema de executar suas funções dentro de limites adequados de tempo, recursos e capacidade, considerando diferentes condições de carga e configuração de hardware.

A Eficiência de Desempenho na ISO/IEC 25010 é composta por três subcaracterísticas: **Comportamento em Relação ao Tempo (Time Behaviour)**, que avalia latência e throughput; **Utilização de Recursos (Resource Utilization)**, que mede o consumo de CPU, memória RAM e VRAM; e **Capacidade (Capacity)**, que verifica os limites operacionais do sistema sob diferentes condições de carga e tamanho de contexto.

O Ollama é uma ferramenta de código aberto projetada para facilitar a execução local de Modelos de Linguagem de Grande Escala (LLMs). O Qwen 2.5 3B — modelo compacto da família Qwen 2.5 com 3 bilhões de parâmetros — representa um caso de uso relevante para avaliação de eficiência em ambientes com recursos computacionais limitados, como laptops de desenvolvimento e servidores de baixo custo.

Este documento integra a Fase 2 do projeto de avaliação de qualidade e serve como base para a coleta e análise de dados nas fases subsequentes.

# Metodologia

A metodologia baseia-se no método GQM (Goal-Question-Metric), que orienta a avaliação da qualidade de software de forma estruturada e orientada a objetivos. O processo segue três etapas:

1. Definição do objetivo de análise: avaliar a eficiência de desempenho do Ollama executando o modelo Qwen 2.5 3B em diferentes condições de carga e configuração de hardware.

2. Formulação de questões: investigando aspectos específicos de latência de inferência, throughput, consumo de recursos computacionais e comportamento sob limites de capacidade.

3. Estabelecimento de métricas: quantificando os resultados observados com fórmulas mensuráveis, possibilitando avaliação objetiva e reproduzível.

As métricas são fundamentadas nas normas ISO/IEC 25010 (modelo de qualidade) e ISO/IEC 25021 (elementos de medida de qualidade), que fornecem definições formais para medidas de desempenho de software. A coleta de dados será realizada por meio da API REST do Ollama (`/api/generate` e `/api/ps`), combinada com ferramentas de monitoramento de sistema como `psutil`, `nvidia-smi` e utilitários nativos do sistema operacional.

# Descrição do Objetivo de Medição de Eficiência de Desempenho

Tabela 1: Objetivo de Medição de Qualidade – Eficiência de Desempenho

| Dimensão | Descrição |
|-----------|-----------|
| Analisar | Ollama com LLM Qwen 2.5 3B |
| Para o propósito de | Entender |
| Com respeito a | Eficiência de Desempenho |
| Da perspectiva do | Pesquisador / Desenvolvedor de Software |
| No contexto de | Disciplina de Qualidade de Software – UnB/FCTE |

<p align="center"><b>Autor:</b> <a href="https://github.com/Luizaxx">Luiza Pugas</a>, 2026.</p>

# Questões e Métricas

## Q1. Quanto ao Comportamento em Relação ao Tempo, a latência de inferência do Ollama com Qwen 2.5 3B é adequada para uso interativo?

### Hipótese

O Qwen 2.5 3B, por ser um modelo compacto (3 bilhões de parâmetros), deve apresentar latência de inferência compatível com uso interativo em hardware de consumo comum (CPU moderna ou GPU de entrada), com tempo de resposta percebível como aceitável pelo usuário. A hipótese é que o sistema consiga gerar os primeiros tokens em menos de 5 segundos e manter uma taxa de geração suficiente para leitura em tempo real em hardware convencional.

### Métrica 1.1: Tempo até o Primeiro Token (Time to First Token – TTFT)

> Fórmula:
>
> TTFT = t_primeiro_token − t_envio_requisição
>
> Medido via timestamps da API REST do Ollama para prompts de referência com 50 tokens de entrada.

***Referência:***

[[3]](#ref-3), [[4]](#ref-4)

> Interpretação:
>
> Aceitável para uso interativo (Hipótese Confirmada): TTFT mediana ≤ 3 segundos em CPU; ≤ 1 segundo com GPU.
>
> Latência elevada (Hipótese Refutada): TTFT mediana > 5 segundos em CPU ou > 2 segundos com GPU.

### Métrica 1.2: Taxa de Geração de Tokens (Tokens Per Second – TPS)

> Fórmula:
>
> TPS = Total de tokens gerados / Tempo total de geração
>
> TPS = eval_count / (eval_duration / 1e9)

***Referência:***

[[3]](#ref-3), [[4]](#ref-4)

> Interpretação:
>
> Legível em tempo real (Hipótese Confirmada): ≥ 10 tokens/s em CPU; ≥ 30 tokens/s com GPU.
>
> Abaixo do limiar aceitável (Hipótese Refutada): < 5 tokens/s.

### Métrica 1.3: Latência de Carregamento do Modelo (Model Load Time – MLT)

> Fórmula:
>
> MLT = t_modelo_pronto − t_início_comando

***Referência:***

[[3]](#ref-3), [[5]](#ref-5)

> Interpretação:
>
> Carregamento rápido (Hipótese Confirmada): ≤ 10 segundos em CPU; ≤ 5 segundos com GPU.
>
> Carregamento lento (Hipótese Refutada): > 30 segundos.

## Q2. Quanto à Utilização de Recursos, o consumo de memória e CPU do Ollama com Qwen 2.5 3B é proporcional ao tamanho do modelo e adequado ao hardware alvo?

### Hipótese

O Qwen 2.5 3B na quantização Q4_K_M deve ocupar aproximadamente 2 GB para os pesos do modelo, mantendo consumo total inferior a 6 GB de RAM em modo CPU-only, permitindo execução em sistemas com 8 GB de memória.

### Métrica 2.1: Consumo de Memória RAM durante Inferência

> Fórmula:
>
> RAM_inferência = RAM_pico − RAM_baseline

***Referência:***

[[6]](#ref-6), [[4]](#ref-4)

> Interpretação:
>
> Consumo adequado (Hipótese Confirmada): ≤ 4 GB.
>
> Consumo excessivo (Hipótese Refutada): > 6 GB.

### Métrica 2.2: Utilização de CPU durante Inferência

> Fórmula:
>
> CPU_uso = Média de utilização de CPU (%) durante a geração

***Referência:***

[[6]](#ref-6), [[4]](#ref-4)

> Interpretação:
>
> Uso aceitável (Hipótese Confirmada): ≤ 90%.
>
> Gargalo de CPU (Hipótese Refutada): 100% dos núcleos por mais de 80% do tempo.

### Métrica 2.3: Índice de Eficiência de Recursos (REI)

> Fórmula:
>
> REI = TPS / (RAM_utilizada_GB × CPU_média_%)

***Referência:***

[[1]](#ref-1), [[4]](#ref-4)

> Interpretação:
>
> Alta eficiência: REI ≥ 1,0.
>
> Baixa eficiência: REI < 0,5.

## Q3. Quanto ao Comportamento em Relação ao Tempo e Utilização de Recursos, como o desempenho do sistema escala com o aumento do tamanho do contexto?

### Hipótese

A complexidade quadrática do mecanismo de atenção dos Transformers deve causar crescimento não linear de latência e memória conforme aumenta o tamanho do contexto. Ainda assim, o sistema deve permanecer operacional dentro do limite de contexto suportado pelo modelo.

### Métrica 3.1: Fator de Escalonamento de Contexto (CSF)

> Fórmula:
>
> CSF = TTFT(n_tokens) / TTFT(256_tokens)

***Referência:***

[[3]](#ref-3), [[4]](#ref-4)

> Interpretação:
>
> Escalonamento aceitável: ≤ 4,0 para 4096 tokens.
>
> Degradação severa: > 8,0.

### Métrica 3.2: Taxa de Crescimento do KV Cache (KVCGR)

> Fórmula:
>
> KVCGR = (RAM_pico(n) − RAM_pico(256)) / (n − 256)

***Referência:***

[[5]](#ref-5), [[6]](#ref-6)

> Interpretação:
>
> Crescimento previsível: ≤ 0,5 MB/token.
>
> Crescimento excessivo: > 1,0 MB/token.

## Q4. Quanto à Capacidade, o Ollama com Qwen 2.5 3B consegue processar múltiplas requisições simultâneas mantendo desempenho aceitável?

### Hipótese

O Ollama processa requisições de forma predominantemente sequencial. A hipótese é que requisições concorrentes aumentem a latência de maneira previsível sem comprometer a estabilidade do sistema.

### Métrica 4.1: Throughput sob Carga Concorrente (CT)

> Fórmula:
>
> CT(n) = Total de tokens gerados / Tempo total do lote

***Referência:***

[[3]](#ref-3), [[7]](#ref-7)

> Interpretação:
>
> Comportamento esperado: CT(n) ≈ CT(1).
>
> Overhead excessivo: CT(n) < CT(1) × 0,8.

### Métrica 4.2: Degradação de Latência sob Carga (LDUL)

> Fórmula:
>
> LDUL(n) = TTFT_mediana(n) / TTFT_mediana(1)

***Referência:***

[[4]](#ref-4), [[7]](#ref-7)

> Interpretação:
>
> Degradação aceitável: ≤ 4,5 para 4 requisições simultâneas.
>
> Degradação severa: > 6,0.

### Métrica 4.3: Taxa de Erros sob Carga Máxima (ERUL)

> Fórmula:
>
> ERUL = Requisições com erro / Total de requisições

***Referência:***

[[1]](#ref-1), [[4]](#ref-4)

> Interpretação:
>
> Sistema estável: ≤ 1% de erros para até 8 requisições simultâneas.
>
> Instabilidade detectada: > 5%.

# Conclusões

Com a aplicação do método GQM, foi possível estruturar de forma mensurável e reproduzível a análise de eficiência de desempenho do Ollama em conjunto com a LLM Qwen 2.5 3B. As quatro questões formuladas cobrem as três subcaracterísticas de eficiência de desempenho previstas na ISO/IEC 25010: Comportamento em Relação ao Tempo (Q1 e Q3), Utilização de Recursos (Q2 e Q3) e Capacidade (Q4).

As métricas definidas permitem avaliar objetivamente a latência de inferência, a taxa de geração de tokens, o consumo de recursos computacionais, o impacto do aumento do contexto e o comportamento do sistema sob carga concorrente.

Esta análise fornece a base metodológica necessária para a Fase 3 (coleta de dados) e para a Fase 4 (análise dos resultados e conclusões finais) do projeto de avaliação de qualidade de software.

OBS: Modelos de Linguagem de Grande Escala (LLMs) foram utilizados como apoio ao brainstorm de perguntas e métricas, bem como para auxílio na estruturação e escrita do documento em formato acadêmico.

# Sobre o Uso de IA

Para a elaboração deste documento, a Inteligência Artificial foi utilizada como ferramenta de apoio. O uso concentrou-se principalmente em auxiliar a compreensão e o esclarecimento de termos técnicos presentes nas normas ISO/IEC 25010 e ISO/IEC 25021, bem como em fontes de documentação técnica do Ollama e da biblioteca psutil. Adicionalmente, a IA foi empregada para estruturar e organizar as ideias na aplicação da metodologia GQM, garantindo coerência entre questões, métricas e o objetivo de análise definido.

[Notebook LM](https://notebooklm.google.com/notebook/e9f64a2d-93cc-4f05-9c28-4d5f14c3af3e)

# Referências Bibliográficas

<a id="ref-1"></a>[1] INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. ISO/IEC 25010:2011 – Systems and software engineering – Software product Quality Requirements and Evaluation (SQuaRE) – Quality model. Geneva: ISO, 2011.

<a id="ref-3"></a>[3] OLLAMA. REST API Documentation. Disponível em: https://github.com/ollama/ollama/blob/main/docs/api.md.
Acesso em: 03 jun. 2026.

<a id="ref-4"></a>[4] FENTON, Norman; BIEMAN, James. Software Metrics: A Rigorous and Practical Approach. 3. ed. Boca Raton: CRC Press, 2015.
Acesso em: 03 jun. 2026.

<a id="ref-5"></a>[5] NVIDIA Corporation. GPU Memory Management Best Practices.
Acesso em: 03 jun. 2026.

<a id="ref-6"></a>[6] PSUTIL. Cross-platform lib for process and system monitoring in Python. Disponível em: https://psutil.readthedocs.io/. Acesso em: 03 jun. 2026.

<a id="ref-7"></a>[7] TSENART, T. vegeta: HTTP load testing tool. Disponível em: https://github.com/tsenart/vegeta.
Acesso em: 03 jun. 2026.

<a id="ref-8"></a>[8] ALIBABA CLOUD. Qwen 2.5 Technical Report. Disponível em: https://huggingface.co/Qwen/Qwen2.5-3B-Instruct.
Acesso em: 03 jun. 2026.

## Histórico de Versão

| Versão | Data | Descrição | Autor | Revisor |
|---------|---------|---------|---------|---------|
| 1.0 | 03/06/2026 | Adição de conteúdo | [Luiza](https://github.com/Luizaxx) | [Gabriel Alves](https://github.com/GdevAlves) |
