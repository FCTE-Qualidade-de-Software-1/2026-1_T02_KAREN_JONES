# Plano de Avaliação — Eficiência de Desempenho

## 1. Introdução

Este documento especifica como serão implementadas e executadas as métricas definidas na metodologia GQM da Fase 2 para avaliar a **Eficiência de Desempenho** do Ollama.

O foco está em três subcaracterísticas conforme ISO/IEC 25010:

- **Comportamento Temporal** (Time Behaviour)
- **Utilização de Recursos** (Resource Utilization)
- **Capacidade** (Capacity)

### 1.1 Nota de Escopo: Sobre Métricas de Carga Concorrente (Q4 / M4)

Embora a subcaracterística de "Capacidade" (ISO/IEC 25010) tenha sido [citada textualmente na Fase 2](../03-fase2/eficiencia.md#conclusoes), esclarece-se que a **Q4 (Capacidade sob carga concorrente)** e as métricas de estresse multiusuário frequentemente associadas (como *M4.1 (Throughput Concorrente)*, *M4.2 (Degradação de Latência)* e *M4.3 (Taxa de Erros)* ) **não foram integradas à metodologia GQM deste trabalho**.

**Justificativa:** O mapeamento da Persona deste projeto estabeleceu um cenário de uso estritamente focado em um **usuário único operando em ambiente local e offline**. Como o ecossistema do Ollama é executado localmente para responder a demandas individuais, testes de acessos simultâneos ou taxas de erro por concorrência de rede divergiriam do contexto prático da aplicação. Portanto, a avaliação de Capacidade concentrou-se exclusivamente no comportamento do sistema sob o escalonamento do tamanho do contexto de prompts ([ED-3.1 e ED-3.2](../04-fase3/eficiencia.md#2-metricas-a-serem-implementadas)).

---

## 2. Métricas a Serem Implementadas

Para garantir a rastreabilidade e a consistência em relação ao modelo conceitual, a tabela a seguir mapeia os identificadores originais definidos na Fase 2 (metodologia GQM) para os novos códigos operacionais utilizados nesta Fase 3 e na Fase 4 (atendendo ao critério F3-C8).

### Tabela de Rastreabilidade de Métricas (Fase 2 e Fase 3)

**Tabela 1: Rastreabilidade e Mapeamento de Identificadores**

| ID GQM (Fase 2) | ID Operacional (Fase 3/4) | Nome da Métrica | Motivo da Codificação |
|:---:|:---:|---|---|
| [M1.1](../03-fase2/eficiencia.md#m11) | [ED-1.1](#6-criterios-de-aceitacao) | Time to First Token (TTFT) | Prefixo **ED** mapeia a característica de **E**ficiência de **D**esempenho. |
| [M1.2](../03-fase2/eficiencia.md#m12) | [ED-1.2](#6-criterios-de-aceitacao) | Tokens por Segundo (TPS) | Prefixo **ED** mapeia a característica de **E**ficiência de **D**esempenho. |
| [M1.3](../03-fase2/eficiencia.md#m13) | [ED-1.3](#6-criterios-de-aceitacao) | Latência de Carregamento do Modelo (MLT) | Prefixo **ED** mapeia a característica de **E**ficiência de **D**esempenho. |
| [M2.1](../03-fase2/eficiencia.md#metrica-21-consumo-de-memoria-ram-durante-inferencia) | [ED-2.1](#6-criterios-de-aceitacao) | Consumo de RAM | Prefixo **ED** mapeia a característica de **E**ficiência de **D**esempenho. |
| [M2.2](../03-fase2/eficiencia.md#metrica-22-utilizacao-de-cpu-durante-inferencia) | [ED-2.2](#6-criterios-de-aceitacao) | Uso Médio de CPU | Prefixo **ED** mapeia a característica de **E**ficiência de **D**esempenho. |
| [M2.3](../03-fase2/eficiencia.md#metrica-23-indice-de-eficiencia-de-recursos-rei) | [ED-2.3](#6-criterios-de-aceitacao) | Índice de Eficiência de Recursos (REI) | Prefixo **ED** mapeia a característica de **E**ficiência de **D**esempenho. |
| [M3.1](../03-fase2/eficiencia.md#metrica-31-fator-de-escalonamento-de-contexto-csf) | [ED-3.1](#6-criterios-de-aceitacao) | Fator de Escalonamento de Contexto (CSF) | Prefixo **ED** mapeia a característica de **E**ficiência de **D**esempenho. |
| [M3.2](../03-fase2/eficiencia.md#metrica-32-taxa-de-crescimento-do-kv-cache-kvcgr) | [ED-3.2](#6-criterios-de-aceitacao) | Taxa de Crescimento do KV Cache (KVCGR) | Prefixo **ED** mapeia a característica de **E**ficiência de **D**esempenho. |
| — | — | Estabilidade do Sistema | Métrica complementar adicionada na Fase 3. |

<p align="center"><b>Autoras:</b> <a href="https://github.com/RenataKurzawa">Renata Quadros</a> e <a href="https://github.com/gio221">Giovana Barbosa</a>, 2026.</p>

---

**Tabela 2: Métricas a Serem Implementadas**

| ID | Métrica | Subcaracterística | Descrição |
|----|---------|-------------------|-----------|
| ED-1.1 | Time to First Token (TTFT) | Comportamento Temporal | Tempo entre o envio do prompt e a chegada do primeiro token de resposta |
| ED-1.2 | Tokens por Segundo (TPS) | Comportamento Temporal | Taxa de geração de tokens após o primeiro token |
| ED-1.3 | Latência de Carregamento do Modelo (MLT) | Comportamento Temporal | Diferença entre tempo de carregamento do modelo e tempo de início da inferência |
| ED-2.1 | Consumo de RAM | Utilização de Recursos | Máximo de memória RAM consumida durante a execução |
| ED-2.2 | Uso Médio de CPU | Utilização de Recursos | Percentual de utilização da CPU durante a execução |
| ED-2.3 | Índice de Eficiência de Recursos (REI) | Utilização de Recursos | Relação entre a taxa de geração de tokens e o consumo de recursos (CPU * RAM) |
| ED-3.1 | Fator de Escalonamento de Contexto (CSF) | Capacidade | TTFT com diferentes tamanhos de contexto (512, 1024, 2048, 4096 tokens) comparado com 256 tokens |
| ED-3.2 | Taxa de Crescimento do KV Cache (KVCGR) | Capacidade | Aumento da memória utilizada pelo cache de chaves e valores conforme o tamanho do contexto |

<p align="center"><b>Autoras:</b> <a href="https://github.com/RenataKurzawa">Renata Quadros</a> e <a href="https://github.com/gio221">Giovana Barbosa</a>, 2026.</p>

**Nota de Escopo:** A métrica de **Estabilidade do Sistema** (avaliada nos Critérios de Aceitação) foi adicionada nesta etapa com o objetivo de verificar a responsividade do Sistema Operacional sob estresse de inferência longa, complementando as métricas originalmente derivadas do método GQM na Fase 2.

---

## 3. Ambiente de Teste

### 3.1 Hardware

**Tabela 3: Especificações de Hardware da Infraestrutura de Testes**

| Componente | Especificação |
|------------|---------------|
| Processador | Intel Core i5 (8 núcleos) |
| Memória RAM | 16 GB DDR5 |
| Armazenamento | SSD 512 GB |
| GPU | Nenhuma (CPU-only) |

<p align="center"><b>Autoras:</b> <a href="https://github.com/RenataKurzawa">Renata Quadros</a> e <a href="https://github.com/gio221">Giovana Barbosa</a>, 2026.</p>

### 3.2 Sistemas Operacionais

**Tabela 4: Sistemas Operacionais Configurados para os Ambientes A e B**

| Ambiente | Sistema Operacional |
|----------|---------------------|
| Ambiente A | Windows 11 (64 bits) |
| Ambiente B | Zorin OS 18.1 Core |

<p align="center"><b>Autoras:</b> <a href="https://github.com/RenataKurzawa">Renata Quadros</a> e <a href="https://github.com/gio221">Giovana Barbosa</a>, 2026.</p>

### 3.3 Software

**Tabela 5: Ecossistema de Software e Versões Utilizadas**

| Ferramenta | Versão | Finalidade |
|------------|--------|------------|
| Ollama | v0.9.0 | Motor de inferência local |
| Qwen 2.5 3B | — | Modelo de linguagem avaliado |
| Python | 3.10+ | Scripts de automação e medição |
| psutil (Python) | 5.9+ | Monitoramento de recursos |

<p align="center"><b>Autoras:</b> <a href="https://github.com/RenataKurzawa">Renata Quadros</a> e <a href="https://github.com/gio221">Giovana Barbosa</a>, 2026.</p>

---

## 4. Instrumentos de Medição

### 4.1 Medição de TTFT e TPS

**Método**: Script Python que envia prompts via API REST do Ollama e registra as marcas de tempo durante a execução.

Dados Coletados:

- Marca de tempo de envio do prompt
- Marca de tempo do primeiro token recebido
- Marca de tempo de conclusão
- Contagem total de tokens gerados

### 4.2 Monitoramento de Recursos
Método: Script Python com psutil executando em paralelo à execução do modelo.

Dados Coletados:

Uso de CPU (%) a cada 500ms
Uso de RAM (MB) a cada 500ms
Pico de uso de RAM

### 4.3 Teste de Capacidade (Carga de Contexto)

Método: Variação do tamanho do prompt de entrada:

**Tabela 6: Classificação de Níveis de Carga por Volume de Contexto**

| Carga    | Tamanho Aproximado |
|----------|--------------------|
| Leve     | 512  tokens  |
| Moderada | 1024 tokens        |
| Alta     |  2048 tokens        |
| Extrema  | 4096 tokens        |

<p align="center"><b>Autoras:</b> <a href="https://github.com/RenataKurzawa">Renata Quadros</a> e <a href="https://github.com/gio221">Giovana Barbosa</a>, 2026.</p>

## 5. Procedimento de Coleta
Passo 1: Preparação

1. Instalar o Ollama conforme documentação oficial
2. Baixar o modelo Qwen 2.5 3B: ollama pull qwen2.5:3b
3. Verificar disponibilidade da API
5. Configurar scripts de medição

Passo 2: Execução dos Testes
Para cada ambiente (Windows e Linux):

1. Reiniciar o sistema operacional
2. Iniciar o Ollama: ollama serve
3. Aguardar 60 segundos para estabilização
4. Executar script de medição de TTFT com 5 repetições para cada tamanho de contexto (justifica-se que 5 ciclos são suficientes para a tendência observada)
5. Registrar resultados em arquivo CSV


Passo 3: Registro
Após cada sessão de testes:

1. Consolidar arquivos CSV
2. Calcular médias e desvios-padrão
3. Documentar observações sobre estabilidade do sistema

## 6. Critérios de Aceitação

**Tabela 7: Critérios de Aceitação**

| ID | Métrica | Critério de Aceitação |
|----|---------|-----------------------|
| [ED-1.1](../03-fase2/eficiencia.md#m11) | TTFT (512 tokens) | ≤ 5 segundos |
| [ED-1.2](../03-fase2/eficiencia.md#m12) | TPS (512 tokens) | ≤ 5 tokens |
| [ED-1.3](../03-fase2/eficiencia.md#m13) | Latência de Carregamento (Load time) | ≤ 30 segundos |
| [ED-2.1](../03-fase2/eficiencia.md#metrica-21-consumo-de-memoria-ram-durante-inferencia) | Consumo de RAM | ≤ 6 GB |
| [ED-2.2](../03-fase2/eficiencia.md#metrica-22-utilizacao-de-cpu-durante-inferencia) | Uso de CPU | ≤ 90 % |
| [ED-2.3](../03-fase2/eficiencia.md#metrica-23-indice-de-eficiencia-de-recursos-rei) | Índice de Eficiência de Recursos (REI) | ≥ 0,5 |
| [ED-3.1](../03-fase2/eficiencia.md#metrica-31-fator-de-escalonamento-de-contexto-csf) | Escalonamento de contexto (512t a 4096t) | ≤ 4,0 |
| [ED-3.2](../03-fase2/eficiencia.md#metrica-32-taxa-de-crescimento-do-kv-cache-kvcgr) | Crescimento KV Cache (512t a 4096t) | ≤ 1 MB/t |
| — | Estabilidade | Sistema responsivo durante 100% dos testes |

<p align="center"><b>Autoras:</b> <a href="https://github.com/RenataKurzawa">Renata Quadros</a> e <a href="https://github.com/gio221">Giovana Barbosa</a>, 2026.</p>

## 7. Localização dos Dados

**Tabela 8: Estrutura de Diretórios e Localização dos Artefatos de Teste**

| Artefato            | Caminho                         | Descrição                     |
|---------------------|---------------------------------|-------------------------------|
| Scripts de medição  | `/tests/scripts/`              | Scripts Python        |
| Resultados brutos   | `/tests/resultados/eficiencia/` | Arquivos CSV                  |
| Logs de execução    | `/tests/logs/`                 | Saída do terminal e erros     |

<p align="center"><b>Autoras:</b> <a href="https://github.com/RenataKurzawa">Renata Quadros</a> e <a href="https://github.com/gio221">Giovana Barbosa</a>, 2026.</p>

# Bibliografia

> 1. ISO/IEC. *ISO/IEC TR 25021:2007: Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — Quality measure elements*. 1. ed. Genebra: International Organization for Standardization / International Electrotechnical Commission, 2007.

> 2. RAMOS, Cristiane Soares. *Medição baseada em objetivos: “Determinando o que medir”*. Material da disciplina FGA0278 - Qualidade de Software 1. Faculdade do Gama (FGA), Universidade de Brasília (UnB), 2024.

> 3. QWEN. *Qwen/Qwen2.5-3B-Instruct*. Repositório de modelos Hugging Face, 2024. Disponível em: <https://ollama.com/library/qwen2.5:3b>. Acesso em: 13 maio 2026.

> 4. QWEN TEAM. *Qwen2 Technical Report*. 2024. Disponível em: <https://arxiv.org/abs/2407.10671>. Acesso em: 13 maio 2026.

> 5. OLLAMA INC. *Ollama: The easiest way to build with open models*. Portal oficial de documentação, 2026. Disponível em: <https://ollama.com>. Acesso em: 13 maio 2026.

## Histórico de Versão
 
| Versão | Data | Descrição | Autor | Revisor |
|---|---|---|---|---|
| 1.0 | 04/06/2026 | Criação do documento |[Giovana Barbosa](https://github.com/gio221) | [Renata Quadros](https://github.com/RenataKurzawa) | 
| 1.1 | 12/06/2026 | Alinhamento de métricas da fase 2 | [Gabriel Alves](https://github.com/GDveAlves) | [Matheus Pinheiro](https://github.com/Matheus-06)|
| 1.2 | 23/06/2026 | Alinhamento de fases, hiperlinks, padronização de títulos, legendas e autorias das tabelas | [Renata Quadros](https://github.com/RenataKurzawa) | [Giovana Barbosa](https://github.com/gio221) |
| 1.3 | 23/06/2026 | Ajuste no número de repetições para 5 ciclos | [Johnnatan Salles](https://github.com/jsalless) | [Equipe](https://github.com/GDveAlves) |