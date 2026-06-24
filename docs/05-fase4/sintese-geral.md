# 5.3 Síntese Geral

## 5.3.1 Introdução

Este documento encerra o ciclo de avaliação iniciado na Fase 1 e reúne, em perspectiva unificada, tudo o que a equipe Karen Jones foi capaz de observar, medir e concluir sobre o Ollama executando o modelo Qwen 2.5 3B. Mais do que um relatório de métricas, este artefato é o registro honesto de uma jornada de aprendizado — da construção do cenário de avaliação à execução dos scripts de coleta, passando pela descoberta de que avaliar software de forma rigorosa é um exercício muito mais complexo do que parece no início.

O objetivo de medição que norteou todo o projeto, formulado na Fase 2 com o método GQM, pode ser retomado da seguinte forma:

> **Analisar** o Ollama com LLM Qwen 2.5 3B, **com o propósito de** entender sua qualidade técnica em termos de **eficiência de desempenho** e **portabilidade**, **da perspectiva do** pesquisador e desenvolvedor de software, **no contexto da** disciplina de Qualidade de Software da UnB/FCTE.

O cenário que motivou toda a avaliação foi simples e próximo da realidade de muitos estudantes brasileiros: uma universitária com um notebook básico (8 GB de RAM, sem GPU dedicada, Windows 11), que precisa de um assistente de estudos que funcione sem internet, e um colega que usa a mesma ferramenta no Linux. A pergunta central era: *o Ollama realmente entrega o que promete para quem tem hardware modesto?*

---

## 5.3.2 Consolidação dos Resultados

### 5.3.2.1 Portabilidade

A característica de Portabilidade foi a que recebeu cobertura empírica mais completa nesta avaliação. Os testes foram executados em dois ambientes reais: **Zorin OS 18.1 Core** (Linux, baseado em Ubuntu 24.04, Ollama v0.30.10, coletado em 23/06/2026) e **Windows 11** (Ollama v0.30.8, coletado em 13/06/2026). A automação via script Python garantiu reprodutibilidade e rastreabilidade dos dados brutos.

**Tabela 1: Consolidação das métricas de portabilidade**

| ID | Métrica | Critério | Zorin OS | Windows 11 | Resultado |
|----|---------|----------|----------|------------|-----------|
| PO-1.1 | Taxa de sucesso na instalação | ≥ 90% | 100,0% | 100,0% | ✓ Aprovado |
| PO-1.2 | Tempo médio de instalação | ≤ 300 s | 225,4 s | 100,1 s | ✓ Aprovado |
| PO-1.3 | Taxa de sucesso na desinstalação | ≥ 90% | 100,0% | 100,0% | ✓ Aprovado |
| PO-1.3 | Arquivos residuais após desinstalação | ausência | nenhum | nenhum | ✓ Aprovado |
| PO-2.1 | Paridade funcional entre SOs | 100% | 100,0% | 100,0% | ✓ Aprovado |
| PO-2.2 | Desvio de desempenho de inferência entre SOs | ≤ 20% | — | — | ✗ Reprovado (126,0%) |
| PO-2.3 | Taxa de falhas por ambiente | ≤ 2% | 0,0% | 0,0% | ✓ Aprovado |
| PO-3.1 | Taxa de sucesso por ambiente | ≥ 95% | 100,0% | 100,0% | ✓ Aprovado |
| PO-3.2 | Desvio relativo de taxa de sucesso entre ambientes | ≤ 5% | — | 0,0% | ✓ Aprovado |
| PO-3.3 | Variação interna de tempo de instalação — Zorin OS (CV) | ≤ 15% | 34,3% | — | ✗ Reprovado |
| PO-3.3 | Variação interna de tempo de instalação — Windows 11 (CV) | ≤ 15% | — | 11,5% | ✓ Aprovado |
| PO-3.3 | Taxa de falhas específicas de ambiente | ≤ 2% | 0,0% | 0,0% | ✓ Aprovado |

De 12 verificações, **10 foram aprovadas** e **2 foram reprovadas**: o desvio de desempenho de inferência entre plataformas (PO-2.2, 126%) e a variação interna de tempo de instalação no Zorin OS (PO-3.3, CV = 34,3%, atribuída a flutuações de rede durante a coleta).

Os dados de adaptabilidade merecem destaque: o Zorin OS apresentou tempo médio de inferência de **1,31 s** (pós aquecimento), enquanto o Windows 11 registrou **5,77 s** em regime estacionário. Essa diferença de aproximadamente **4,4×** entre as plataformas superou em muito o limiar de 20% estabelecido como critério, sinalizando que a experiência do usuário varia significativamente dependendo do sistema operacional, mesmo com hardware idêntico.

### 5.3.2.2 Eficiência de Desempenho

A característica de Eficiência de Desempenho foi planejada com rigor na Fase 2 — métricas bem definidas como TTFT (Time to First Token), TPS (Tokens por Segundo), consumo de RAM e CPU, e fator de escalonamento de contexto — e instrumentada na Fase 3 com scripts Python e psutil. No entanto, a execução completa dos testes de eficiência não foi concluída dentro do prazo desta avaliação.

O que foi possível observar empiricamente sobre o comportamento temporal do Ollama com Qwen 2.5 3B veio dos próprios testes de adaptabilidade realizados no âmbito da Portabilidade. Nesses testes, com um prompt de inferência simples executado 5 vezes em cada ambiente, os tempos registrados foram:

- **Zorin OS 18.1 Core:** média de 1,31 s por inferência (pós aquecimento do modelo)
- **Windows 11:** média de 6,44 s por inferência (incluindo cold start) / 5,77 s em regime estacionário

Esses valores, embora obtidos com um único prompt e sem a variação sistemática de tamanho de contexto prevista no plano, fornecem uma referência real e concreta sobre a latência do sistema. No Zorin OS, o resultado situa-se bem abaixo do critério de TTFT ≤ 5 s para 512 tokens, sugerindo que o sistema seria aprovado nessa métrica em ambiente Linux. No Windows, os tempos ficaram próximos do limite, levantando a hipótese de que o critério poderia ser excedido em contextos mais longos.

Sobre o consumo de recursos, os logs de execução dos testes de portabilidade indicam que o sistema operou de forma estável em ambas as plataformas, sem relatos de travamentos ou falhas por falta de memória. O hardware utilizado — Intel Core i5, 8 GB de RAM, sem GPU — conseguiu sustentar a execução do Qwen 2.5 3B sem comprometer a responsividade do sistema operacional durante os testes realizados. Esse indício qualitativo, embora não substitua os dados quantitativos planejados, sugere que o consumo de RAM ficou dentro de limites operacionais aceitáveis para o hardware do cenário avaliado.

---

## 5.3.3 Resposta às Decisões Apoiadas

Na Fase 1, a equipe identificou quatro decisões concretas que a avaliação deveria apoiar. Com os dados coletados, é possível respondê-las da seguinte forma:

**Decisão 1 — Validação de Hardware:** *O hardware com 8 GB de RAM e sem GPU é suficiente para rodar o Qwen 2.5 3B via Ollama?*

A resposta que os dados permitem dar é: **sim, com ressalvas**. O sistema executou todas as inferências sem falhas em ambas as plataformas e sem relatos de instabilidade por falta de memória. Os tempos de resposta observados — especialmente no Linux, com média de 1,31 s — são compatíveis com uso interativo. No Windows, os tempos foram maiores (em torno de 5–6 s), mas ainda dentro de um limiar que, dependendo da tarefa, pode ser aceitável. Para tarefas de resumo e apoio a estudos sem necessidade de resposta imediata, o hardware se mostrou viável. Para cenários de uso contínuo e intenso, os dados sugerem que o Linux oferece uma experiência mais fluida nessa configuração.

**Decisão 2 — Adoção de Sistemas Operacionais:** *Há paridade de desempenho entre Windows e Linux?*

A resposta é **não** — pelo menos não em termos de velocidade de inferência. Há paridade *funcional* total: o sistema instalou, executou e desinstalou sem falhas em ambas as plataformas. Mas o desempenho de inferência no Linux foi aproximadamente 4,4 vezes mais rápido do que no Windows para o hardware testado. Para estudantes e pesquisadores que têm a opção de usar Linux, os dados indicam uma vantagem de desempenho expressiva.

**Decisão 3 — Configuração de Modelo:** *O limite de contexto de tokens precisa ser ajustado para manter o TTFT em níveis aceitáveis?*

Esta questão não pode ser respondida com precisão, pois os testes de variação de contexto (512, 1024, 2048 e 4096 tokens) previstos na Fase 3 não foram executados. O que se sabe é que, com um prompt curto e padronizado, o sistema respondeu em 1,31 s no Linux e em aproximadamente 5,77 s no Windows. Se esses valores já se situam próximos do limiar em Windows, é razoável supor que contextos maiores possam ultrapassá-lo. Esta permanece como uma questão aberta para trabalhos futuros.

**Decisão 4 — Agilidade de Deploy:** *O processo de instalação é simples o suficiente para ser recomendado a qualquer perfil de usuário?*

Sim, e esta é talvez a conclusão mais sólida e inequívoca desta avaliação. A instalação alcançou 100% de sucesso em 5 tentativas em cada sistema operacional, com tempo médio de 100 s no Windows e 225 s no Linux (com variação atribuída à rede). A desinstalação foi igualmente limpa e rápida, sem deixar resíduos. Um usuário com conhecimento mínimo de terminal seria capaz de instalar e remover o Ollama sem dificuldade técnica. A agilidade de deploy é, portanto, **confirmada**.

---

## 5.3.4 Conclusão

Quando a equipe começou este projeto, a pergunta que motivava tudo era relativamente direta: *o Ollama com Qwen 2.5 3B funciona de verdade em hardware modesto?* Após quatro fases de trabalho — desde a construção do cenário de avaliação até a execução dos scripts e análise dos dados — a resposta que os dados permitem dar é mais matizada e, por isso, mais interessante do que um simples "sim" ou "não".

O Ollama demonstrou ser uma ferramenta genuinamente acessível sob o ângulo da instalabilidade e da paridade funcional. Instalar, usar e remover o software é um processo simples, limpo e reproduzível tanto no Windows quanto no Linux. Para uma estudante que nunca usou a linha de comando com frequência, o processo é surpreendentemente direto. Esse resultado responde de forma positiva à questão central da Portabilidade.

O ponto de maior aprendizado — e de maior surpresa — foi a diferença de desempenho de inferência entre as plataformas. Esperava-se que sistemas operacionais diferentes pudessem introduzir alguma variação, mas um desvio de 126% (aproximadamente 4,4× mais rápido no Linux do que no Windows) foi significativamente maior do que a hipótese inicial de ≤ 20% formulada na Fase 2. Esse resultado não invalida o uso do Ollama no Windows, mas indica que a plataforma importa — e que recomendar o sistema sem essa ressalva seria uma simplificação inadequada.

Do ponto de vista da eficiência de desempenho, os dados coletados são parciais, mas apontam na direção de que o Qwen 2.5 3B é operável em 8 GB de RAM sem GPU, com uma experiência de uso interativo razoável no Linux. No Windows, a latência maior pode ser compensada dependendo do tipo de tarefa — para resumos e apoio a estudos sem urgência de resposta imediata, o sistema permanece viável.

A conclusão prática que a equipe pode oferecer, com base nos dados que foi possível coletar, é a seguinte: **o Ollama com Qwen 2.5 3B é uma opção real e funcional para estudantes e pesquisadores com hardware modesto, especialmente em Linux, onde o desempenho de inferência se mostrou compatível com uso interativo cotidiano**. Para usuários Windows, o sistema funciona, mas com latência notavelmente maior, o que deve ser comunicado claramente a quem considera adotá-lo.

---

## 5.3.5 Ameaças à Validade

Toda avaliação empírica carrega limitações que precisam ser reconhecidas para que os resultados sejam interpretados com responsabilidade.

**Ambiente único de hardware.** Todos os testes foram realizados em uma única máquina (ou em configurações muito próximas), o que limita a generalização dos resultados. Variações de CPU, memória, armazenamento e estado do sistema podem produzir resultados diferentes em outras máquinas com as mesmas especificações nominais.

**Versões distintas do Ollama entre ambientes.** O Zorin OS utilizou a versão 0.30.10, coletada em 23/06/2026, enquanto o Windows 11 utilizou a versão 0.30.8, coletada em 13/06/2026. A diferença de patch pode introduzir variações de desempenho não controladas, e deve ser considerada ao interpretar comparações diretas entre os dois ambientes.

**Assimetria metodológica nos testes de adaptabilidade.** O script do Zorin OS realizou uma inferência de aquecimento prévia e descartada antes de medir as 5 inferências oficiais. O script do Windows não incluiu esse procedimento, o que pode ter introduzido um viés favorável ao Linux na comparação direta. A abordagem que exclui a inferência 1 do Windows (média de 5,77 s) tenta mitigar esse efeito, mas a assimetria permanece como uma limitação metodológica.

**Ausência de controle de processos em segundo plano no Windows.** Os logs de execução do Windows não documentam o estado de processos como antivírus, indexação e configurações de energia, todos capazes de influenciar os tempos de inferência de forma não controlada.

---

## 5.3.6 Reflexão sobre o Processo

Avaliar qualidade de software é diferente de usar software. Essa distinção, aparentemente óbvia, foi o aprendizado mais profundo que este projeto proporcionou à equipe.

Construir um plano de avaliação com o método GQM obriga a ser explícito sobre o que se quer saber antes de olhar para qualquer dado. Formular hipóteses com antecedência muda a forma como os resultados são lidos — uma métrica reprovada deixa de ser um problema e passa a ser uma descoberta. A métrica PO-2.2, que reprovaria por 126% acima do critério de 20%, não é uma falha do Ollama no sentido de que o software é ruim; é uma descoberta sobre como o sistema operacional importa de formas que não eram óbvias antes da medição.

A automação da coleta de dados, implementada via script Python para os testes de portabilidade, foi uma das decisões mais acertadas do projeto. Ela garantiu que os dados fossem coletados de forma consistente, com rastreabilidade dos logs, e que as 5 repetições em cada ambiente fossem comparáveis entre si. A experiência mostrou que o esforço inicial de escrever o script é compensado pela confiança que os dados automatizados trazem — sabe-se exatamente o que foi medido e como.

O projeto também evidenciou os desafios reais de conduzir avaliações empíricas dentro das restrições de tempo e recursos de um trabalho acadêmico. Planejar é mais fácil do que executar. Os testes de eficiência de desempenho foram planejados com cuidado, mas sua execução completa não foi viável no prazo disponível. Essa limitação, longe de ser uma vergonha, é um resultado em si: mostra o quanto um plano de avaliação rigoroso exige, e quão importante é calibrar o escopo ao que é realista.

Por fim, o projeto confirmou que a pergunta que motivou tudo — *o Ollama funciona para estudantes com hardware modesto?* — não tem uma resposta única. Funciona bem no Linux, funciona com ressalvas no Windows, funciona para tarefas simples, pode ter limitações para contextos longos. Essa nuance é exatamente o que uma avaliação bem conduzida deveria produzir.

---

## Sobre o Uso de IA

Para a elaboração deste documento, modelos de linguagem de grande porte foram utilizados como apoio à estruturação do texto, revisão da linguagem acadêmica e organização das tabelas. Todo o conteúdo analítico — interpretação dos dados, formulação dos veredictos, identificação das ameaças à validade e a reflexão sobre o processo — foi produzido e conferido pela equipe com base nos dados brutos coletados pelos scripts automatizados e disponíveis no repositório do projeto.

---

## Bibliografia

1. INTERNATIONAL ORGANIZATION FOR STANDARDIZATION. **ISO/IEC 25010:2011** — Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — System and software quality models. Genebra: ISO, 2011.

2. FENTON, Norman; BIEMAN, James. **Software Metrics: A Rigorous and Practical Approach**. 3. ed. Boca Raton: CRC Press, 2015.

3. RAMOS, Cristiane Soares. **Medição baseada em objetivos: "Determinando o que medir"**. Material da disciplina FGA0315 — Qualidade de Software 1. Faculdade do Gama (FGA), Universidade de Brasília (UnB), 2026.

4. OLLAMA INC. **Ollama: The easiest way to build with open models**. Portal oficial de documentação, 2026. Disponível em: <https://ollama.com>. Acesso em: 23 jun. 2026.

5. QWEN TEAM. **Qwen2 Technical Report**. 2024. Disponível em: <https://arxiv.org/abs/2407.10671>. Acesso em: 23 jun. 2026.

---

## Histórico de Versão

| Versão | Data       | Descrição | Autor | Revisor |
|--------|------------|-----------|-------|---------|
| 1.0    | 12/06/2026 | Criação do documento | Gabriel | — |
| 1.1    | 23/06/2026 | Reescrita completa com dados reais de portabilidade (Windows e ZorinOS corrigidos); consolidação das conclusões sobre eficiência a partir dos dados disponíveis; adição da seção de reflexão sobre o processo | Gabriel / Giovana Barbosa | — |