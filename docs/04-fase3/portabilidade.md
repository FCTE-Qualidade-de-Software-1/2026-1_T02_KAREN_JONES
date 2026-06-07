# Plano de Avaliação — Portabilidade

## 1. Introdução

Este documento especifica como serão implementadas e executadas as métricas definidas na metodologia GQM da Fase 2 para avaliar a **Portabilidade** do Ollama.

O foco está em duas subcaracterísticas conforme ISO/IEC 25010:

- **Adaptabilidade**: capacidade de operar em diferentes sistemas operacionais
- **Instalabilidade**: facilidade de instalação e desinstalação

---

## 2. Métricas a Serem Implementadas

| ID | Métrica | Subcaracterística | Descrição |
|----|---------|-------------------|-----------|
| PO-1.1 | Taxa de Sucesso na Instalação | Instalabilidade | Proporção de instalações bem-sucedidas em 10 tentativas |
| PO-1.2 | Tempo Médio de Instalação | Instalabilidade | Tempo decorrido do início ao fim do processo de instalação |
| PO-1.3 | Taxa de Sucesso na Desinstalação | Instalabilidade | Proporção de desinstalações que removem completamente o software |
| PO-2.1 | Paridade Funcional entre SOs | Adaptabilidade | Proporção de funcionalidades que operam igualmente em Windows e Linux |
| PO-2.2 | Desvio de Desempenho entre SOs | Adaptabilidade | Diferença percentual no TTFT entre Windows e Linux |
| PO-2.3 | Taxa de Falhas por Ambiente | Adaptabilidade | Proporção de falhas durante execução em cada SO |

---

## 3. Ambiente de Teste

### 3.1 Hardware

| Componente | Especificação |
|------------|---------------|
| Processador | Intel Core i5 (4 núcleos) ou equivalente |
| Memória RAM | 8 GB DDR4 |
| Armazenamento | SSD 256 GB |
| GPU | Nenhuma |

### 3.2 Sistemas Operacionais

| Ambiente | Sistema Operacional | Método |
|----------|---------------------|--------|
| Ambiente A | Windows 11 (64 bits) | Instalação nativa |
| Ambiente B | Ubuntu 22.04 LTS | Instalação nativa ou via WSL2 |

### 3.3 Ferramentas

| Ferramenta | Finalidade |
|------------|------------|
| PowerShell 7+ | Execução de scripts no Windows |
| Bash | Execução de scripts no Linux |
| Cronômetro digital | Medição manual de tempo de instalação |
| Gravação de tela | Evidência do processo de instalação |

---

## 4. Instrumentos de Medição

### 4.1 Medição de Instalabilidade

**Método de Instalação - Windows**:
```powershell
# Comando oficial do Ollama para Windows
irm get.ollama.ai | iex
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

---

## 4.2 Medição de Desinstalação

### Windows

* Verificar remoção via Painel de Controle ou comando;
* Confirmar exclusão de arquivos em `%USERPROFILE%\.ollama`.

### Linux

* Executar script de desinstalação ou remoção manual;
* Confirmar exclusão de arquivos em `~/.ollama`.

---

## 4.3 Medição de Adaptabilidade

### Método

Executar uma bateria de testes funcionais idêntica em ambos os ambientes:

1. Iniciar o servidor Ollama;
2. Baixar o modelo Qwen 2.5 3B;
3. Enviar 5 prompts de teste padronizados;
4. Verificar as respostas geradas;
5. Registrar o TTFT (*Time To First Token*) e eventuais erros.

---

# 5. Procedimento de Coleta

## Passo 1: Preparação

* Preparar máquina de teste com Windows 11 limpo (ou máquina virtual);
* Preparar máquina de teste com Ubuntu 22.04 limpo (ou VM/WSL2);
* Documentar o estado inicial do sistema (espaço em disco, processos em execução);
* Preparar checklist de verificação pós-instalação.

---

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

---

## Passo 3: Testes de Adaptabilidade

1. Instalar o Ollama em ambos os ambientes;
2. Baixar o modelo:

```bash
ollama pull qwen2.5:3b
```

3. Executar o script de testes funcionais padronizado;
4. Registrar resultados comparativos.

---

## Passo 4: Consolidação

* Calcular taxas de sucesso;
* Comparar tempos médios entre ambientes;
* Identificar diferenças funcionais ou de desempenho.

---

# 6. Critérios de Aceitação

| Métrica                        | Critério de Aceitação                               |
| ------------------------------ | --------------------------------------------------- |
| Taxa de Sucesso na Instalação  | ≥ 90% em ambos os SOs                               |
| Tempo de Instalação            | ≤ 5 minutos                                         |
| Paridade Funcional             | 100% das funcionalidades testadas operam igualmente |
| Desvio de Desempenho entre SOs | ≤ 20%                                               |

---

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