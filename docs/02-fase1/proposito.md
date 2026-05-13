# 2.1 Propósito da Avaliação

# Propósito da avaliação e uso pretendido

O objetivo desta seção é descrever as razões para a realização da avaliação de qualidade, identificando os interessados e como os dados obtidos influenciarão as decisões sobre a stack tecnológica escolhida. Será dividido em: Por que avaliar?  ; Para quem avaliar? ; Como os resultados serão utilizados ?

Toda a avaliação será feita sob as especificações da norma **ISO/IEC 25010 (SQuaRE)**, focando nas características de **portabilidade** e **eficiência de desempenho**.

## Por que avaliar ?

Atualmente o acesso à Inteligencia Artificial se esbarra em dois principais obstáculos: a exigência de hardware de alto custo e a dependência de conectividade estável. 

Tendo em vista os estudantes, pesquisadores e quaisquer pessoas que utilizam a inteligencia artificial que se localizam em regiões com a infraestrutura limitada precisam de ferramentas que garantam a funcionalidade offline e privacidade.

O Ollama (executando o modelo Qwen 2.5 3B, versão v0.9.0) tem uma solução para esse cenário. Porém, é fundamental validar de essa promessa de "agilidade" e "execução local" se sustenta em hardware modesto, como um com 8GB de RAM e sem GPU dedicada. A avaliação desse trabalho busca medir se o sistema é realmente viável e consistente em diferentes sistemas operacionais, focando na portabilidade e também medir a eficiência e desempenho.

## Para quem avaliar ?

A avaliação e resultados se destinam principalmente a:

**Estudantes e Pesquisadores**: Para decidir se o Ollama é uma alternativa viável em máquinas básicas.

**Comunidade de Software Acadêmico**: Para validar o Qwen 2.5 3B como um modelo eficiente para tarefas de resumo e escrita local.

**Decisores Técnicos**: Os dados servirão de base para recomendar (ou não) a adoção deste software como padrão para inclusão digital em áreas remotas.


### Como os resultados serão utilizados?

Os resultados serão utilizados para tomar as seguintes decisões:

**Validação de Hardware**: Decidir se 8GB de RAM são suficientes para rodar o Qwen 2.5 3B sem comprometer a estabilidade do sistema operacional.

**Adoção de Sistemas Operacionais**: Determinar se há paridade de desempenho entre Windows e Linux.

**Configuração de Modelo**: Decidir se o limite de contexto de tokens precisa ser ajustado para garantir que o tempo de chegada do primeiro token (TTFT) não ultrapasse um limite aceitável para o usuário.

**Agilidade de Deploy**: Validar se o método de instalação atual do Ollama é simples o suficiente para ser recomendado a todos os tipos de usuários.

### Cenário de Avaliação

Foi definido o seguinte cénario para avaliação:

>"Uma estudante universitária com acesso instável à internet e um notebook básico (Windows 11, 8GB RAM, sem GPU) precisa de um assistente para estudos. 
>Um colega utiliza a mesma ferramenta no Linux (Ubuntu). Eles buscam uma solução gratuita, privada e offline. O foco da nossa avaliação é verificar se o Qwen 2.5 3B via Ollama entrega um tempo de resposta aceitável nesse hardware e se a experiência de instalação e adaptação é equivalente entre os dois sistemas operacionais."


## Escopo da Avaliação (ISO/IEC 25021)

As características centrais da norma aplicada a este trabalho é dtalhada abaixo. O foco será exclusivamente em Eficiência de desempenho (especificamente o comportamento temporal) e Portabilidade. Especificamos mais na aba de [Modelo de Qualidade e Escopo](https://fcte-qualidade-de-software-1.github.io/2026-1_T02_KAREN_JONES/02-fase1/modelo/).

### Eficiência de desempenho
Não avaliaremos a "Eficiência" genérica (qualidade em uso), mas sim a capacidade técnica do modelo em gerenciar recursos e tempo:

**Comportamento Temporal** : Focaremos no Time to First Token (TTFT). Em modelos locais, o tempo que o sistema leva para começar a responder é o principal indicador de usabilidade em máquinas sem GPU.

**Utilização de recursos** : Focaremos em medir se os recursos (RAM/CPU) são otimizados para garantir o desempenho adequado no cenário de 8GB de RAM.

**Capacidade** : Avaliaremos como o contexto de tokens impacta a velocidade de processamento, ignorando a capacidade multilíngue por não ser o foco da estabilidade local.

### Portabilidade
Vamos verificar se a "agilidade" prometida pelo Ollama se traduz na prática:

**Adaptabilidade**: O sistema mantém o desempenho ao alternar entre o Windows (via PowerShell) e o Linux?

**Instalabilidade**: O comando ```install.ps1 | iex``` realmente facilita o acesso para um usuário leigo ou apresenta barreiras em hardware limitado?


# Bibliográfia

> 1. ISO/IEC. *ISO/IEC TR 25021:2007: Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — Quality measure elements*. 1. ed. Genebra: International Organization for Standardization / International Electrotechnical Commission, 2007.

> 2. RAMOS, Cristiane Soares. *Medição baseada em objetivos: “Determinando o que medir”*. Material da disciplina FGA0278 - Qualidade de Software 1. Faculdade do Gama (FGA), Universidade de Brasília (UnB), 2024.

> 3. QWEN. *Qwen/Qwen2.5-3B-Instruct*. Repositório de modelos Hugging Face, 2024. Disponível em: <https://ollama.com/library/qwen2.5:3b>. Acesso em: 13 maio 2026.

## Histórico de Versão
 
| Versão | Data | Descrição | Autor | Revisor |
|---|---|---|---|---|
| 1.0 | 13/05/2026 | Criação do próposito da avaliação | [Renata Quadros](https://github.com/RenataKurzawa) | — |
