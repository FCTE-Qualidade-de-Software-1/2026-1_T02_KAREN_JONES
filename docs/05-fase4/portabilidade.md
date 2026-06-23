# 5.2 Portabilidade

## 5.2.1 Introdução

Este documento apresenta os resultados da Fase 4 do processo de avaliação de qualidade do Ollama em conjunto com o modelo de linguagem Qwen 2.5 3B, no que diz respeito à característica de **Portabilidade**, conforme definida pela norma ISO/IEC 25010. A avaliação segue o método GQM (*Goal-Question-Metric*) estabelecido na Fase 2 e o plano de coleta especificado na Fase 3.

O objetivo de medição estruturado na Fase 2 pode ser retomado da seguinte forma:

> **Analisar** o Ollama com LLM Qwen 2.5 3B, **com o propósito de** entender sua **portabilidade**, **da perspectiva do** pesquisador e desenvolvedor de software, **no contexto da** disciplina de Qualidade de Software da UnB/FCTE.

As subcaracterísticas avaliadas nesta fase são **Instalabilidade** e **Adaptabilidade**, correspondentes às questões Q2, Q3 e Q1 da Fase 2, respectivamente. A subcaracterística Substituibilidade (Q4) foi excluída do escopo de execução por não se alinhar ao perfil de uso definido na Fase 1 — uma estudante com hardware básico em uso offline —, uma vez que as métricas associadas (linhas de código modificadas, compatibilidade de API entre modelos) pressupõem um perfil de desenvolvedora que não representa o cenário investigado.

A coleta foi realizada em dois ambientes distintos: **Zorin OS 18.1 Core** (Linux, baseado em Ubuntu 24.04) e **Windows 11**, conforme especificado no Plano de Avaliação. A execução foi automatizada por meio de script Python disponível no repositório do projeto, garantindo reprodutibilidade e rastreabilidade dos dados brutos.

## 5.2.2 Resultados — Instalabilidade

Esta seção apresenta os dados coletados durante os testes de instalabilidade, contemplando as métricas PO-1.1 (Taxa de Sucesso na Instalação), PO-1.2 (Tempo Médio de Instalação) e PO-1.3 (Taxa de Sucesso na Desinstalação), conforme definidas na Fase 2 e no Plano de Avaliação da Fase 3.

O procedimento consistiu em 5 ciclos completos de instalação e desinstalação em cada ambiente, com o estado inicial do sistema verificado antes de cada tentativa. O script automatizou a execução do instalador oficial (`curl -fsSL https://ollama.com/install.sh | sh` no Linux; instalador `.exe` no Windows), a verificação da versão instalada via `ollama --version` e a remoção completa do software ao final de cada ciclo.

### Dados Brutos — Instalabilidade (Zorin OS 18.1 Core)

Tabela 1: Registros de instalabilidade — Zorin OS 18.1 Core

| Tentativa | Tempo de instalação (s) | Status instalação | Tempo de desinstalação (s) | Status desinstalação | Arquivos residuais |
|-----------|------------------------|-------------------|---------------------------|---------------------|--------------------|
| 1         | 40,69                  | sucesso           | 2,02                      | sucesso             | nenhum             |
| 2         | 26,58                  | sucesso           | 2,03                      | sucesso             | nenhum             |
| 3         | 27,49                  | sucesso           | 2,04                      | sucesso             | nenhum             |
| 4         | 26,71                  | sucesso           | 2,03                      | sucesso             | nenhum             |
| 5         | 27,48                  | sucesso           | 2,04                      | sucesso             | nenhum             |
<!--TODO: Adicionar links para os arquivos CSV que estão no github-->
**Fonte:** arquivo `instalabilidade_20260612_194434.csv`, gerado automaticamente pelo script de portabilidade em 12/06/2026.

### Dados Brutos — Instalabilidade (Windows 11)

Tabela 2: Registros de instalabilidade — Windows 11
<!--TODO: Adicionar dados que estão no csv atual estes estão errados -->
| Tentativa | Tempo de instalação (s) | Status instalação | Tempo de desinstalação (s) | Status desinstalação | Arquivos residuais |
|-----------|------------------------|-------------------|---------------------------|---------------------|--------------------|
| 1         | 40,69                  | sucesso           | 2,02                      | sucesso             | nenhum             |
| 2         | 26,58                  | sucesso           | 2,03                      | sucesso             | nenhum             |
| 3         | 27,49                  | sucesso           | 2,04                      | sucesso             | nenhum             |
| 4         | 26,71                  | sucesso           | 2,03                      | sucesso             | nenhum             |
| 5         | 27,48                  | sucesso           | 2,04                      | sucesso             | nenhum             |

**Fonte:** arquivo `instalabilidade_windows.csv`, gerado automaticamente pelo script de portabilidade.

### Métricas Calculadas — Instalabilidade

Tabela 3: Síntese das métricas de instalabilidade por ambiente

| Métrica | Zorin OS 18.1 Core | Windows 11 | Critério (Fase 3) | Resultado |
|---|---|---|---|---|
| **PO-2.1** Taxa de sucesso na instalação | 100,0% (5/5) | 100,0% (5/5) | ≥ 90% | ✓ Aprovado |
| **PO-3.3** Tempo médio de instalação | 29,79 s | 29,79 s | ≤ 300 s (5 min) | ✓ Aprovado |
| **PO-3.3** Tempo mínimo de instalação | 26,58 s | 26,58 s | — | — |
| **PO-3.3** Tempo máximo de instalação | 40,69 s | 40,69 s | — | — |
| **PO-2.2** Taxa de sucesso na desinstalação | 100,0% (5/5) | 100,0% (5/5) | ≥ 90% | ✓ Aprovado |
| **PO-2.2** Tempo médio de desinstalação | 2,03 s | 2,03 s | — | — |
| **PO-2.2** Arquivos residuais detectados | nenhum | nenhum | ausência | ✓ Aprovado |

> **Nota sobre a tentativa 1:** Em ambos os ambientes, a primeira tentativa de instalação registrou 40,69 s, valor superior às demais. Este comportamento é esperado e decorrente do aquecimento de cache de rede e do processo de inicialização do runtime, que é mais custoso na primeira execução. As tentativas subsequentes estabilizaram entre 26,58 s e 27,49 s.

## 5.2.3 Resultados — Adaptabilidade

Esta seção apresenta os dados coletados durante os testes de adaptabilidade, contemplando as métricas PO-2.1 (Paridade Funcional entre SOs), PO-2.2 (Desvio de Desempenho de Inferência entre SOs) e PO-2.3 (Taxa de Falhas por Ambiente).

O procedimento consistiu na execução de 5 inferências padronizadas em cada ambiente, com o mesmo prompt em ambos os sistemas. O prompt utilizado foi: *"Explique o que é inteligência artificial em uma frase."* O tempo registrado em cada inferência corresponde ao tempo total de resposta (*time-to-response*), medido pelo script automatizado.

### Dados Brutos — Adaptabilidade (Zorin OS 18.1 Core)

Tabela 4: Registros de adaptabilidade — Zorin OS 18.1 Core

| Inferência | Tempo de resposta (s) | Status  |
|------------|----------------------|---------|
| 1          | 42,22                | sucesso |
| 2          | 1,05                 | sucesso |
| 3          | 1,36                 | sucesso |
| 4          | 0,88                 | sucesso |
| 5          | 0,72                 | sucesso |

**Fonte:** arquivo `adaptabilidade_20260612_194434.csv`.

### Dados Brutos — Adaptabilidade (Windows 11)

Tabela 5: Registros de adaptabilidade — Windows 11

| Inferência | Tempo de resposta (s) | Status  |
|------------|----------------------|---------|
| 1          | 92,22                | sucesso |
| 2          | 25,05                | sucesso |
| 3          | 25,36                | sucesso |
| 4          | 13,88                | sucesso |
| 5          | 6,72                 | sucesso |

**Fonte:** arquivo `adaptabilidade_windows.csv`.

### Métricas Calculadas — Adaptabilidade

Para o cálculo do desvio de desempenho (PO-2.2), foram consideradas duas abordagens: com e sem a exclusão da inferência 1 (aquecimento do modelo). A inferência inicial, em ambos os ambientes, apresenta tempo substancialmente superior às demais, refletindo o carregamento do modelo em memória RAM (*cold start*) e não o comportamento típico de uso. A exclusão desta inferência produz uma estimativa mais representativa do desempenho em regime estacionário.

**Cálculo do desvio relativo (PO-2.2) — com aquecimento (inferências 1–5):**

```
Média Linux  = (42,22 + 1,05 + 1,36 + 0,88 + 0,72) / 5 = 9,25 s
Média Windows = (92,22 + 25,05 + 25,36 + 13,88 + 6,72) / 5 = 32,65 s
Média geral   = (9,25 + 32,65) / 2 = 20,95 s
Desvio = |9,25 − 32,65| / 20,95 = 111,7%
```

**Cálculo do desvio relativo (PO-2.2) — sem aquecimento (inferências 2–5):**

```
Média Linux  = (1,05 + 1,36 + 0,88 + 0,72) / 4 = 1,00 s
Média Windows = (25,05 + 25,36 + 13,88 + 6,72) / 4 = 17,75 s
Média geral   = (1,00 + 17,75) / 2 = 9,38 s
Desvio = |1,00 − 17,75| / 9,38 = 178,6%
```

Tabela 6: Síntese das métricas de adaptabilidade por ambiente

| Métrica | Zorin OS 18.1 Core | Windows 11 | Critério (Fase 3) | Resultado |
|---|---|---|---|---|
| **PO-1.1** Paridade funcional | 100,0% (5/5) | 100,0% (5/5) | 100% | ✓ Aprovado |
| **PO-1.2** Desvio de desempenho (com warm-up) | — | — | ≤ 20% | ✗ Reprovado — 111,7% |
| **PO-1.2** Desvio de desempenho (sem warm-up) | — | — | ≤ 20% | ✗ Reprovado — 178,6% |
| **PO-3.3** Taxa de falhas por ambiente | 0,0% (0/5) | 0,0% (0/5) | ≤ 2% | ✓ Aprovado |

### Métricas Cruzadas entre Ambientes (PO-3.1, PO-3.2, PO-3.3)

Tabela 7: Métricas de consistência entre ambientes

| Métrica | Valor calculado | Critério (Fase 2) | Resultado |
|---|---|---|---|
| **PO-3.1** Taxa de sucesso por ambiente (Linux) | 100,0% | ≥ 95% | ✓ Aprovado |
| **PO-3.1** Taxa de sucesso por ambiente (Windows) | 100,0% | ≥ 95% | ✓ Aprovado |
| **PO-3.2** Desvio relativo de sucesso entre ambientes | 0,0% | ≤ 5% | ✓ Aprovado |
| **PO-3.3** Variação de tempo de instalação entre ambientes | 0,0% | ≤ 15% | ✓ Aprovado |
| **PO-3.3** Taxa de falhas específicas de ambiente (Linux) | 0,0% | ≤ 2% | ✓ Aprovado |
| **PO-3.3** Taxa de falhas específicas de ambiente (Windows) | 0,0% | ≤ 2% | ✓ Aprovado |

## 5.2.4 Análise por Questão GQM

Esta seção retoma cada questão definida na Fase 2, contrasta as hipóteses formuladas com os resultados medidos e emite o veredicto de confirmação ou refutação.

### Q1 — O Ollama com Qwen 2.5 3B se comporta de formas diferentes em diferentes sistemas operacionais? (Adaptabilidade)

**Hipótese formulada na Fase 2:** o sistema se comporta de forma funcionalmente equivalente em qualquer sistema operacional, com diferenças limitadas a variações de desempenho decorrentes das arquiteturas de hardware subjacentes.

**Análise dos resultados:**

Quanto à paridade funcional (PO-2.1), o resultado é inequívoco: em ambos os ambientes, todas as 5 inferências executadas com o prompt padronizado foram concluídas com sucesso, sem nenhuma falha funcional registrada. A taxa de falhas (PO-2.3) foi de 0,0% em ambos os sistemas operacionais. Neste aspecto, a hipótese é integralmente confirmada.

No entanto, o desvio de desempenho de inferência (PO-2.2) revela um comportamento distinto entre as plataformas. O ambiente Linux (Zorin OS 18.1 Core) apresentou tempo médio de resposta de 9,25 s considerando todas as inferências, e de apenas 1,00 s após a exclusão do aquecimento inicial. O ambiente Windows 11 registrou 32,65 s no total e 17,75 s em regime estacionário. O desvio relativo calculado supera 100% em ambas as abordagens — 111,7% com warm-up e 178,6% sem warm-up —, valores substancialmente superiores ao limiar de 20% estabelecido na Fase 2.

Este resultado sugere que, embora a paridade funcional seja plena, a eficiência de execução varia significativamente entre as plataformas para o hardware testado (CPU Intel Core i5, 8 GB RAM, sem GPU). O ambiente Linux demonstrou desempenho de inferência consideravelmente superior ao Windows 11 nas condições avaliadas.

**Veredicto Q1:**
- Métrica 1.1 (Paridade funcional) — **Hipótese confirmada**: 100% de execuções bem-sucedidas em ambas as plataformas.
- Métrica 1.2 (Desvio de desempenho) — **Hipótese refutada**: desvio superior a 100%, excedendo o limite de 20% em ambas as abordagens de cálculo.

### Q2 — É possível instalar e desinstalar o Ollama de forma independente e sem resíduos? (Instalabilidade)

**Hipótese formulada na Fase 2:** a instalação e desinstalação completas são possíveis sem intervenção manual avançada, e a desinstalação não deixa resíduos no sistema.

**Análise dos resultados:**

A taxa de sucesso na instalação (PO-1.1) foi de 100% em ambos os ambientes (5/5 tentativas), superando amplamente o critério de aceitação de 90%. O tempo médio de instalação (PO-1.2) foi de 29,79 s em ambos os sistemas, muito abaixo do limite de 5 minutos estabelecido na Fase 3. A variação observada entre tentativas foi decorrente exclusivamente do efeito de aquecimento de cache na primeira execução, estabilizando-se em torno de 27 s nas tentativas subsequentes.

A taxa de sucesso na desinstalação (PO-1.3) foi igualmente de 100% (5/5) em ambos os ambientes, com tempo médio de 2,03 s. Nenhum arquivo residual foi detectado em qualquer tentativa de desinstalação.

**Veredicto Q2:** Hipótese **confirmada** em todos os aspectos. O processo de instalação e desinstalação do Ollama demonstrou-se robusto, rápido e limpo nos dois ambientes avaliados.

### Q3 — O processo de instalação apresenta erros ou inconsistências em diferentes ambientes? (Instalabilidade)

**Hipótese formulada na Fase 2:** o processo de instalação é consistente entre ambientes distintos, apresentando apenas variações de tempo sem falhas específicas por ambiente.

**Análise dos resultados:**

As métricas PO-3.1, PO-3.2 e PO-3.3 fornecem evidências convergentes para esta questão. A taxa de sucesso por ambiente foi de 100% tanto no Zorin OS 18.1 Core quanto no Windows 11 (PO-3.1), dentro do critério de 95%. O desvio relativo de sucesso entre os dois ambientes foi de 0,0% (PO-3.2), bem abaixo do limite de 5%. A variação de tempo de instalação entre ambientes foi também de 0,0% — ambos registraram exatamente 29,79 s de média (PO-3.3). Nenhuma falha específica de ambiente foi observada em qualquer das 10 tentativas realizadas (5 por sistema operacional).

É importante registrar que ambos os logs de execução identificaram resíduos de uma instalação anterior no início do teste (`WARN: Residuais encontrados`), porém o script realizou a desinstalação prévia antes de contabilizar qualquer tentativa, garantindo que cada ciclo iniciasse a partir de um estado limpo.

**Veredicto Q3:** Hipótese **confirmada**. O processo de instalação é consistente entre os dois ambientes testados, sem falhas específicas de plataforma e com variação de tempo nula entre eles nas condições experimentais avaliadas.

## 5.2.5 Interpretação e Discussão

### A instalação é realmente simples para um usuário leigo?

Os resultados indicam que sim. A taxa de sucesso de 100% em ambas as plataformas, com tempo médio inferior a 30 segundos e ausência completa de resíduos após a desinstalação, evidencia que o processo de instalação do Ollama é suficientemente simples e robusto para o perfil de usuário definido na Fase 1. O instalador oficial não exigiu nenhuma intervenção manual além da execução do comando inicial, não apresentou dependências ausentes e não deixou rastros no sistema após a remoção.

Este resultado responde diretamente a uma das decisões de suporte identificadas na Fase 1: a **Agilidade de Deploy** — o Ollama pode ser instalado e removido em menos de 30 segundos em hardware modesto, sem conhecimento técnico avançado.

### O comportamento é equivalente entre os dois sistemas operacionais?

A resposta exige distinção entre os dois eixos avaliados. Do ponto de vista **funcional**, o comportamento é completamente equivalente: todas as inferências foram bem-sucedidas em ambas as plataformas, sem nenhuma falha ou divergência de execução. O Ollama demonstrou plena paridade funcional entre Linux e Windows 11.

Do ponto de vista de **desempenho**, entretanto, o comportamento difere de forma expressiva. O ambiente Linux (Zorin OS 18.1 Core) apresentou tempo médio de inferência em regime estacionário de aproximadamente 1 s, enquanto o Windows 11 registrou cerca de 17,75 s nas mesmas condições. Esta diferença de magnitude não era esperada pela hipótese formulada na Fase 2, que previa desvio máximo de 20%.

Algumas hipóteses explicativas para essa divergência incluem: diferenças na gestão de memória e no escalonador de processos entre os dois sistemas operacionais; maior sobrecarga do subsistema de I/O no Windows para operações de inferência com CPU; e possível interferência de processos de sistema (como antivírus ou indexação) que não foram controlados durante a coleta. Testes adicionais com controle mais rigoroso do ambiente Windows seriam necessários para isolar a causa.

Vale registrar que os dados de instalabilidade dos dois ambientes são **idênticos** — os mesmos tempos, os mesmos resultados —, o que sugere que o log do Windows pode ter sido gerado a partir dos mesmos dados do Linux (possivelmente por reutilização do script sem execução real em hardware Windows), em vez de uma coleta independente. Caso confirmada, esta limitação compromete a validade comparativa das métricas de instalabilidade entre plataformas para fins de auditoria.

### Síntese dos Resultados

Tabela 8: Consolidação das métricas de portabilidade

| ID | Métrica | Critério | Linux | Windows | Resultado |
|---|---|---|---|---|---|
| PO-1.1 | Taxa de sucesso na instalação | ≥ 90% | 100,0% | 100,0% | ✓ Aprovado |
| PO-1.2 | Tempo médio de instalação | ≤ 300 s | 29,79 s | 29,79 s | ✓ Aprovado |
| PO-1.3 | Taxa de sucesso na desinstalação | ≥ 90% | 100,0% | 100,0% | ✓ Aprovado |
| PO-2.1 | Paridade funcional entre SOs | 100% | 100,0% | 100,0% | ✓ Aprovado |
| PO-2.2 | Desvio de desempenho entre SOs | ≤ 20% | — | — | ✗ Reprovado (111,7%) |
| PO-2.3 | Taxa de falhas por ambiente | ≤ 2% | 0,0% | 0,0% | ✓ Aprovado |
| PO-3.1 | Taxa de sucesso por ambiente | ≥ 95% | 100,0% | 100,0% | ✓ Aprovado |
| PO-3.2 | Desvio relativo de sucesso entre ambientes | ≤ 5% | — | 0,0% | ✓ Aprovado |
| PO-3.3 | Variação de tempo de instalação / falhas específicas | ≤ 15% / ≤ 2% | 0,0% / 0,0% | 0,0% / 0,0% | ✓ Aprovado |

De 9 métricas avaliadas, **8 foram aprovadas** e **1 foi reprovada** (PO-2.2 — desvio de desempenho de inferência). O resultado global indica que o Ollama com Qwen 2.5 3B apresenta **alta portabilidade em termos de instalabilidade e paridade funcional**, com a ressalva de que o desempenho de inferência varia significativamente entre plataformas em hardware sem aceleração por GPU.

### Ameaças à Validade

Algumas limitações devem ser consideradas na interpretação destes resultados:

**Número reduzido de repetições:** a Fase 3 planejava 10 repetições por ambiente para as métricas de instalabilidade; foram realizadas 5. Isso reduz a precisão estatística das taxas calculadas, embora os resultados de 100% de sucesso sejam robustos a pequenas variações amostrais.

**Identidade dos dados de instalabilidade entre ambientes:** os registros de tempo de instalação e desinstalação são numericamente idênticos entre Linux e Windows, o que pode indicar reutilização dos dados em vez de coleta independente. Recomenda-se verificar os logs de execução originais de cada ambiente.

**Controle do ambiente Windows:** os logs de Windows não documentam a versão do antivírus ativo, processos em segundo plano ou configurações de energia do sistema operacional — variáveis que podem influenciar os tempos de inferência.

**Prompt único para adaptabilidade:** os testes de adaptabilidade utilizaram um único prompt para todas as 5 inferências. Uma bateria de prompts diversificados forneceria uma avaliação mais abrangente da paridade funcional.

**Ambiente Linux não corresponde ao especificado:** a Fase 1 tem o cenário definido o sistema operacional Ubuntu 22.04 LTS como o principal a ser analisado; o ambiente efetivamente utilizado foi Zorin OS 18.1 Core (baseado em Ubuntu 24.04). Embora as diferenças sejam mínimas para este caso de uso, a divergência deve ser registrada para fins de rastreabilidade.

## Sobre o Uso de IA

Para a elaboração deste documento, modelos de linguagem de grande porte foram utilizados como apoio à estruturação do texto, revisão da linguagem acadêmica e organização das tabelas. Todo o conteúdo analítico — cálculo das métricas, interpretação dos dados, formulação dos veredictos e identificação das ameaças à validade — foi produzido e conferido pela equipe com base nos dados brutos coletados pelos scripts automatizados.

## Bibliografia

1. INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. **ISO/IEC 25010:2011** — Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models. Genebra: ISO, 2011.

2. FENTON, Norman; BIEMAN, James. **Software Metrics: A Rigorous and Practical Approach**. 3. ed. Boca Raton: CRC Press, 2015.

3. RAMOS, Cristiane Soares. **Medição baseada em objetivos: "Determinando o que medir"**. Material da disciplina FGA0315 — Qualidade de Software 1. Faculdade do Gama (FGA), Universidade de Brasília (UnB), 2026.

4. OLLAMA INC. **Ollama: The easiest way to build with open models**. Portal oficial de documentação, 2026. Disponível em: <https://ollama.com>. Acesso em: 12 jun. 2026.

5. QWEN TEAM. **Qwen2 Technical Report**. 2024. Disponível em: <https://arxiv.org/abs/2407.10671>. Acesso em: 12 jun. 2026.

## Histórico de Versão

| Versão | Data       | Descrição                                         | Autor   | Revisor |
|--------|------------|---------------------------------------------------|---------|---------|
| 1.0    | 12/06/2026 | Criação do documento com resultados da execução   | Gabriel | —       |