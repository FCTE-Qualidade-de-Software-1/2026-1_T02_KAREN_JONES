# Plano de Avaliação — Portabilidade

## 1. Introdução

Este documento especifica como serão implementadas e executadas as métricas definidas na metodologia GQM da Fase 2 para avaliar a **Portabilidade** do Ollama.

O foco está em duas subcaracterísticas conforme ISO/IEC 25010:

- **Adaptabilidade**: capacidade de operar em diferentes sistemas operacionais
- **Instalabilidade**: facilidade de instalação e desinstalação


## 2. Métricas a Serem Implementadas

| ID | Métrica | Subcaracterística | Descrição |
|----|---------|-------------------|-----------|
| PO-1.1 | Taxa de Execuções Sem Falha entre Plataformas | Adaptabilidade | Proporção de execuções bem-sucedidas em todas as plataformas |
| PO-1.2 | Desvio de Desempenho de Inferência entre Plataformas | Adaptabilidade | Variação do tempo médio de inferência entre plataformas |
| PO-2.1 | Taxa de Sucesso na Instalação | Instalabilidade | Proporção de instalações (runtime + modelo) bem-sucedidas |
| PO-2.2 | Taxa de Sucesso na Desinstalação | Instalabilidade | Proporção de desinstalações que removem o software e o modelo completamente |
| PO-3.1 | Taxa de Sucesso de Instalação por Ambiente | Instalabilidade | Proporção de instalações bem-sucedidas em cada ambiente específico |
| PO-3.2 | Desvio Relativo de Sucesso entre Ambientes | Instalabilidade | Consistência da taxa de sucesso de instalação entre os ambientes testados |
| PO-3.3 | Tempo de Instalação e Tipos de Falha por Ambiente | Instalabilidade | Variação do tempo de instalação e taxa de falhas específicas por ambiente |

## 3. Ambiente de Teste

### 3.1 Hardware

| Componente | Especificação |
|------------|---------------|
| Processador | Intel Core i5 (8 núcleos) |
| Memória RAM | 16 GB DDR5 |
| Armazenamento | SSD 512 GB |
| GPU | Nenhuma (CPU-only) |

### 3.2 Sistemas Operacionais

| Ambiente | Sistema Operacional | Método |
|----------|---------------------|--------|
| Ambiente A | Windows 11 (64 bits) | Instalação nativa |
| Ambiente B | Zorin OS 18.1 Core | Instalação nativa |

### 3.3 Ferramentas

| Ferramenta | Finalidade |
|------------|------------|
| PowerShell 7+ | Execução de scripts no Windows |
| Bash | Execução de scripts no Linux |
| Cronômetro digital | Medição manual de tempo de instalação |
| Gravação de tela | Evidência do processo de instalação |


## 4. Instrumentos de Medição

### 4.1 Medição de Instalabilidade

**Método de Instalação - Windows**:
```powershell
# Comando oficial do Ollama para Windows
irm https://ollama.com/install.ps1 | iex
```

### Método de Instalação - Linux

```bash
# Comando oficial do Ollama para Linux
curl -fsSL https://ollama.com/install.sh | sh
```

### Dados Coletados

* Timestamp de início e fim da instalação;
* Status final (sucesso/falha);
* Mensagens de erro (se houver);
* Verificação pós-instalação:

```bash
ollama --version
```


### 4.2 Medição de Desinstalação

### Windows

* Verificar remoção via Painel de Controle ou comando;
* Confirmar exclusão de arquivos em `%USERPROFILE%\.ollama`.

### Linux

* Executar script de desinstalação ou remoção manual;
* Confirmar exclusão de arquivos em `~/.ollama`.


### 4.3 Medição de Adaptabilidade

### Método

Executar uma bateria de testes funcionais idêntica em ambos os ambientes:

1. Iniciar o servidor Ollama;
2. Baixar o modelo Qwen 2.5 3B;
3. Executar scripts python da fase de eficiência para inferência;
4. Capturar o tempo médio de inferência;
5. Registrar falhas funcionais durante as execuções.


## 5. Procedimento de Coleta

### 5.1. Perfil do Avaliador

Qualquer membro da equipe pode executar o procedimento, independentemente de experiência prévia com Ollama. As instruções são autocontidas e não requerem conhecimento técnico além de:

- Saber abrir terminal (PowerShell no Windows, Bash no Linux)
- Saber copiar e colar comandos
- Saber operar cronômetro e gravador de tela

### 5.2. Ferramentas de Apoio

| Ferramenta | Sistema | Finalidade | Configuração |
|------------|---------|------------|--------------|
| Script Python | Windows: PowerShell 7+ / Linux: Bash | Execução de comandos | Fonte legível para captura em prints |

### 5.3. Definições Operacionais

| Termo | Definição Exata |
|-------|-----------------|
| **Início da instalação** | Definido em Script python |
| **Fim da instalação** | Definido em Script python |
| **Instalação bem-sucedida** | `ollama --version` retorna string no formato `ollama version X.Y.Z` sem mensagem de erro |
| **Desinstalação completa** | O comando `ollama --version` retorna "comando não encontrado" ou equivalente E o diretório `~/.ollama` (Linux) ou `%USERPROFILE%\.ollama` (Windows) não existe ou está vazio |
| **Arquivo residual** | Qualquer arquivo ou pasta remanescente nos diretórios mencionados após desinstalação |

### 5.4. Protocolo Passo a Passo

# 5. Procedimento de Coleta

## Passo 1: Preparação

* Preparar máquina de teste com Windows 11;
* Preparar máquina de teste com Zorin OS 18.1 Core;
* Preparar máquina de teste com Windows 11;
* Preparar máquina de teste com Zorin OS 18.1 Core;
* Documentar o estado inicial do sistema (espaço em disco, processos em execução);
* Preparar checklist de verificação pós-instalação.


## Passo 2: Testes de Instalabilidade

Para cada ambiente, repetir o procedimento **10 vezes**:

1. Garantir que o Ollama não está instalado;
2. Iniciar o cronômetro;
3. Executar o comando de instalação;
4. Registrar conclusão ou erro;
5. Parar o cronômetro;
6. Verificar instalação:

```bash
ollama --version
```

7. Proceder à desinstalação completa;
8. Verificar remoção de arquivos residuais.

### Planilha de Registro

```csv
ambiente,tentativa,tempo_instalacao_s,status_instalacao,tempo_desinstalacao_s,status_desinstalacao,arquivos_residuais
```

## Passo 3: Testes de Adaptabilidade

1. Instalar o Ollama em ambos os ambientes;
2. Baixar o modelo:

```bash
ollama pull qwen2.5:3b
```

3. Executar o script de testes funcionais padronizado;
4. Registrar resultados comparativos.


## Passo 4: Consolidação

* Calcular taxas de sucesso;
* Comparar tempos médios entre ambientes;
* Identificar diferenças funcionais ou de desempenho.


# 6. Critérios de Aceitação

Conforme as hipóteses definidas na Fase 2:

| Métrica | Critério de Aceitação | Referência Fase 2 |
| --- | --- | --- |
| PO-1.1 Taxa de Execuções Sem Falha | ≥ 99,0% de execuções bem-sucedidas em todas as plataformas | Métrica 1.1 |
| PO-1.2 Desvio de Desempenho de Inferência | ≤ 20% de variação entre plataformas | Métrica 1.2 |
| PO-2.1 Taxa de Sucesso na Instalação | ≥ 95% das tentativas bem-sucedidas por plataforma | Métrica 2.1 |
| PO-2.2 Taxa de Sucesso na Desinstalação | ≥ 90% das tentativas resultam em remoção completa do sistema | Métrica 2.2 |
| PO-3.1 Taxa de Sucesso de Instalação por Ambiente | ≥ 95% de sucesso em cada ambiente testado | Métrica 3.1 |
| PO-3.2 Desvio Relativo de Sucesso entre Ambientes | ≤ 5% de variação entre quaisquer dois ambientes | Métrica 3.2 |
| PO-3.3 Tempo de Instalação e Tipos de Falha | Variação de tempo ≤ 15% e nenhuma falha com taxa > 2% | Métrica 3.3 |

# 7. Localização dos Dados

| Artefato                   | Caminho                                              | Descrição                        |
| -------------------------- | ---------------------------------------------------- | -------------------------------- |
| Planilha de instalação     | link | Registro de tempos e status      |
| Planilha de adaptabilidade | link | Comparativo entre SOs            |
| Gravações de tela          | link                          | Vídeos do processo de instalação |
| Logs de erro               | link`                         | Mensagens de erro capturadas     |
| Checklist de verificação   | link`                                 | Verificações pós-instalação      |

---


# Bibliografia

> 1. ISO/IEC. *ISO/IEC TR 25021:2007: Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — Quality measure elements*. 1. ed. Genebra: International Organization for Standardization / International Electrotechnical Commission, 2007.

> 2. RAMOS, Cristiane Soares. *Medição baseada em objetivos: “Determinando o que medir”*. Material da disciplina FGA0278 - Qualidade de Software 1. Faculdade do Gama (FGA), Universidade de Brasília (UnB), 2024.

> 3. QWEN. *Qwen/Qwen2.5-3B-Instruct*. Repositório de modelos Hugging Face, 2024. Disponível em: <https://ollama.com/library/qwen2.5:3b>. Acesso em: 13 maio 2026.

> 4. QWEN TEAM. *Qwen2 Technical Report*. 2024. Disponível em: <https://arxiv.org/abs/2407.10671>. Acesso em: 13 maio 2026.

> 5. OLLAMA INC. *Ollama: The easiest way to build with open models*. Portal oficial de documentação, 2026. Disponível em: <https://ollama.com>. Acesso em: 13 maio 2026.


## Histórico de Versão
 
| Versão | Data | Descrição | Autor | Revisor |
|---|---|---|---|---|
| 1.0 | 04/06/2026 | Criação do documento | [Renata Quadros](https://github.com/RenataKurzawa) |[Giovana Barbosa](https://github.com/gio221) |
| 1.1 | 12/06/2026 | Alinhamento de métricas da fase 2 | [Gabriel Alves](https://github.com/GDveAlves) | [Matheus Pinheiro](https://github.com/Matheus-06)|
| 1.2 | 12/06/2026 | Atualização | [Renata Quadros](https://github.com/RenataKurzawa) |[Giovana Barbosa](https://github.com/gio221) |