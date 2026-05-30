# 2.4 Justificativas

## 2.4.1 Por que o Qwen 2.5:3B?

### Tamanho e Viabilidade Local
A versão de **3 bilhões de parâmetros** do Qwen 2.5 caracteriza-se como um modelo robusto, mas otimizado o suficiente para ser executado com fluidez em hardware de consumo.  

Além disso, o modelo suporta **quantização**, tornando-se um candidato ideal para testes de estresse e avaliação dos limites do hardware local sem exigir infraestrutura de alto custo.

### Janela de Contexto e *Time Behaviour*
O modelo é capaz de lidar com janelas de contexto extremamente longas, de até **128K tokens**.  

Essa característica é central para os testes de **Eficiência de Desempenho**, pois permite submeter o sistema a diferentes volumes e cargas textuais no prompt, possibilitando medir com precisão o:

- **Time to First Token (TTFT)** — tempo necessário para a chegada do primeiro token gerado.

Essa medição fornecerá uma métrica precisa do atributo **Comportamento no Tempo (Time Behaviour)** sob diferentes condições de estresse computacional.

## 2.4.2 Por que o Ollama?

### Isolamento de Ambiente (Offline)
O **Ollama** permite executar modelos de linguagem de forma local e totalmente offline.  

Essa característica é essencial para os testes de **Eficiência de Desempenho**, pois elimina variáveis externas imprevisíveis, tais como:

- Latência de rede;
- Instabilidades de conexão;
- Gargalos de servidores em nuvem.

Com isso, o tempo de resposta medido reflete diretamente o desempenho do hardware local e da aplicação.

### Verificação da Promessa de Agilidade (Portabilidade)
O Ollama é promovido como uma das formas mais simples de implementar e executar modelos abertos localmente.  

O objetivo deste trabalho é validar essa proposta na prática, avaliando e metrificando:

- O esforço de instalação;
- A complexidade de configuração;
- A capacidade de adaptação em diferentes sistemas operacionais;
- A compatibilidade com ambientes conteinerizados via Docker.

Esses testes permitirão validar os parâmetros relacionados à característica de **Portabilidade**.

## 2.4.3 Estruturação da Medição (Abordagem GQM e ISO)
Para garantir que a coleta de dados esteja alinhada aos objetivos do projeto, será utilizado o framework **GQM (Goal-Question-Metric)**.

A definição do propósito analítico estrutura-se da seguinte forma:

- **Objeto de análise:** o modelo Qwen 2.5:3B executado sob o motor do Ollama;
- **Propósito:** compreender e metrificar o comportamento do sistema;
- **Foco:** atributos de qualidade relacionados à Eficiência e Portabilidade;
- **Ponto de vista:** equipe de desenvolvimento e testes;
- **Contexto:** ambiente operacional do software.

As medições realizadas estarão fundamentadas nos elementos de medida definidos pelo relatório técnico **ISO/IEC TR 25021**.[ISO/IEC TR 25021 (SQuaRE – Quality Measure Elements)](https://www.iso.org/standard/35736.html?), entenda mis sobre o modelo na aba [modelo](./modelo.md).

O detalhamento individual das métricas coletadas — como:

- tempo de resposta;
- utilização de recursos;
- adaptabilidade;
- instalabilidade;

bem como as justificativas para suas escolhas, serão apresentados nos tópicos específicos subsequentes.

# Bibliografia

> 1. ISO/IEC. *ISO/IEC TR 25021:2007: Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — Quality measure elements*. 1. ed. Genebra: International Organization for Standardization / International Electrotechnical Commission, 2007.

> 2. RAMOS, Cristiane Soares. *Medição baseada em objetivos: “Determinando o que medir”*. Material da disciplina FGA0278 - Qualidade de Software 1. Faculdade do Gama (FGA), Universidade de Brasília (UnB), 2024.

> 3. QWEN. *Qwen/Qwen2.5-3B-Instruct*. Repositório de modelos Hugging Face, 2024. Disponível em: <https://ollama.com/library/qwen2.5:3b>. Acesso em: 13 maio 2026.

> 4. QWEN TEAM. *Qwen2 Technical Report*. 2024. Disponível em: <https://arxiv.org/abs/2407.10671>. Acesso em: 13 maio 2026.

> 5. OLLAMA INC. *Ollama: The easiest way to build with open models*. Portal oficial de documentação, 2026. Disponível em: <https://ollama.com>. Acesso em: 13 maio 2026.

---

## Histórico de Versão
 
| Versão | Data | Descrição | Autor | Revisor |
|---|---|---|---|---|
| 1.0 | 13/05/2026 | Adição do histórico de versão e revisão do conteúdo | [Renata Quadros](https://github.com/RenataKurzawa) | [Gabriel Alves](https://github.com/GdevAlves) |
| 1.1 | 29/05/2026 | Correções de links e Títulos | [Gabriel Alves](https://github.com/GdevAlves) | [Gabriel Alves](https://github.com/GdevAlves) |