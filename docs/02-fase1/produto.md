# 2.3 Descrição do Produto

O objetivo desta página é fornecer uma visão geral do software em avaliação e apresentar suas principais características técnicas e funcionais.
 
---

![](../img/ollamaImage.png)
 
## Informações Básicas
 
- **Nome do produto**: Ollama
- **Versão do produto**: v0.9.0 (versão mais recente estável, maio de 2026)
- **Aplicação do produto**: Servidor de inferência local para Modelos de Linguagem de Grande Escala (LLMs)
- **Repositório do Código Principal**: [GitHub — ollama/ollama](https://github.com/ollama/ollama)
- **Licença do Produto**: MIT License
- **Linguagem de implementação**: Go (Golang)
- **Site oficial**: [https://ollama.com](https://ollama.com)
- **Documentação oficial**: [https://docs.ollama.com](https://docs.ollama.com)
---
 
## Sobre o Ollama
 
### O que é?
 
O **Ollama** é uma ferramenta de código aberto que permite executar Modelos de Linguagem de Grande Escala (LLMs) diretamente na máquina local do usuário, sem depender de serviços em nuvem ou chaves de API externas. Com um único comando no terminal, é possível baixar e executar modelos como Llama 3, Mistral, Gemma, DeepSeek, Qwen, entre mais de 100 outros disponíveis na biblioteca oficial.
 
O projeto foi criado para **remover as barreiras técnicas** que historicamente tornavam o uso de LLMs complexo: configuração de ambientes, gerenciamento de pesos de modelos, aceleração por GPU e compatibilidade de hardware. O Ollama abstrai toda essa complexidade, oferecendo uma interface simples tanto para uso via linha de comando quanto para integração via API REST.
 
### Arquitetura técnica
 
O Ollama utiliza uma arquitetura **cliente-servidor**:
 
- O **cliente** é a interface de linha de comando (CLI) pela qual o usuário digita comandos.
- O **servidor** roda em segundo plano, sendo responsável por gerenciar modelos e processar requisições de inferência.
Como motor de inferência, o Ollama utiliza internamente o **llama.cpp**, otimizado para rodar modelos em hardware convencional, mesmo sem GPU dedicada. Quando uma GPU está disponível, o Ollama a detecta automaticamente e a utiliza para acelerar as respostas — com suporte a **NVIDIA (CUDA)**, **AMD (ROCm)** e **Apple Silicon (Metal)**. Na ausência de GPU, o processamento recai sobre a CPU.
 
A API REST embutida escuta por padrão na porta **11434** e é compatível com o formato da API da OpenAI, permitindo que aplicações já integradas com serviços em nuvem sejam redirecionadas para uma instância local com mínimas alterações de código.
 
Os modelos são armazenados localmente em `$HOME/.ollama/models` e gerenciados por um sistema de conteúdo endereçável, similar ao funcionamento de contêineres Docker.
 
---
 
## Sobre o uso do Ollama
 
- **Funções do produto**: execução local de LLMs, gerenciamento de modelos, inferência de texto, geração de embeddings, suporte a modelos multimodais (texto + imagem), integração via API REST
- **Classificação do produto**: AI Inference Server, Open-Source, Local-First
- **Público-alvo**: desenvolvedores de software, pesquisadores, cientistas de dados, profissionais de TI, entusiastas de IA
- **Ambientes de uso**: desenvolvimento local, pipelines de automação, aplicações empresariais com requisitos de privacidade, ambientes educacionais, pesquisa acadêmica
- **Dispositivos**: Desktop, Notebook (com suporte a macOS, Windows e Linux)
- **Conectividade**: funciona **completamente offline** para execução e inferência; utiliza internet apenas para baixar modelos do repositório oficial (`registry.ollama.ai`)
- **Suporte técnico**: comunidade ativa via GitHub Issues, Discord oficial, e documentação em [docs.ollama.com](https://docs.ollama.com); sem suporte comercial oficial para a versão local
### Modelos disponíveis
 
A biblioteca oficial do Ollama conta com mais de **100 modelos prontos para uso**, organizados nas seguintes categorias:
 
| Categoria | Exemplos de modelos |
|---|---|
| Uso geral / chat | Llama 3.3, Mistral, Gemma 3, Qwen 3 |
| Geração de código | Code Llama, DeepSeek Coder, Phi-4 |
| Raciocínio | DeepSeek-R1, QwQ |
| Multimodal (texto + imagem) | LLaVA, Llama 3.2 Vision, Qwen-VL |
| Embeddings | nomic-embed-text, mxbai-embed-large |
 
### Integrações e ecossistema
 
O Ollama possui um ecossistema amplo de integrações com ferramentas populares do mercado:
 
- **Interfaces gráficas**: Open WebUI, Enchanted, Ollama App
- **IDEs e editores de código**: Continue (VS Code), Cline, Void
- **Frameworks de IA**: LangChain, LlamaIndex
- **Agentes de codificação**: Claude Code, GitHub Copilot CLI, OpenCode
- **SDKs oficiais**: Python (`ollama-python`) e JavaScript/TypeScript (`ollama-js`)
### Planos e preços
 
| Modalidade | Custo | Características |
|---|---|---|
| **Local (padrão)** | Gratuito, sem limite | Execução offline, sem conta necessária, privacidade total |
| **Cloud Free** | Gratuito com conta | Acesso a modelos maiores em infraestrutura remota |
| **Cloud Pro** | US$ 20/mês | 3 modelos simultâneos em nuvem, maior volume de uso |
| **Cloud Max** | US$ 100/mês | 10 modelos simultâneos, uso intensivo |
 
> **Importante**: a funcionalidade local é **completamente gratuita e sem restrições**. A camada de nuvem é opcional e foi introduzida em setembro de 2025.
 
---
 
## Como as ODS se relacionam com o Ollama
 
**ODS 4 – Educação de Qualidade**
 
O Ollama é uma ferramenta gratuita e de código aberto que democratiza o acesso a tecnologias de inteligência artificial avançadas. Ao eliminar a necessidade de chaves de API pagas e de conexão constante com a internet, ele viabiliza que estudantes, professores e pesquisadores — inclusive em contextos de menor infraestrutura — possam estudar, experimentar e desenvolver com LLMs de ponta. Isso contribui diretamente para a redução das barreiras de acesso à educação tecnológica e para a formação de profissionais qualificados em IA, alinhando-se ao ODS 4, que busca assegurar educação inclusiva, equitativa e de qualidade para todos.
 
**ODS 9 – Indústria, Inovação e Infraestrutura**
 
O Ollama representa um avanço significativo na democratização da infraestrutura de IA. Ao permitir que organizações de qualquer porte executem modelos sofisticados em hardware comum, sem custos de API ou dependência de grandes provedores de nuvem, o software fomenta a inovação descentralizada. Pequenas empresas, startups e times independentes passam a ter acesso à mesma capacidade técnica anteriormente restrita a grandes corporações, alinhando-se ao ODS 9, que busca construir infraestruturas resilientes, promover a industrialização inclusiva e fomentar a inovação.
 
**ODS 10 – Redução das Desigualdades**
 
A filosofia *local-first* do Ollama contribui para reduzir a desigualdade no acesso à IA. Modelos de linguagem poderosos, antes acessíveis apenas mediante pagamento por uso a empresas como OpenAI e Anthropic, tornam-se disponíveis gratuitamente a qualquer pessoa com um computador convencional. Isso é especialmente relevante em países em desenvolvimento, onde os custos de acesso a APIs externas podem ser proibitivos. O Ollama, portanto, alinha-se ao ODS 10 ao ampliar o acesso equitativo a tecnologias transformadoras.
 
---
 
## Bibliografia
 
> 1. OLLAMA. *Ollama — The easiest way to build with open models*. Disponível em: <https://ollama.com>. Acesso em: 11 maio 2026.
 
> 2. OLLAMA. *Ollama — Repositório oficial*. GitHub, 2026. Disponível em: <https://github.com/ollama/ollama>. Acesso em: 11 maio 2026.
 
> 3. OLLAMA. *Documentação oficial do Ollama*. Disponível em: <https://docs.ollama.com>. Acesso em: 11 maio 2026.
 
> 4. OLLAMA. *Biblioteca de modelos do Ollama*. Disponível em: <https://ollama.com/library>. Acesso em: 11 maio 2026.
 
> 5. TOOLCHASE. Ollama Review 2026 — Pricing, Features & Alternatives. **ToolChase**, 2026. Disponível em: <https://toolchase.com/tool/ollama/>. Acesso em: 11 maio 2026.
 
> 6. INFRALOVERS. Ollama in 2025: Major Updates Transform Local AI Experience. **Infralovers**, ago. 2025. Disponível em: <https://www.infralovers.com/blog/2025-08-13-ollama-2025-updates/>. Acesso em: 11 maio 2026.
 
> 7. SKYWORK AI. What is Ollama? Complete Guide to Local AI Models 2025. **Skywork**, out. 2025. Disponível em: <https://skywork.ai/blog/agent/what-is-ollama-complete-guide-to-local-ai-models-2025/>. Acesso em: 11 maio 2026.
 
> 8. DEEPWIKI. System Requirements — ollama/ollama. **DeepWiki**, 2025. Disponível em: <https://deepwiki.com/ollama/ollama/1.2-system-requirements>. Acesso em: 11 maio 2026.
 
> 9. OHIO SUPERCOMPUTER CENTER. Ollama. **OSC**, 2025. Disponível em: <https://www.osc.edu/resources/available_software/software_list/ollama>. Acesso em: 11 maio 2026.
 
> 10. BYTESIZEGO. Exploring Ollama: Running LLMs Locally with Go. **ByteSizeGo**, dez. 2025. Disponível em: <https://www.bytesizego.com/blog/exploring-ollama-running-llms-locally-with-go>. Acesso em: 11 maio 2026.
 
> 11. ORGANIZAÇÃO DAS NAÇÕES UNIDAS. Objetivo de Desenvolvimento Sustentável 4: Educação de qualidade. Disponível em: <https://brasil.un.org/pt-br/sdgs/4>. Acesso em: 11 maio 2026.
 
> 12. ORGANIZAÇÃO DAS NAÇÕES UNIDAS. Objetivo de Desenvolvimento Sustentável 9: Indústria, inovação e infraestrutura. Disponível em: <https://brasil.un.org/pt-br/sdgs/9>. Acesso em: 11 maio 2026.
 
> 13. ORGANIZAÇÃO DAS NAÇÕES UNIDAS. Objetivo de Desenvolvimento Sustentável 10: Redução das desigualdades. Disponível em: <https://brasil.un.org/pt-br/sdgs/10>. Acesso em: 11 maio 2026.
 
---
 
## Histórico de Versão
 
| Versão | Data | Descrição | Autor | Revisor |
|---|---|---|---|---|
| 1.0 | 11/05/2026 | Criação da descrição do produto Ollama | [Johnnatan Salles](https://github.com/jsalless) | [Renata Quadros](https://github.com/RenataKurzawa) |