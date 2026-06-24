# 5.2 Portabilidade

## 5.2.1 Introdução

Este documento apresenta os resultados da Fase 4 do processo de avaliação de qualidade do Ollama em conjunto com o modelo de linguagem Qwen 2.5 3B, no que diz respeito à característica de **Portabilidade**, conforme definida pela norma ISO/IEC 25010. A avaliação segue o método GQM (*Goal-Question-Metric*) estabelecido na Fase 2 e o plano de coleta especificado na Fase 3.

O objetivo de medição estruturado na Fase 2 pode ser retomado da seguinte forma:

> **Analisar** o Ollama com LLM Qwen 2.5 3B, **com o propósito de** entender sua **portabilidade**, **da perspectiva do** pesquisador e desenvolvedor de software, **no contexto da** disciplina de Qualidade de Software da UnB/FCTE.

As subcaracterísticas avaliadas nesta fase são **Instalabilidade** e **Adaptabilidade**, correspondentes às questões Q2, Q3 e Q1 da Fase 2, respectivamente. A subcaracterística Substituibilidade (Q4) foi excluída do escopo de execução por não se alinhar ao perfil de uso definido na Fase 1 — uma estudante com hardware básico em uso offline —, uma vez que as métricas associadas (linhas de código modificadas, compatibilidade de API entre modelos) pressupõem um perfil de desenvolvedora que não representa o cenário investigado.

A coleta foi realizada em dois ambientes distintos: **Zorin OS 18.1 Core** (Linux, baseado em Ubuntu 24.04) e **Windows 11**, conforme especificado no Plano de Avaliação. A execução foi automatizada por meio de script Python disponível no repositório do projeto, garantindo reprodutibilidade e rastreabilidade dos dados brutos.

> **Nota sobre versões do Ollama:** O script instalou e verificou automaticamente a versão disponível em cada ambiente no momento da execução. No Zorin OS 18.1 Core a versão instalada foi **0.30.10**, coletada em 23/06/2026. No Windows 11 a versão instalada foi **0.30.8**, coletada em 13/06/2026. Essa diferença de versão (patch) deve ser considerada como variável não controlada ao interpretar os resultados comparativos.

---

## 5.2.2 Resultados — Instalabilidade

Esta seção apresenta os dados coletados durante os testes de instalabilidade, contemplando as métricas PO-1.1 (Taxa de Sucesso na Instalação), PO-1.2 (Tempo Médio de Instalação) e PO-1.3 (Taxa de Sucesso na Desinstalação), conforme definidas na Fase 2 e no Plano de Avaliação da Fase 3.

O procedimento consistiu em 5 ciclos completos de instalação e desinstalação em cada ambiente, com o estado inicial do sistema verificado e limpo antes de cada tentativa. No Zorin OS, o script limpou caches do sistema entre cada ciclo; no Windows 11, o script verificou e removeu instalações anteriores antes de iniciar. O instalador oficial foi utilizado em ambos os casos (`curl -fsSL https://ollama.com/install.sh | sh` no Linux; instalador `.exe` no Windows).

### Dados Brutos — Instalabilidade (Zorin OS 18.1 Core)

**Tabela 1: Registros de instalabilidade — Zorin OS 18.1 Core**
*(Fonte: `instalabilidade_20260623_212835.csv`, coletado em 23/06/2026, Ollama v0.30.10)*

| Tentativa | Download (s) | Instalação (s) | Status instalação | Desinstalação (s) | Status desinstalação | Arquivos residuais |
|-----------|-------------|----------------|-------------------|-------------------|----------------------|--------------------|
| 1         | 0,75        | 118,17         | sucesso           | 2,06              | sucesso              | nenhum             |
| 2         | 0,40        | 248,01         | sucesso           | 2,07              | sucesso              | nenhum             |
| 3         | 0,86        | 332,70         | sucesso           | 2,11              | sucesso              | nenhum             |
| 4         | 0,42        | 221,91         | sucesso           | 2,06              | sucesso              | nenhum             |
| 5         | 0,42        | 206,23         | sucesso           | 2,07              | sucesso              | nenhum             |

> **Nota:** O tempo de instalação no Linux inclui o download do binário e a configuração do serviço systemd. A alta variação entre tentativas (118 s a 332 s) reflete flutuações de largura de banda na rede doméstica durante a coleta e é capturada pela métrica de variação interna (PO-3.3). O tempo de download é registrado separadamente e representa fração pequena do total.

### Dados Brutos — Instalabilidade (Windows 11)

**Tabela 2: Registros de instalabilidade — Windows 11**
*(Fonte: `instalabilidade_windows.csv`, coletado em 13/06/2026, Ollama v0.30.8)*

| Tentativa | Instalação (s) | Status instalação | Desinstalação (s) | Status desinstalação | Arquivos residuais |
|-----------|----------------|-------------------|-------------------|----------------------|--------------------|
| 1         | 107,86         | sucesso           | 13,84             | sucesso              | nenhum             |
| 2         | 98,29          | sucesso           | 13,82             | sucesso              | nenhum             |
| 3         | 115,45         | sucesso           | 13,40             | sucesso              | nenhum             |
| 4         | 88,75          | sucesso           | 12,90             | sucesso              | nenhum             |
| 5         | 90,01          | sucesso           | 12,94             | sucesso              | nenhum             |

> **Nota:** O log de Windows registrou `WARN: Residuais encontrados` na preparação inicial (pasta `C:\Users\galve\AppData\Local\Ollama`), referente a uma instalação preexistente removida pelo script antes da primeira tentativa. Todos os 5 ciclos partiram de ambiente limpo e nenhum resíduo foi detectado ao fim de cada desinstalação.

### Métricas Calculadas — Instalabilidade

**Tabela 3: Síntese das métricas de instalabilidade por ambiente**

| Métrica | Zorin OS 18.1 Core | Windows 11 | Critério (Fase 3) | Resultado |
|---------|-------------------|------------|-------------------|-----------|
| **PO-1.1** Taxa de sucesso na instalação | 100,0% (5/5) | 100,0% (5/5) | ≥ 90% | ✓ Aprovado |
| **PO-1.2** Tempo médio de instalação | **225,40 s** | **100,07 s** | ≤ 300 s | ✓ Aprovado (ambos) |
| **PO-1.2** Tempo mínimo de instalação | 118,17 s | 88,75 s | — | — |
| **PO-1.2** Tempo máximo de instalação | 332,70 s | 115,45 s | — | — |
| **PO-1.3** Taxa de sucesso na desinstalação | 100,0% (5/5) | 100,0% (5/5) | ≥ 90% | ✓ Aprovado |
| **PO-1.3** Tempo médio de desinstalação | 2,07 s | 13,38 s | — | — |
| **PO-1.3** Arquivos residuais detectados | nenhum | nenhum | ausência | ✓ Aprovado |

> **Nota sobre a variação de tempo de instalação no Zorin OS:** o coeficiente de variação interno foi de 34,3% (σ = 77,30 s sobre média = 225,40 s), ultrapassando o critério de ≤ 15% definido na métrica PO-3.3 para variação interna por ambiente. Essa variabilidade é atribuída a flutuações de rede durante o download do instalador. O Windows 11 apresentou variação interna de 11,5% (σ = 11,51 s), dentro do critério.

---

## 5.2.3 Resultados — Adaptabilidade

Esta seção apresenta os dados coletados durante os testes de adaptabilidade, contemplando as métricas PO-2.1 (Paridade Funcional entre SOs), PO-1.2/PO-2.2 (Desvio de Desempenho de Inferência entre SOs) e PO-3.3 (Taxa de Falhas por Ambiente).

O procedimento consistiu na execução de 5 inferências padronizadas em cada ambiente com o mesmo prompt: *"Explique o que é inteligência artificial em uma frase."* O tempo registrado corresponde ao tempo total de resposta (*time-to-response*), medido pelo script automatizado.

**Diferença metodológica relevante entre ambientes:** no Zorin OS 18.1 Core, o script executou uma inferência de aquecimento (*warm-up*) prévia e descartada das métricas — as 5 inferências registradas já refletem o modelo aquecido em memória (RAM cache quente). No Windows 11, não houve inferência de warm-up prévia; a inferência 1 inclui o custo de carregamento inicial do modelo (*cold start*).

### Dados Brutos — Adaptabilidade (Zorin OS 18.1 Core)

**Tabela 4: Registros de adaptabilidade — Zorin OS 18.1 Core**
*(Fonte: `adaptabilidade_20260623_212835.csv`, coletado em 23/06/2026. Warm-up de 6,16 s executado e descartado antes das 5 inferências.)*

| Inferência | Tempo de resposta (s) | Status  |
|------------|-----------------------|---------|
| 1          | 1,32                  | sucesso |
| 2          | 1,44                  | sucesso |
| 3          | 1,34                  | sucesso |
| 4          | 1,43                  | sucesso |
| 5          | 1,03                  | sucesso |

**Média: 1,31 s | Mín: 1,03 s | Máx: 1,44 s**

### Dados Brutos — Adaptabilidade (Windows 11)

**Tabela 5: Registros de adaptabilidade — Windows 11**
*(Fonte: `adaptabilidade_windows.csv` / log `log_portabilidade_windows.txt`, coletado em 13/06/2026. Sem warm-up prévio; a inferência 1 inclui cold start.)*

| Inferência | Tempo de resposta (s) | Status  | Observação |
|------------|-----------------------|---------|------------|
| 1          | 9,12                  | sucesso | Cold start (modelo sendo carregado) |
| 2          | 5,43                  | sucesso | Regime estacionário |
| 3          | 6,70                  | sucesso | Regime estacionário |
| 4          | 6,26                  | sucesso | Regime estacionário |
| 5          | 4,69                  | sucesso | Regime estacionário |

**Média total (inf. 1–5): 6,44 s | Média sem inf. 1 (inf. 2–5): 5,77 s**

### Métricas Calculadas — Adaptabilidade

Para o cálculo do desvio de desempenho (PO-1.2 / PO-2.2), são apresentadas duas abordagens, dada a diferença metodológica de warm-up entre os ambientes:

**Abordagem A — Comparação direta (Zorin pós warm-up vs. Windows completo):**

```
Média Zorin   = 1,31 s  (5 inferências, pós warm-up)
Média Windows = 6,44 s  (5 inferências, inclui cold start na inf. 1)
Média geral   = (1,31 + 6,44) / 2 = 3,88 s
Desvio PO-1.2 = |1,31 − 6,44| / 3,88 = 132,4%
```

**Abordagem B — Comparação sem cold start em ambos (mais justa):**

```
Média Zorin   = 1,31 s  (5 inferências pós warm-up)
Média Windows = (5,43 + 6,70 + 6,26 + 4,69) / 4 = 5,77 s  (inf. 2–5)
Média geral   = (1,31 + 5,77) / 2 = 3,54 s
Desvio PO-1.2 = |1,31 − 5,77| / 3,54 = 126,0%
```

Em ambas as abordagens, o desvio supera amplamente o critério de ≤ 20%.

**Tabela 6: Síntese das métricas de adaptabilidade por ambiente**

| Métrica | Zorin OS 18.1 Core | Windows 11 | Critério (Fase 3) | Resultado |
|---------|-------------------|------------|-------------------|-----------|
| **PO-2.1** Paridade funcional (taxa exec. sem falha) | 100,0% (5/5) | 100,0% (5/5) | 100% | ✓ Aprovado |
| **PO-1.2 / PO-2.2** Desvio de desempenho (Abord. A) | — | — | ≤ 20% | ✗ Reprovado — 132,4% |
| **PO-1.2 / PO-2.2** Desvio de desempenho (Abord. B) | — | — | ≤ 20% | ✗ Reprovado — 126,0% |
| **PO-3.3** Taxa de falhas por ambiente | 0,0% (0/5) | 0,0% (0/5) | ≤ 2% | ✓ Aprovado |

### Métricas Cruzadas entre Ambientes (PO-3.1, PO-3.2, PO-3.3)

**Tabela 7: Métricas de consistência entre ambientes**

| Métrica | Valor calculado | Critério (Fase 2/3) | Resultado |
|---------|----------------|---------------------|-----------|
| **PO-3.1** Taxa de sucesso por ambiente — Zorin OS | 100,0% | ≥ 95% | ✓ Aprovado |
| **PO-3.1** Taxa de sucesso por ambiente — Windows 11 | 100,0% | ≥ 95% | ✓ Aprovado |
| **PO-3.2** Desvio relativo de taxa de sucesso entre ambientes | 0,0% | ≤ 5% | ✓ Aprovado |
| **PO-3.3** Variação interna de tempo de instalação — Zorin OS (CV) | **34,3%** | ≤ 15% | ✗ Reprovado |
| **PO-3.3** Variação interna de tempo de instalação — Windows 11 (CV) | 11,5% | ≤ 15% | ✓ Aprovado |
| **PO-3.3** Variação cruzada de tempo médio de instalação entre ambientes | **77,0%** | ≤ 15% | ✗ Reprovado |
| **PO-3.3** Taxa de falhas específicas de ambiente — Zorin OS | 0,0% | ≤ 2% | ✓ Aprovado |
| **PO-3.3** Taxa de falhas específicas de ambiente — Windows 11 | 0,0% | ≤ 2% | ✓ Aprovado |

> **Cálculo da variação cruzada (PO-3.3):** `|225,40 − 100,07| / ((225,40 + 100,07) / 2) = 125,33 / 162,74 = 77,0%`. A diferença expressiva entre os tempos médios de instalação (225 s no Linux vs. 100 s no Windows) deve-se principalmente à alta variabilidade de rede no ambiente Linux durante a coleta em 23/06/2026.

---

## 5.2.4 Análise por Questão GQM

### Q1 — O Ollama com Qwen 2.5 3B se comporta de formas diferentes em diferentes sistemas operacionais? (Adaptabilidade)

**Hipótese formulada na Fase 2:** o sistema se comporta de forma funcionalmente equivalente em qualquer sistema operacional, com diferenças limitadas a variações de desempenho decorrentes das arquiteturas de hardware subjacentes.

**Análise dos resultados:**

Quanto à **paridade funcional** (PO-2.1), o resultado é inequívoco: em ambos os ambientes, todas as 5 inferências executadas com o prompt padronizado foram concluídas com sucesso, sem nenhuma falha registrada. A taxa de falhas (PO-3.3) foi de 0,0% nos dois sistemas operacionais. Neste aspecto, a hipótese é integralmente confirmada.

No entanto, o **desvio de desempenho de inferência** (PO-1.2 / PO-2.2) revela comportamento assimétrico entre as plataformas. O Zorin OS 18.1 Core apresentou tempo médio de resposta de 1,31 s (pós warm-up). O Windows 11 registrou 6,44 s no total e 5,77 s em regime estacionário (excluindo cold start). O desvio relativo calculado supera 125% em ambas as abordagens — muito além do limiar de 20% estabelecido na Fase 2.

Este resultado indica que, embora a paridade funcional seja plena, a eficiência de execução varia expressivamente entre as plataformas para o hardware testado (CPU Intel Core i5, AMD64, sem GPU dedicada). O ambiente Linux demonstrou desempenho de inferência entre 4 e 5 vezes superior ao Windows 11 nas condições avaliadas. A diferença de versão do Ollama entre os ambientes (0.30.10 no Linux vs. 0.30.8 no Windows) pode contribuir marginalmente para essa diferença, mas dificilmente explica uma magnitude desta ordem.

**Veredicto Q1:**
- Métrica PO-2.1 (Paridade funcional) — **Hipótese confirmada**: 100% de execuções bem-sucedidas em ambas as plataformas.
- Métrica PO-1.2 / PO-2.2 (Desvio de desempenho) — **Hipótese refutada**: desvio superior a 126%, excedendo o limite de 20% em ambas as abordagens de cálculo.

---

### Q2 — É possível instalar e desinstalar o Ollama de forma independente e sem resíduos? (Instalabilidade)

**Hipótese formulada na Fase 2:** a instalação e desinstalação completas são possíveis sem intervenção manual avançada, e a desinstalação não deixa resíduos no sistema.

**Análise dos resultados:**

A taxa de sucesso na instalação (PO-1.1) foi de 100% em ambos os ambientes (5/5 tentativas), superando o critério de 90%. O tempo médio de instalação foi de 225,40 s no Zorin OS e 100,07 s no Windows 11 — ambos abaixo do limite de 300 s (5 min) definido na Fase 3.

A taxa de sucesso na desinstalação (PO-1.3) foi igualmente de 100% (5/5) nos dois ambientes. O tempo médio de desinstalação foi de 2,07 s no Linux e 13,38 s no Windows. Nenhum arquivo residual foi detectado em qualquer tentativa de desinstalação em nenhum dos dois sistemas.

**Veredicto Q2:** Hipótese **confirmada** em todos os aspectos. O processo de instalação e desinstalação do Ollama demonstrou-se robusto e limpo nos dois ambientes avaliados, dentro dos critérios de aceitação definidos.

---

### Q3 — O processo de instalação apresenta erros ou inconsistências em diferentes ambientes? (Instalabilidade)

**Hipótese formulada na Fase 2:** o processo de instalação é consistente entre ambientes distintos, apresentando apenas variações de tempo sem falhas específicas por ambiente.

**Análise dos resultados:**

As taxas de sucesso por ambiente (PO-3.1) foram de 100% tanto no Zorin OS 18.1 Core quanto no Windows 11, dentro do critério de 95%. O desvio relativo de taxa de sucesso entre os dois ambientes foi de 0,0% (PO-3.2), bem abaixo do limite de 5%. Nenhuma falha específica de ambiente foi observada em qualquer das 10 tentativas realizadas (5 por sistema operacional).

Entretanto, **a hipótese é parcialmente refutada no que diz respeito à variação temporal**: a variação interna do Zorin OS atingiu 34,3% (coeficiente de variação), ultrapassando o critério de ≤ 15% da métrica PO-3.3. A variação cruzada entre os tempos médios dos dois ambientes foi de 77,0%, igualmente fora do critério. Esses resultados indicam que, embora não haja falhas de instalação, o processo apresenta inconsistências temporais significativas — especialmente no Linux, onde a dependência de download de rede introduz variabilidade considerável.

**Veredicto Q3:** Hipótese **parcialmente confirmada**. Não há falhas funcionais de instalação em nenhum ambiente, mas a variação temporal interna do Linux e a diferença cruzada entre ambientes excedem os critérios estabelecidos.

---

## 5.2.5 Interpretação e Discussão

### A instalação é realmente simples para um usuário leigo?

Os resultados indicam que **sim, do ponto de vista funcional**. A taxa de sucesso de 100% em ambas as plataformas e a ausência completa de resíduos após a desinstalação evidenciam que o processo de instalação do Ollama é suficientemente robusto para o perfil de usuário definido na Fase 1. O instalador oficial não exigiu nenhuma intervenção manual além da execução do comando inicial, não apresentou dependências ausentes e não deixou rastros no sistema após a remoção.

Do ponto de vista do **tempo**, a experiência difere entre os sistemas. No Windows 11, a instalação concluiu em média em 100 s com baixa variação. No Linux, o tempo médio foi de 225 s com alta variabilidade (entre 118 s e 332 s), o que pode surpreender o usuário leigo que espera uma experiência homogênea.

### O comportamento é equivalente entre os dois sistemas operacionais?

A resposta exige distinção entre os dois eixos avaliados.

Do ponto de vista **funcional**, o comportamento é completamente equivalente: todas as inferências foram bem-sucedidas em ambas as plataformas, sem nenhuma falha ou divergência de execução.

Do ponto de vista de **desempenho de inferência**, o comportamento difere de forma expressiva. O Zorin OS 18.1 Core apresentou tempo médio de inferência de 1,31 s (regime estacionário), enquanto o Windows 11 registrou 5,77 s nas mesmas condições. Esta diferença de aproximadamente 4,4× não era esperada pela hipótese formulada na Fase 2, que previa desvio máximo de 20%.

Hipóteses explicativas para essa divergência incluem: diferenças na gestão de memória e no escalonador de processos entre os dois sistemas operacionais; maior sobrecarga de subsistemas no Windows para operações de inferência com CPU; possível interferência de processos de sistema (antivírus, indexação, Windows Defender) não controlados durante a coleta; e diferença de versão do Ollama entre os ambientes (0.30.10 vs. 0.30.8). Testes adicionais com controle mais rigoroso do ambiente Windows — incluindo isolamento de processos em segundo plano — seriam necessários para isolar a causa.

### Síntese dos Resultados

**Tabela 8: Consolidação das métricas de portabilidade**

| ID | Métrica | Critério | Zorin OS | Windows 11 | Resultado |
|----|---------|----------|----------|------------|-----------|
| **PO-1.1** | Taxa de sucesso na instalação | ≥ 90% | 100,0% | 100,0% | ✓ Aprovado |
| **PO-1.2** | Tempo médio de instalação | ≤ 300 s | 225,40 s | 100,07 s | ✓ Aprovado (ambos) |
| **PO-1.3** | Taxa de sucesso na desinstalação | ≥ 90% | 100,0% | 100,0% | ✓ Aprovado |
| **PO-2.1** | Paridade funcional entre SOs | 100% | 100,0% | 100,0% | ✓ Aprovado |
| **PO-2.2** | Desvio de desempenho entre SOs | ≤ 20% | — | — | ✗ Reprovado (126,0%–132,4%) |
| **PO-2.3** | Taxa de falhas por ambiente | ≤ 2% | 0,0% | 0,0% | ✓ Aprovado |
| **PO-3.1** | Taxa de sucesso por ambiente | ≥ 95% | 100,0% | 100,0% | ✓ Aprovado |
| **PO-3.2** | Desvio relativo de sucesso entre ambientes | ≤ 5% | — | 0,0% | ✓ Aprovado |
| **PO-3.3** | Variação interna de tempo de instalação (Zorin) | ≤ 15% | 34,3% | — | ✗ Reprovado |
| **PO-3.3** | Variação interna de tempo de instalação (Windows) | ≤ 15% | — | 11,5% | ✓ Aprovado |
| **PO-3.3** | Variação cruzada de tempo médio entre ambientes | ≤ 15% | — | — | ✗ Reprovado (77,0%) |
| **PO-3.3** | Taxa de falhas específicas de ambiente | ≤ 2% | 0,0% | 0,0% | ✓ Aprovado |

De 12 verificações de métricas, **9 foram aprovadas** e **3 foram reprovadas** (PO-2.2 — desvio de desempenho de inferência; PO-3.3 — variação interna do Zorin OS; PO-3.3 — variação cruzada entre ambientes). O resultado global indica que o Ollama com Qwen 2.5 3B apresenta **alta portabilidade em termos de instalabilidade e paridade funcional**, com ressalvas relevantes: o desempenho de inferência varia significativamente entre plataformas em hardware sem aceleração por GPU, e o tempo de instalação no Linux apresenta variabilidade considerável dependente de condições de rede.

### Ameaças à Validade

**Diferença de versão do Ollama entre ambientes:** o Zorin OS executou a versão 0.30.10 e o Windows 11 a versão 0.30.8. Embora a diferença seja de patch, não se pode excluir completamente que otimizações de desempenho entre as versões contribuam para a diferença observada nas inferências.

**Metodologia de warm-up assimétrica:** o script do Zorin OS executou uma inferência de aquecimento prévia e descartada antes de medir as 5 inferências. O script do Windows não realizou esse procedimento. Isso cria uma comparação ligeiramente desfavorável ao Windows na Abordagem A. A Abordagem B tenta mitigar esse viés excluindo a inferência 1 do Windows, resultando ainda em desvio de 126%.

**Controle do ambiente Windows:** os logs de Windows não documentam a versão do antivírus ativo, processos em segundo plano ou configurações de energia — variáveis que podem influenciar os tempos de inferência.

**Variabilidade de rede no Zorin OS:** a alta variação de tempo de instalação no Linux (CV = 34,3%) está associada a flutuações de largura de banda durante o download do instalador em rede doméstica. Em um ambiente com rede controlada, os resultados seriam mais estáveis.
---

## Sobre o Uso de IA

Para a elaboração deste documento, modelos de linguagem de grande porte foram utilizados como apoio à estruturação do texto, revisão da linguagem acadêmica e organização das tabelas. Todo o conteúdo analítico cálculo das métricas, interpretação dos dados, formulação dos veredictos e identificação das ameaças à validade foi produzido e conferido pela equipe com base nos dados brutos coletados pelos scripts automatizados e disponíveis no repositório do projeto.

---

## Bibliografia

1. INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. **ISO/IEC 25010:2011** — Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models. Genebra: ISO, 2011.

2. FENTON, Norman; BIEMAN, James. **Software Metrics: A Rigorous and Practical Approach**. 3. ed. Boca Raton: CRC Press, 2015.

3. RAMOS, Cristiane Soares. **Medição baseada em objetivos: "Determinando o que medir"**. Material da disciplina FGA0315 — Qualidade de Software 1. Faculdade do Gama (FGA), Universidade de Brasília (UnB), 2026.

4. OLLAMA INC. **Ollama: The easiest way to build with open models**. Portal oficial de documentação, 2026. Disponível em: <https://ollama.com>. Acesso em: 23 jun. 2026.

5. QWEN TEAM. **Qwen2 Technical Report**. 2024. Disponível em: <https://arxiv.org/abs/2407.10671>. Acesso em: 23 jun. 2026.

---

## Histórico de Versão

| Versão | Data       | Descrição                                                                 | Autor            | Revisor          |
|--------|------------|---------------------------------------------------------------------------|------------------|------------------|
| 1.0    | 12/06/2026 | Criação do documento com resultados da execução                           | Gabriel          | Giovana Barbosa  |
| 1.1    | 23/06/2026 | Correção dos dados de instalabilidade do Windows (bug de duplicação); atualização com dados reais do ZorinOS (coleta 23/06/2026); recálculo de todas as métricas cruzadas; correção da Tabela 3 (tempos de instalação distintos por ambiente); adição de nota sobre versões do Ollama e assimetria de warm-up | Gabriel / Giovana Barbosa | — |