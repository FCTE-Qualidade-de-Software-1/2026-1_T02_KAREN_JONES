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
| OBS Studio 30.0+ | Windows/Linux | Gravação de tela | Resolução 1920×1080, 30fps, codec H.264 |
| Cronômetro do smartphone | — | Medição de tempo | Modo lap/split para registrar marcos |
| Terminal nativo | Windows: PowerShell 7+ / Linux: Bash | Execução de comandos | Fonte legível para captura em vídeo |

### 5.3. Definições Operacionais

| Termo | Definição Exata |
|-------|-----------------|
| **Início da instalação** | Momento em que a tecla Enter é pressionada após digitar/colar o comando de instalação |
| **Fim da instalação** | Momento em que o terminal exibe o prompt de comando novamente (cursor piscando, pronto para novo comando) E o comando `ollama --version` retorna uma versão válida |
| **Instalação bem-sucedida** | `ollama --version` retorna string no formato `ollama version X.Y.Z` sem mensagem de erro |
| **Desinstalação completa** | O comando `ollama --version` retorna "comando não encontrado" ou equivalente E o diretório `~/.ollama` (Linux) ou `%USERPROFILE%\.ollama` (Windows) não existe ou está vazio |
| **Arquivo residual** | Qualquer arquivo ou pasta remanescente nos diretórios mencionados após desinstalação |

### 5.4. Protocolo Passo a Passo

#### Passo 0: Preparação (executar uma vez por sessão)

1. Reiniciar o sistema operacional
2. Fechar todos os aplicativos exceto terminal e OBS Studio
3. Verificar espaço em disco disponível (mínimo 10 GB livres)
4. Abrir OBS Studio e configurar captura de tela cheia
5. Preparar cronômetro do smartphone em modo lap
6. Criar pasta para armazenar evidências do dia: `~/evidencias-portabilidade/YYYY-MM-DD/`

#### Passo 1: Pré-verificação (a cada tentativa)

1. Confirmar que Ollama **não** está instalado:

```bash
   # Linux
   ollama --version
   # Esperado: "command not found" ou equivalente
   # Windows (PowerShell)
   ollama --version
   # Esperado: erro de comando não reconhecido
```

2. Confirmar que diretório de dados não existe: 

```bash
 # Linux
ls -la ~/.ollama
# Esperado: "No such file or directory"
# Windows (PowerShell)
Test-Path "$env:USERPROFILE\.ollama"
# Esperado: False
```

### Passo 2: Instalação

1. Iniciar gravação no OBS Studio (Ctrl+Shift+R ou botão)
2. No terminal, digitar (não colar ainda) o comando de instalação
3. Zerar cronômetro e posicionar dedo sobre Enter
4. Pressionar Enter e iniciar cronômetro simultaneamente
5. Aguardar conclusão sem interagir com o sistema
6. Quando o prompt reaparecer, pressionar lap no cronômetro
7. Executar verificação:
   
```bash
   ollama --version
```

8. Parar cronômetro após resultado da verificação
9.  Parar gravação no OBS Studio
10. Registrar na planilha:
- Tempo de instalação (lap 1)
- Status (sucesso/falha)
- Mensagem de erro (se houver, copiar texto completo)
- Versão retornada (se sucesso)

### Passo 3: Desinstalação
1. Iniciar nova gravação
2. Zerar e iniciar cronômetro
3. Executar desinstalação: Linux: 
```bash
sudo rm -rf /usr/local/bin/ollama
sudo rm -rf /usr/local/lib/ollama
rm -rf ~/.ollama
sudo systemctl stop ollama 2>/dev/null
sudo systemctl disable ollama 2>/dev/null
sudo rm /etc/systemd/system/ollama.service 2>/dev/null
```

Windows (PowerShell como Administrador):

```bash
# Parar processo se estiver rodando
Stop-Process -Name "ollama" -Force -ErrorAction SilentlyContinue
# Remover via winget (se instalado assim) ou manualmente
winget uninstall Ollama.Ollama --silent
# Remover diretório de dados
Remove-Item -Recurse -Force "$env:USERPROFILE\.ollama" -ErrorAction SilentlyContinue
# Remover do PATH se necessário (verificar manualmente)
```
4. Pressionar lap quando comandos terminarem
5. Verificar remoção:

```bash
ollama --version
# Esperado: comando não encontrado
```

6. Verificar diretórios:

```bash
# Linux
ls -la ~/.ollama
# Windows
Test-Path "$env:USERPROFILE\.ollama"
```

7. Parar cronômetro e gravação
Registrar na planilha:
- Tempo de desinstalação
- Status (completa/parcial/falha)
- Arquivos residuais encontrados (listar)

### Passo 4: Repetir
Repetir Passos 1–3 por 10 vezes em cada ambiente, totalizando 20 execuções.

### 5.5. Planilha de Registro
Criar arquivo CSV com o seguinte cabeçalho:

```bash
ambiente,tentativa,data_hora,tempo_instalacao_s,status_instalacao,versao_instalada,erro_instalacao,tempo_desinstalacao_s,status_desinstalacao,arquivos_residuais,observacoes,video_arquivo
```

Exemplo de linha preenchida:

```bash
Windows 11,1,2026-06-17T10:15:00,45.3,sucesso,0.9.0,,38.1,completa,nenhum,,evidencias-portabilidade/2026-06-17/win11_tentativa01.mp4
```

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