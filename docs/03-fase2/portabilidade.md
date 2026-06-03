# 3.2 Portabilidade

# Introdução

Este artefato aplica o método GQM (Goal-Question-Metric) para analisar o Ollama em conjunto com a LLM Qwen 2.5 3B sob o critério de Portabilidade, conforme definido na norma ISO/IEC 25010. A proposta é definir metas, perguntas e métricas que permitam examinar a capacidade do sistema de ser instalado, executado e adaptado em diferentes ambientes operacionais, identificando limitações e oportunidades de melhoria.

O Ollama é uma ferramenta de código aberto projetada para facilitar a execução local de modelos de linguagem de grande porte (LLMs). Quando combinado com o Qwen 2.5 3B — modelo compacto da família Qwen 2.5, com 3 bilhões de parâmetros — o sistema representa um caso de uso relevante para avaliação de portabilidade em ambientes de recursos limitados.

Este documento integra a Fase 2 do projeto de avaliação de qualidade, fornecendo a base para coleta e análise de dados que apoiarão a tomada de decisões voltadas à qualidade e à manutenção do sistema.

# Metodologia

A metodologia adotada neste artefato baseia-se no método GQM (Goal-Question-Metric), que orienta a avaliação da qualidade de software de forma estruturada e orientada a objetivos. O processo segue três etapas:

1. Definição do objetivo de análise: neste caso, avaliar a portabilidade do Ollama executando o modelo Qwen 2.5 3B.

2. Formulação de questões: que permitem investigar aspectos específicos do critério, como comportamento em diferentes sistemas operacionais, facilidade de instalação e substituibilidade de dependências.

3. Estabelecimento de métricas: que quantifiquem os resultados observados, possibilitando avaliação objetiva e comparável.

A portabilidade, segundo a ISO/IEC 25010, é composta pelas subcaracterísticas **Adaptabilidade**, **Instalabilidade** e **Substituibilidade**, todas contempladas pelas questões e métricas definidas neste documento.

# Descrição do Objetivo de Medição de Portabilidade

A tabela a seguir apresenta o objetivo de medição estruturado segundo o paradigma GQM:

Tabela 1: Objetivo de Medição de Qualidade – Portabilidade

| Dimensão           | Descrição                                          |
|--------------------|----------------------------------------------------|
| Analisar           | Ollama com LLM Qwen 2.5 3B                         |
| Para o propósito de| Entender                                           |
| Com respeito a     | Portabilidade                                      |
| Da perspectiva do  | Pesquisador / Desenvolvedor de Software            |
| No contexto de     | Disciplina de Qualidade de Software – UnB/FCTE     |


<p align="center"><b>Autor:</b> <a href="https://github.com/Luizaxx"> Luiza Pugas </a>, 2026.</p>  

# Questões e Métricas

### Q1. Quanto à Adaptabilidade, o Ollama com Qwen 2.5 3B se comporta de formas diferentes em diferentes sistemas operacionais?

### Hipótese

O Ollama foi projetado com suporte explícito a múltiplas plataformas (Linux, macOS e Windows). A hipótese é que o sistema se comporte de forma funcionalmente equivalente em qualquer sistema operacional, com diferenças limitadas a variações de desempenho decorrentes das arquiteturas de hardware subjacentes.

### Métrica 1.1: Taxa de Execuções Sem Falha entre Plataformas

> Fórmula:

> Taxa = 1 - (Execuções com falha / Total de execuções)

>Calculada individualmente para cada sistema > >  operacional testado (Linux, macOS, Windows).

***Referência:***

[[2]](#ref-2)

> Interpretação:

> Alta adaptabilidade (Hipótese Confirmada): ≥ 99,0% de execuções bem-sucedidas em todas as plataformas.

> Baixa adaptabilidade (Hipótese Refutada): < 99,0% de execuções bem-sucedidas em alguma plataforma.

> Esta métrica avalia a estabilidade funcional do sistema entre plataformas. Falhas funcionais indicam lacunas na portabilidade de execução.

### Métrica 1.2: Desvio de Desempenho de Inferência entre Plataformas

> Fórmula:

> Desvio = |Tempo médio inferência em A - Tempo médio inferência em B| / Tempo médio geral

> Medido para inferência com prompt padronizado (100 tokens de entrada, 200 tokens de saída esperados).

***Referência:***

 [[3]](#ref-3), [[4]](#ref-4)

>Interpretação:

> Desvio aceitável (Hipótese Confirmada): ≤ 20% de variação entre plataformas de mesma arquitetura.

> Desvio elevado (Hipótese Refutada): > 20% de variação, sugerindo dependências de otimização específicas da plataforma.

> Diferenças entre CPU-only e GPU-acelerado são esperadas e devem ser documentadas separadamente.

### Métrica 1.3: Paridade de Saída do Modelo entre Plataformas

> Fórmula:

> Para um mesmo prompt e temperatura = 0 (modo determinístico):
> Paridade = 1 se as saídas são semanticamente equivalentes entre plataformas; 0 caso contrário.

***Referência:***

 [[4]](#ref-4), [[5]](#ref-5)

> **Interpretação:**

> Paridade total (Hipótese Confirmada): saídas semanticamente equivalentes em todas as plataformas.

> Divergência detectada (Hipótese Refutada): saídas com divergências factuais ou estruturais relevantes entre plataformas.

> Esta métrica garante que a portabilidade não afete a qualidade das respostas do modelo.

### Q2. Quanto à Instalabilidade, é possível instalar e desinstalar o Ollama com o modelo Qwen 2.5 3B de forma independente e sem resíduos?

### Hipótese

O Ollama oferece instaladores nativos para cada plataforma suportada. A hipótese é que a instalação e desinstalação completas (incluindo o modelo Qwen 2.5 3B) sejam possíveis sem necessidade de intervenção manual avançada, e que a desinstalação não deixe resíduos no sistema.

### Métrica 2.1: Taxa de Sucesso na Instalação (Installation Success Rate)

> Fórmula:

> Taxa = Instalações bem-sucedidas / Total de tentativas de instalação

> Considerando instalação do Ollama + download e vinculação do modelo Qwen 2.5 3B via `ollama pull qwen2.5:3b`.

***Referência:***

[[6]](#ref-6), [[7]](#ref-7)

>Interpretação:

>Alta taxa de sucesso (Hipótese Confirmada): ≥ 95% das tentativas bem-sucedidas por plataforma.

>Baixa taxa de sucesso (Hipótese Refutada): < 95% em alguma plataforma testada.

>Erros de instalação mais comuns esperados: dependências ausentes de drivers de GPU e bloqueios de antivírus no Windows.

### Métrica 2.2: Taxa de Sucesso na Desinstalação (Uninstallation Success Rate)

> Fórmula:

> Taxa = Desinstalações bem-sucedidas / Total de tentativas de desinstalação

> Verificação: ausência de processos residuais, arquivos em diretórios de dados e chaves de registro (Windows) após desinstalação.

***Referência:***

[[6]](#ref-6), [[7]](#ref-7), [[8]](#ref-8)


> Interpretação:
>
> Alta taxa de sucesso (Hipótese Confirmada): ≥ 90% das tentativas resultam em remoção completa do sistema.
>
> Baixa taxa de sucesso (Hipótese Refutada): < 90% ou presença de resíduos detectados após desinstalação.
>
> A remoção do modelo (ollama rm qwen2.5:3b) deve ser verificada separadamente da remoção do runtime.

### Q3. Quanto à Instalabilidade, o processo de instalação do Ollama com Qwen 2.5 3B apresenta erros ou inconsistências em diferentes ambientes?

### Hipótese

A hipótese é que o processo de instalação seja consistente entre ambientes distintos (distribuições Linux, versões de macOS, versões de Windows, arquiteturas x86_64 e arm64), apresentando apenas variações de tempo de download sem falhas específicas por ambiente.

### Métrica 3.1: Taxa de Sucesso de Instalação por Ambiente

>Fórmula:
>   
>Taxa(ambiente X) = Instalações bem-sucedidas em X / Total de tentativas em X
>
>Ambientes: Ubuntu 22.04, Ubuntu 24.04, macOS 13 (Intel), macOS 14 (Apple Silicon), Windows 11.

***Referência:***
[[6]](#ref-6), [[7]](#ref-7)

>Interpretação:

>Hipótese Confirmada: ≥ 95% de sucesso em cada ambiente testado individualmente.

> Hipótese Refutada: < 95% em algum ambiente específico.

> Ambientes com GPU (CUDA/Metal/ROCm) devem ser testados como subconjuntos separados.

### Métrica 3.2: Desvio Relativo de Sucesso entre Ambientes

> Fórmula:
>
> Desvio = |Taxa(X) - Taxa(Y)| / Taxa_média_entre_ambientes
>
>Alternativamente: desvio padrão relativo calculado sobre todas as taxas por ambiente.

***Referência:***

[[3]](#ref-3), [[4]](#ref-4)

> Interpretação:
>
> Consistência alta (Hipótese Confirmada): Desvio Relativo ≤ 5% entre quaisquer dois ambientes.
>
>Inconsistência significativa (Hipótese Refutada): Desvio > 5% indicando dependência de ambiente específico.
>
>Diferenças na disponibilidade de drivers de GPU são esperadas e devem ser documentadas como variáveis controladas.
>
### Métrica 3.3: Tempo de Instalação e Tipos de Falha por Ambiente

>Fórmula:
>
>   Variação de tempo = |Tempo médio em A - Tempo médio em B| / Tempo médio geral
Taxa de falhas específicas = Ocorrências de erro tipo T em ambiente X / Total de tentativas em X

***Referência:***

[[3]](#ref-3), [[8]](#ref-8)

> Interpretação:

> Hipótese Confirmada: variação de tempo ≤ 15% (excluindo diferença de velocidade de internet para download do modelo) e nenhuma falha específica por ambiente com taxa > 2%.
>
>Hipótese Refutada: variação de tempo > 15% ou presença de erros específicos de ambiente com taxa > 2%.

>Categorias de erro a monitorar: dependência ausente, permissão negada, incompatibilidade de arquitetura, timeout de download.

### Q4. Quanto à Substituibilidade, é possível substituir o Qwen 2.5 3B por outro modelo de LLM no Ollama sem impacto nos fluxos de uso?

### Hipótese

A arquitetura do Ollama é agnóstica ao modelo, utilizando uma API REST padronizada para inferência. A hipótese é que a substituição do Qwen 2.5 3B por outro modelo compatível (ex.: Mistral, Llama 3.2) exija apenas a troca do identificador de modelo nas chamadas de API, sem modificações na integração ou nos scripts de uso.

### Métrica 4.1: Taxa de Compatibilidade da API com Modelos Alternativos

> Fórmula:
>
>Taxa = Modelos alternativos testados com API 100% compatível / Total de modelos testados
>
> Modelos de referência: Qwen 2.5 3B (baseline), Llama 3.2 3B, Mistral 7B, Phi-3 Mini.

***Referência:***

[[3]](#ref-3), [[8]](#ref-8)


> Interpretação:
>
> Alta compatibilidade (Hipótese Confirmada): ≥ 90% dos modelos testados são compatíveis sem modificação na integração.

> Baixa compatibilidade (Hipótese Refutada): < 90%, indicando dependência de comportamentos específicos do Qwen 2.5 3B.

> Avaliar especialmente campos de resposta, tratamento de tokens especiais e parâmetros de geração.

### Métrica 4.2: Esforço de Substituição de Modelo

> Fórmula:
>
> Linhas modificadas = Número de linhas alteradas no código de integração para trocar o modelo
Tempo de adaptação = Tempo médio (minutos) para substituir o modelo em um projeto de referência

***Referência:***

[[1]](#ref-1), [[8]](#ref-8)

>Interpretação:
>
>Baixo esforço (Hipótese Confirmada): ≤ 3 linhas modificadas e ≤ 15 minutos de adaptação por projeto.
>
>Alto esforço (Hipótese Refutada): > 3 linhas ou > 15 minutos, indicando acoplamento excessivo ao modelo específico.
>
>Inclui o tempo de download do modelo alternativo via `ollama pull`.

### Métrica 4.3: Taxa de Sucesso em Testes após Substituição de Modelo

> Fórmula:

> Taxa = Testes bem-sucedidos após substituição / Total de testes existentes

Usando suite de testes definida para o fluxo principal de inferência com Qwen 2.5 3B como baseline.

***Referência:***
[[8]](#ref-8)
    
> Interpretação:
>
>Alta confiabilidade (Hipótese Confirmada): ≥ 90% dos testes passam com o modelo alternativo.
>
>Baixa confiabilidade (Hipótese Refutada): < 90%, indicando dependência comportamental do Qwen 2.5 3B.
>
>Falhas esperadas por diferença de capacidade do modelo devem ser classificadas separadamente de falhas de integração.

# Conclusões

Com a aplicação do método GQM, foi possível estruturar de forma clara e mensurável a análise de portabilidade do Ollama em conjunto com a LLM Qwen 2.5 3B. As quatro questões formuladas cobrem as três subcaracterísticas de portabilidade previstas na ISO/IEC 25010: Adaptabilidade (Q1), Instalabilidade (Q2 e Q3) e Substituibilidade (Q4).

As métricas definidas permitem avaliar objetivamente: como o sistema se comporta funcionalmente e em termos de desempenho em diferentes sistemas operacionais; a confiabilidade e consistência do processo de instalação e desinstalação; e a facilidade de substituição do modelo Qwen 2.5 3B por alternativas compatíveis dentro da mesma infraestrutura Ollama.

Esta análise, ao estabelecer hipóteses verificáveis e critérios de aceitação quantitativos, fornece a base metodológica necessária para a Fase 3 (coleta de dados) e a Fase 4 (análise e conclusões finais) do projeto de avaliação de qualidade de software.

OBS: Modelos de Linguagem de Grande Escala (LLMs) foram utilizados como apoio ao brainstorm de perguntas e métricas, bem como para auxílio na estruturação e escrita do documento em formato acadêmico.

# Sobre o Uso de IA

Para a elaboração deste documento, a Inteligência Artificial foi utilizada como ferramenta de apoio. O uso concentrou-se principalmente em auxiliar a compreensão e o esclarecimento de termos técnicos presentes na norma ISO/IEC 25010 e em fontes corporativas e acadêmicas consultadas. Adicionalmente, a IA foi empregada para estruturar e organizar as ideias na aplicação da metodologia GQM, garantindo coerência entre as questões, métricas e o objetivo de análise.

[Notebook LM](https://notebooklm.google.com/notebook/e9f64a2d-93cc-4f05-9c28-4d5f14c3af3e)

# Referências Bibliográficas

<a id="ref-1"></a>[1] FENTON, Norman; BIEMAN, James. Software Metrics: A Rigorous and Practical Approach. 3. ed. Boca Raton: CRC Press, 2015.

<a id="ref-2"></a>[2]  GOOGLE. Firebase Crashlytics: Métricas de crash-free. Disponível em: https://firebase.google.com/docs/crashlytics/crash-free-metrics?hl=pt-br
. Acesso em: 03 jun. 2026.

<a id="ref-3"></a>[3] HEADSPIN. Gain Insight Into Cross-Platform Performance Metrics. HeadSpin Blog, 2023. Disponível em: https://www.headspin.io/blog/gain-insight-into-cross-platform-performance-metrics
. Acesso em:  03 jun. 2026

<a id="ref-4"></a>[4] B. BUMGARDNER. Benchmarking: When can I stop making measurements? Stack Overflow, 2009. Disponível em: https://stackoverflow.com/questions/1390047/benchmarking-when-can-i-stop-making-measurements
. Acesso em:  03 jun. 2026

<a id="ref-5"></a>[5] LINKEDIN ENGINEERING. How We Identify and Stop Slow Latency Leaks at LinkedIn. 2017. Disponível em: https://www.linkedin.com/blog/engineering/optimization/fixing-the-plumbing-how-we-identify-and-stop-slow-latency-leaks
. Acesso em:  03 jun. 2026

<a id="ref-6"></a>[6] ADJUST. How to track app uninstalls: Everything you need to know. Disponível em: https://www.adjust.com/blog/how-to-track-app-installs-and-uninstalls/
. Acesso em:  03 jun. 2026

<a id="ref-7"></a>[7] INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. ISO/IEC 25036:2011 – Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Quality in use measures. Geneva: ISO, 2011.

<a id="ref-8"></a>[8] REPLICATED. Instance Insights: Install Success Rate. 2023. Disponível em: https://replicated.com/blog/instance-insights-install-success-rate
. Acesso em:  03 jun. 2026.

## Histórico de Versão
 
| Versão | Data | Descrição | Autor | Revisor |
|---|---|---|---|---|
| 1.0 | 03/06/2026 | Adição de conteúdo | [Luiza](https://github.com/Luizaxx) | [Gabriel Alves](https://github.com/GdevAlves) |