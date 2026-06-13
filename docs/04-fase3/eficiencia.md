# Plano de Avaliação — Eficiência de Desempenho

## 1. Introdução

Este documento especifica como serão implementadas e executadas as métricas definidas na metodologia GQM da Fase 2 para avaliar a **Eficiência de Desempenho** do Ollama.

O foco está em três subcaracterísticas conforme ISO/IEC 25010:

- **Comportamento Temporal** (Time Behaviour)
- **Utilização de Recursos** (Resource Utilization)
- **Capacidade** (Capacity)

---

## 2. Métricas a Serem Implementadas

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


---

## 3. Ambiente de Teste

### 3.1 Hardware

| Componente | Especificação |
|------------|---------------|
| Processador | Intel Core i5 (8 núcleos) |
| Memória RAM | 16 GB DDR5 |
| Armazenamento | SSD 512 GB |
| GPU | Nenhuma (CPU-only) |

### 3.2 Sistemas Operacionais

| Ambiente | Sistema Operacional |
|----------|---------------------|
| Ambiente A | Windows 11 (64 bits) |
| Ambiente B | Zorin OS 18.1 Core |

### 3.3 Software

| Ferramenta | Versão | Finalidade |
|------------|--------|------------|
| Ollama | v0.9.0 | Motor de inferência local |
| Qwen 2.5 3B | — | Modelo de linguagem avaliado |
| Python | 3.10+ | Scripts de automação e medição |
| psutil (Python) | 5.9+ | Monitoramento de recursos |

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

| Carga    | Tamanho Aproximado |
|----------|--------------------|
| Leve     | 512  tokens  |
| Moderada | 1024 tokens        |
| Alta     |  2048 tokens        |
| Extrema  | 4096 tokens        |

## 5. Procedimento de Coleta
Passo 1: Preparação

1. Instalar o Ollama conforme documentação oficial
2. Baixar o modelo Qwen 2.5 3B: ollama pull qwen2.5:3b
3. Verificar disponibilidade da API
4. Preparar prompts de teste em arquivo prompts.json
5. Configurar scripts de medição

Passo 2: Execução dos Testes
Para cada ambiente (Windows e Linux):

1. Reiniciar o sistema operacional
2. Iniciar o Ollama: ollama serve
3. Aguardar 60 segundos para estabilização
4. Executar script de medição de TTFT com 10 repetições para cada tamanho de contexto
5. Registrar resultados em arquivo CSV


Passo 3: Registro
Após cada sessão de testes:

1. Consolidar arquivos CSV
2. Calcular médias e desvios-padrão
3. Documentar observações sobre estabilidade do sistema

## 6. Critérios de Aceitação

| Métrica            | Critério de Aceitação                  |
|--------------------|-----------------------------------------|
| TTFT (512 tokens)  | ≤ 5 segundos                            |
| TTFT (2048 tokens) | ≤ 15 segundos                           |
| Uso de RAM         | ≤ 12 GB (75% dos 16 GB disponíveis)       |
| Estabilidade       | Sistema responsivo durante 100% dos testes |

## 7. Localização dos Dados

| Artefato            | Caminho                         | Descrição                     |
|---------------------|---------------------------------|-------------------------------|
| Scripts de medição  | `/tests/scripts/`              | Scripts Python        |
| Resultados brutos   | `/tests/resultados/eficiencia/` | Arquivos CSV                  |
| Logs de execução    | `/tests/logs/`                 | Saída do terminal e erros     |

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