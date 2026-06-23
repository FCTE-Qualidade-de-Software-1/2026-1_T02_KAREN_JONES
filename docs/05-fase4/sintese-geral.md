# 5.3 Síntese Geral

## 5.3.1 Consolidação dos Resultados

Tabela-resumo cruzando todas as métricas com seus critérios e o resultado obtido (aprovado/reprovado):

### Windows

| Característica | ID | Métrica | Critério | Resultado | Veredicto |
|---|---|---|---|---|---|
| Eficiência | ED-1.1 | TTFT (512 tok) | ≤ 5s | 278,68 ms | Aprovado |
| Eficiência | ED-1.2 | TPS (512 tok) | ≤ 5 tokens | 53,2t | Aprovado |
| Eficiência | ED-1.3 | Load time (512 t) | ≤ 30 s | 2,31s | Aprovado |
| Eficiência | ED-2.1 | Consumo de ram | ≤ 6GB | 336.16 MB | Aprovado |
| Eficiência | ED-2.2 | Uso de CPU | ≤ 90% | 0.23% | Aprovado |
| Eficiência | ED-2.3 | Eficiência de recurso | ≤ 0,5 | 704.54 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 256t | ≤ 8,0 | 261.37 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 512t | ≤ 8,0 | 274.87 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 1024t | ≤ 8,0 | 266.08 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 2048t | ≤ 8,0 | 278.35 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 4096t | ≤ 8,0 | 285.17 | Aprovado |
| Eficiência | ED-3.2 | Crescimento KV Cache 512t | ≤ 1MB/t | -172 | Inconclusivo |
| Eficiência | ED-3.2 | Crescimento KV Cache 1024t | ≤ 1MB/t | -62 | Inconclusivo |
| Eficiência | ED-3.2 | Crescimento KV Cache 2048t | ≤ 1MB/t | -31 | Inconclusivo |
| Eficiência | ED-3.2 | Crescimento KV Cache 4096t | ≤ 1MB/t | -21 | Inconclusivo |

### Linux (Zorin)

| Característica | ID | Métrica | Critério | Resultado | Veredicto |
|---|---|---|---|---|---|
| Eficiência | ED-1.1 | TTFT (512 tok) | ≤ 5s | 237,31 ms | Aprovado |
| Eficiência | ED-1.2 | TPS (512 tok) | ≤ 5 tokens | 53,43t | Aprovado |
| Eficiência | ED-1.3 | Load time (512 t) | ≤ 30 s | 1,82s | Aprovado |
| Eficiência | ED-2.1 | Consumo de ram | ≤ 6GB | 57.02 MB | Aprovado |
| Eficiência | ED-2.2 | Uso de CPU | ≤ 90% | 0.18% | Aprovado |
| Eficiência | ED-2.3 | Eficiência de recurso | ≤ 0,5 | 5421.42 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 256t | ≤ 8,0 | 196,95 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 512t | ≤ 8,0 | 196,75 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 1024t | ≤ 8,0 | 203,09 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 2048t | ≤ 8,0 | 218,9 | Aprovado |
| Eficiência | ED-3.1 | Escalonamento de contexto 4096t | ≤ 8,0 | 220,93 | Aprovado |
| Eficiência | ED-3.2 | Crescimento KV Cache 512t | ≤ 1MB/t | 2 | Inconclusivo |
| Eficiência | ED-3.2 | Crescimento KV Cache 1024t | ≤ 1MB/t | 1 | Inconclusivo |
| Eficiência | ED-3.2 | Crescimento KV Cache 2048t | ≤ 1MB/t | 4 | Inconclusivo |
| Eficiência | ED-3.2 | Crescimento KV Cache 4096t | ≤ 1MB/t | 3 | Inconclusivo |

> **Nota:** Acreditamos que o crescimento do KV Cache teve valores inesperados por conta do baixo uso de RAM pelo Ollama + Qwen 2.5 3B, o que fez com que ruídos alterassem a taxa de uso de RAM por tokens, às vezes diminuindo o consumo ao duplicar o número de tokens.

## 5.3.2 Resposta às Decisões Apoiadas (Fase 1 — Tabela 1)

| Decisão (Fase 1) | Resposta baseada nos dados |
|---|---|
| Validação de Hardware: 16 GB de RAM são suficientes? | Aprovado, 16 GB foram mais que o suficiente para requisições com até 4096 tokens. |
| Adoção de SOs: há paridade entre Windows e Linux? | Aprovado, todas as funcionalidades passaram em ambos os SOs, com exceção das inconclusivas pelo uso de RAM muito baixo sofrendo interferência. |
| Configuração de Modelo: o limite de contexto precisa de ajuste? | Aprovado, o TTFT se manteve dentro do esperado com o aumento do número de tokens. |
| Agilidade de Deploy: a instalação é simples para qualquer usuário? | Aprovado, a instalação é muito simples e robusta, demonstrada pela taxa de sucesso de 100% e tempo médio de instalação extremamente baixo (menos de 30 segundos) em ambos os ambientes. |

## 5.3.3 Conclusão

Recomendação final: O Ollama com Qwen 2.5 3B é altamente viável para o cenário acadêmico e offline proposto (estudante com hardware básico), operando dentro dos critérios de aceitação estabelecidos para tempo de resposta e consumo de memória RAM. A principal ressalva refere-se ao desvio de desempenho de inferência em Windows sem aceleração por GPU, que se mostrou substancialmente mais lento do que em Linux (Zorin OS), embora ainda dentro dos limites aceitáveis.

## 5.3.4 Ameaças à Validade

- **Variação de hardware:** diferentes especificações de CPU podem influenciar os resultados.
- **Número limitado de repetições (5 por métrica):** pode não capturar toda a variabilidade.
- **Ausência de GPU:** os resultados refletem exclusivamente o desempenho em CPU.
- **Versão específica do Ollama:** os resultados podem diferir em versões futuras.
- **Ambiente controlado:** condições reais de uso podem introduzir variáveis não consideradas.

## 5.4 Tabela de Contribuição — Fase 4

| Nome | Contribuição | Participação |
|---|---|---|
| Gabriel Alves | Organização e estruturação dos resultados (autor principal) | 16,66% |
| Giovana Barbosa | Pesquisa e redação | 16,66% |
| Johnnatan Salles | Pesquisa e redação | 16,66% |
| Luiza da Silva | Pesquisa e redação | 16,66% |
| Matheus Pinheiro | Scripts de desempenho e organização de dados | 16,66% |
| Renata Quadros | Pesquisa e redação | 16,66% |
| **Total** | | **100%** |

## Referências Bibliográficas

> 1. ISO/IEC. *ISO/IEC 25010:2011 – Systems and software Quality Requirements and Evaluation (SQuaRE) – Quality model*. Geneva: ISO, 2011.
>
> 2. ISO/IEC. *ISO/IEC TR 25021:2007 – SQuaRE – Quality measure elements*. Geneva: ISO, 2007.
>
> 3. RAMOS, Cristiane Soares. *Medição baseada em objetivos*. Material FGA0278 – Qualidade de Software 1. FGA/UnB, 2024.
>
> 4. QWEN TEAM. *Qwen2 Technical Report*. 2024. Disponível em: <https://arxiv.org/abs/2407.10671>.
>
> 5. OLLAMA INC. *Ollama – The easiest way to build with open models*. Disponível em: <https://ollama.com>. Acesso em: maio 2026.
>
> 6. FENTON, Norman; BIEMAN, James. *Software Metrics: A Rigorous and Practical Approach*. 3. ed. CRC Press, 2015.
>
> 7. PSUTIL. *Cross-platform lib for process and system monitoring in Python*. Disponível em: <https://psutil.readthedocs.io>.
>
> 8. GOOGLE. *Firebase Crashlytics: Métricas de crash-free*. Disponível em: <https://firebase.google.com/docs/crashlytics/crash-free-metrics>.
>
> 9. RAMOS, Cristiane Soares. *Medição baseada em objetivos: "Determinando o que medir"*. Material da disciplina FGA0315 — Qualidade de Software 1. Faculdade do Gama (FGA), Universidade de Brasília (UnB), 2026.

## Histórico de Versão

| Versão | Data | Descrição | Autor | Revisor |
|---|---|---|---|---|
| 1.0 | 12/06/2026 | Criação do documento | [Gabriel](https://github.com/GDevAlves) | [Renata Quadros](https://github.com/RenataKurzawa) |
| 1.1 | 23/06/2026 | Preenchimento da consolidação dos resultados, respostas e bibliografia | [Johnnatan Salles](https://github.com/jsalless) | [Equipe](https://github.com/GDveAlves) |