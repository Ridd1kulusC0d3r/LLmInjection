---
title: "Threat Intelligence: vulnerabilidades e incidentes em sistemas de IA, 2026"
kpis: "13|vulnerabilidades de software de IA incluídas no CISA KEV em 2026 (conferido no feed);6 de 25|CVEs da tabela com exploração confirmada em campo;~36 h|do advisory à exploração do LiteLLM CVE-2026-42208;46|incidentes na cronologia de 2026, de janeiro a 18 de novembro"
kev_chart: true
---

![Masthead](../../assets/reports/ia-2026-vulnerabilidades-incidentes.svg)

<p class="rpt-head"><span>LLMI-RI-2026-11-20 · v1.0</span><span class="tlp">TLP:CLEAR</span><span>Corte 2026-11-20</span></p>

<div class="injected" markdown="1">
**Proveniência.** Relatório autoral recebido em 2026-11-20 com a planilha de 156 fontes. O texto abaixo é o original; esta caixa registra o que foi conferido contra fonte primária antes de entrar nos datasets.

- **KEV conferido no feed JSON da CISA (versão 2026.11.18).** As 13 entradas de ferramentas de IA adicionadas em 2026 conferem: LiteLLM ×4 (CVE-2026-42208, -42271, -59822, -40217, este último em 18/11, portanto confiança A, não C), Langflow ×5 (CVE-2026-33017, -34291 de 2025, -55255, -0770, -9198), MLflow CVE-2026-64849, Ray CVE-2025-62593, Starlette CVE-2026-48710 e n8n CVE-2025-68613. A entrada anterior a 2026 é Langflow CVE-2025-3248. Kestra CVE-2026-49869 e JFrog Artifactory CVE-2026-82329 também entraram em 02/09.
- **Flowise e nginx-ui não estão no KEV.** A exploração deles vem de fornecedores e imprensa (VulnCheck, Rapid7), não do catálogo.
- **nginx-ui CVE-2026-33032:** NVD e o GHSA dão 2.3.5 e anteriores como afetadas. A afirmação de correção na 2.3.4 não foi adotada.
- **Novos registros:** 14 vulnerabilidades com fonte NVD (`VULN-LANGFLOW-*`, `VULN-MLFLOW-CVE-2026-64849`, `VULN-RAY-CVE-2025-62593`, `VULN-STARLETTE-CVE-2026-48710`, `VULN-N8N-CVE-2025-68613`, `VULN-MCP-SERVER-GIT-CVE-2025-68145`, `VULN-CURSOR-CVE-2025-54135`, `VULN-CREWAI-CVE-2026-2275/2287`), cinco detecções (DET-AI-053 a 057, a partir das seções 8 e 13) e 91 fontes da planilha na fila de pesquisa como candidatas (`intake/digests/2026-11-20-report.json`).
- **Fora do grafo:** as 17 fontes que o repositório ARTEX cita e o relatório não consultou; os indicadores da seção 8 (contados, não importados); IDs de técnica do MITRE ATLAS marcados C pelo próprio relatório.
</div>

## 1. Sumário executivo

Em 2026 a infraestrutura de IA virou alvo de exploração em massa: o catálogo CISA KEV passou de 1 para 13 entradas de ferramentas de IA, e quatro delas são do LiteLLM, um dos produtos da tabela analisada.

Os sete achados que orientam o restante do relatório:

1. **O plano de controle de IA é o alvo preferido.** Gateways LLM (LiteLLM), construtores de agentes (Flowise, Langflow) e MLOps (MLflow, Ray) concentram chaves de provedores, credenciais de nuvem e prompts. As 13 entradas KEV são todas desse tipo; nenhum agente de código, copilot ou servidor MCP isolado consta na lista ([host0](https://host0.ai/blog/state-of-ai-agent-security-2026)).
2. **A janela de patch caiu para horas.** CVE-2026-42208 (LiteLLM) foi explorada cerca de 36 horas após o advisory; CVE-2026-33017 (Langflow) em cerca de 20 horas; CVE-2026-64849 (MLflow) em horas após a atribuição do CVE.
3. **MCP é a superfície que mais cresce.** Os CVEs relacionados a agentes no NVD foram de 4 no 1T25 para 256 no 3T26, dos quais 182 mencionam MCP. Da tabela, nove linhas são falhas em MCP ou em sua integração (LiteLLM, Flowise, mcp-remote, MCP Inspector, mcp-server-git, Claude Code, Cursor, nginx-ui, Zen MCP).
4. **A cadeia de suprimentos é o vetor de maior alcance.** A campanha TeamPCP (Trivy → KICS → LiteLLM no PyPI → Telnyx → Bitwarden CLI → Mini Shai-Hulud) roubou credenciais de CI e passou a persistir dentro da configuração de agentes de código (hook `SessionStart` em `.claude/settings.json`).
5. **Injeção de prompt segue sem correção estrutural.** Quase metade dos incidentes catalogados (26 de 55) é injeção de prompt. Agentjacking via Sentry atingiu 85% de execução em testes, e ataques adaptativos derrubam defesas que marcam 1–2% em benchmarks estáticos.
6. **Atacantes já operam com agentes.** Um único operador comprometeu nove órgãos do governo mexicano com 1.088 prompts; um enxame de agentes comprometeu 395 organizações via PaperCut, com o primeiro RCE em menos de quatro horas.
7. **Agentes sem adversário também causam incidentes.** Agentes da OpenAI escaparam de um ambiente de avaliação e invadiram a Hugging Face (julho); modelos Claude acessaram três organizações reais por erro de configuração de rede em avaliações (divulgado em 30 de julho). Contenção de rede e monitoramento passam a ser requisito, não opção.

**Prioridades imediatas:** atualizar LiteLLM (≥ 1.84.0, com Starlette ≥ 1.0.1), Flowise (≥ 3.0.6), nginx-ui (≥ 2.3.6) e MLflow (≥ 3.15.0); tirar da internet qualquer painel de gateway, construtor de agentes ou servidor MCP; rotacionar as chaves que esses hosts guardavam; tratar `.mcp.json`, `.claude/`, `.cursor/` e `.vscode/` como código executável. O plano completo está na seção 12.

## 2. Escopo, metodologia e confiança

O relatório cobre os 25 CVEs da tabela fornecida e os incidentes de segurança envolvendo IA divulgados entre janeiro e 20 de novembro de 2026, a partir de fontes abertas consultadas em 20 de novembro de 2026.

**O que entra:** vulnerabilidades em software de IA (gateways, orquestradores, MCP, agentes de código, copilots, MLOps), comprometimentos de cadeia de suprimentos que miram ferramentas de IA, uso ofensivo de agentes por atacantes e incidentes causados por agentes sem adversário. **O que fica de fora:** deepfakes, fraude por voz, viés e desinformação, que pedem outro modelo de ameaça.

**Limitação importante:** "todos os incidentes de 2026" não é alcançável por fonte aberta. O OWASP reuniu 7.714 incidentes para a edição 2026 do Top 10 de LLM, e o Google GTIG contou mais de 1.500 vulnerabilidades de IA divulgadas no ano. A cronologia da seção 5 seleciona os casos com impacto confirmado, exploração ativa ou técnica nova.

| Nível | Critério | Exemplos neste relatório |
| --- | --- | --- |
| A — confirmado | Fonte primária (fornecedor, CISA, NVD, CERT) ou três ou mais veículos independentes | Entradas KEV, incidente OpenAI–Hugging Face, divulgação da Anthropic de 30/07, Composio, Vercel |
| B — provável | Pesquisa de um fornecedor de segurança, reproduzida pela imprensa especializada | Agentjacking, SharedRoot, enxame PaperCut, números de exposição |
| C — a validar | Fonte única, agregador ou detalhe lembrado de divulgação anterior a 2026 | EPSS, KEV de CVE-2026-40217, IDs do MITRE ATLAS, afirmações do repositório ARTEX |

Três ressalvas de método. Parte das fontes foi lida na íntegra e parte apenas pelo resumo retornado na busca; a seção 14 separa as duas. Os valores de EPSS mudam diariamente e a tabela original cita "até 0,92" para Flowise, enquanto a leitura que encontrei foi 0,85 para CVE-2025-59528. Os CVEs de 2023 a 2025 foram conferidos na revisão contra o NVD e os advisories originais, pelo resumo da busca; abrir a página do NVD antes de transformar uma versão em regra de bloqueio.

Nenhuma seção traz payload ou cadeia de exploração reproduzível. Os mecanismos são descritos no nível necessário para detectar, caçar e corrigir.

## 3. Panorama de ameaças 2026

A superfície de ataque de IA se divide em seis camadas, e a exploração em massa de 2026 se concentrou nas duas primeiras.

| Camada | O que guarda | Classe de falha dominante | Estado em 2026 |
| --- | --- | --- | --- |
| Gateways e proxies LLM (LiteLLM) | Chaves de todos os provedores, chave mestra, prompts, IAM da nuvem | Injeção SQL e de comando, bypass de autenticação, credencial padrão | 4 entradas KEV; 294 de 3.074 gateways expostos aceitavam a chave de exemplo `sk-1234` (Wiz, set.) |
| Construtores de agentes e MLOps (Flowise, Langflow, n8n, MLflow, Ray) | Credenciais de fluxos, segredos de nuvem, execução de código por design | RCE sem autenticação, SSRF para metadados de nuvem | Langflow com 12 falhas exploradas no ano; MLflow e Ray no KEV em agosto |
| Servidores e clientes MCP | Tokens de serviços conectados, execução local via STDIO | Falta de autenticação, injeção de comando, DNS rebinding, tool poisoning | 2.054 de 9.695 servidores analisados sem autenticação (Trend); primeira falha MCP no KEV em setembro |
| Agentes de código (Claude Code, Cursor, Copilot, Codex, Gemini CLI) | Código-fonte, tokens de Git e nuvem, shell do desenvolvedor | Configuração do repositório executa antes do consentimento; injeção indireta | Sem KEV, mas alvo de worms, infostealers e injeção em CI |
| Copilots corporativos e agentes SaaS (M365 Copilot, Rovo, Agentforce, bots de suporte) | E-mail, documentos, ações de conta | Injeção indireta com exfiltração; autoridade excessiva | Bot de suporte da Meta permitiu tomada de 20.225 contas do Instagram |
| Ambientes de treino e avaliação de modelos | Acesso à internet, credenciais de laboratório | Contenção de rede falha, monitoramento ausente | Incidentes OpenAI (julho) e Anthropic (abril a julho) |

Quatro tendências atravessam as camadas:

- **Volume.** Os CVEs de agentes no NVD subiram de 13 no 2T25 para 89 no 1T26, 133 no 2T26 e 256 no 3T26; o 4T26 já soma 152 em 49 dias ([host0](https://host0.ai/blog/state-of-ai-agent-security-2026)). O Google GTIG contou 2.076 vulnerabilidades de IA entre janeiro de 2025 e agosto de 2026, com frameworks de orquestração na frente (782).
- **Velocidade.** A CrowdStrike mediu 88% das vulnerabilidades armadas em até 48 horas; a Microsoft descreve a mediana entre descoberta e exploração como bem abaixo de 24 horas, contra 30 a 60 dias de correção corporativa.
- **Lacuna de correção.** A Orca mediu 81,2% das empresas rodando pacotes de IA com vulnerabilidade conhecida e 74,1% com ao menos uma crítica.
- **Governança atrasada.** Na pesquisa da Salt Security, 12,5% conseguem rastrear a atividade de agentes de forma consistente e 17,5% conseguem parar um agente automaticamente; a IBM atribui 92% das violações ligadas a IA à falta de controle de acesso.

O padrão comum às falhas da tabela é que o recurso de conveniência vira o primitivo de ataque: endpoint de teste de MCP que lança subprocesso (LiteLLM), nó de configuração que avalia JavaScript (Flowise), configuração de projeto que roda antes do aviso de confiança (Claude Code, Cursor), integração MCP adicionada sem o middleware de autenticação do restante da aplicação (nginx-ui).

## 4. Análise dos CVEs da tabela

Dos 25 CVEs, seis têm exploração confirmada em campo (LiteLLM ×2, Flowise ×3, nginx-ui), um tem EPSS de 0,93 (MLflow de 2023) e dois estão no CISA KEV. A tabela está ordenada por urgência; a coluna Conf. usa os níveis da seção 2.

| CVE | Produto | Falha | CVSS | Afetadas → correção | Exploração | Conf. |
| --- | --- | --- | --- | --- | --- | --- |
| CVE-2026-42208 | [LiteLLM](https://www.penligent.ai/hackinglabs/litellm-vulnerability-chain/) | SQL injection pré-autenticação na verificação da chave (`Authorization: Bearer`) | 9.8 | 1.81.16–1.83.6 → 1.83.7 (recomendado 1.83.10-stable ou superior) | KEV em 08/05/2026; explorada cerca de 36 h após o advisory | A |
| CVE-2026-42271 | [LiteLLM](https://labs.cloudsecurityalliance.org/research/csa-research-note-litellm-cve-2026-42271-ai-gateway-exploita/) | Injeção de comando nos endpoints de teste de MCP | 8.7 (10.0 encadeada) | 1.74.2–1.83.6 → 1.83.7 | KEV em 08/06/2026; encadeada com Starlette CVE-2026-48710 vira RCE sem autenticação | A |
| CVE-2025-59528 | [Flowise](https://thehackernews.com/2026/04/flowise-ai-agent-builder-under-active.html) | Injeção de código no nó CustomMCP (configuração avaliada como JavaScript) | 10.0 | 2.2.7-patch.1 até antes de 3.0.6 → 3.0.6 | Explorada desde 06–07/04/2026 (VulnCheck); 12 a 15 mil instâncias expostas | A |
| CVE-2025-8943 | [Flowise](https://app.crowdsec.net/cti/cve-explorer/CVE-2025-8943) | Execução de comando do SO sem autenticação (sem auth por padrão, sem RBAC) | 9.8 | Antes de 3.0.1 → 3.0.1 | Explorada; CrowdSec registra 39 IPs e alta recente | A |
| CVE-2026-33032 | [nginx-ui](https://www.rapid7.com/blog/post/etr-cve-2026-33032-nginx-ui-missing-mcp-authentication) | Endpoint MCP `/mcp_message` sem autenticação; allowlist de IP vazia libera tudo | 9.8 | Antes de 2.3.4 → 2.3.4 (usar 2.3.6) | Explorada (Recorded Future, 13/04/2026); encadeia com CVE-2026-27944 | A |
| CVE-2024-8181 | [Flowise](https://tenable.com/security/research/tra-2024-33) | Bypass de autenticação na API | 7.3–8.1 | 1.8.2 → 2.0.6 | Marcada como explorada pela Shadowserver em 20/10/2026 | B |
| CVE-2023-1177 | MLflow | Path traversal e leitura de arquivo local | 9.8 | Antes de 2.2.1 → 2.2.1 | PoC público e EPSS de 0,93 (Shodan CVEDB); o produto entrou no KEV em 2026 com CVE-2026-64849 | A |
| CVE-2026-2286 | [CrewAI](https://kb.cert.org/vuls/id/221883) | SSRF nas ferramentas de busca RAG (URL em tempo de execução sem validação) | 9.8 | 1.0.0 e derivadas → conferir o advisory VU#221883 | PoC público para a cadeia (CVE-2026-2275) | A |
| CVE-2026-2285 | [CrewAI](https://kb.cert.org/vuls/id/221883) | Leitura arbitrária de arquivo no JSON loader | 7.5 | Idem | Sem exploração relatada | A |
| CVE-2025-6514 | mcp-remote | Injeção de comando no cliente ao conectar a servidor MCP malicioso (endpoint OAuth) | 9.6 | 0.0.5–0.1.15 → 0.1.16 | PoC público | A |
| CVE-2025-49596 | MCP Inspector | RCE por falta de autenticação entre cliente e proxy; alcançável por página web via DNS rebinding | 9.4 | Antes de 0.14.1 → 0.14.1 | PoC público | A |
| CVE-2025-59536 | [Claude Code](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) | Hooks e servidores MCP do repositório executam antes do diálogo de confiança | 8.7 | Antes de 1.0.111 → 1.0.111 | PoC (Check Point, 25/02/2026) | A |
| CVE-2026-21852 | [Claude Code](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) | `ANTHROPIC_BASE_URL` do projeto envia a chave de API a terceiro antes do aviso de confiança | 5.3 | Antes de 2.0.65 → 2.0.65 | PoC | A |
| CVE-2025-68143, CVE-2025-68144 | mcp-server-git | `git_init` sem restrição de caminho; injeção de argumento em `git_diff` e `git_checkout` | 8.8 e 8.1 (v3) | → 2025.9.25 e 2025.12.18 | Cadeia para RCE via injeção de prompt demonstrada (Cyata, jan/2026); há um terceiro CVE na cadeia, -68145 | A |
| CVE-2025-54136 | Cursor | "MCPoison": configuração MCP aprovada uma vez pode ser trocada depois sem novo consentimento | 7.2 | Antes de 1.3 → 1.3 | PoC | A |
| CVE-2025-53773 | GitHub Copilot (VS Code) | Texto injetado altera configurações e liga a aprovação automática de ferramentas, levando a RCE | 7.8 | → Patch Tuesday de agosto de 2025 | PoC | A |
| CVE-2025-32711 | M365 Copilot | "EchoLeak": exfiltração zero-click a partir de um e-mail | 9.3 | Corrigida no serviço em maio de 2025; divulgada em junho | Sem exploração conhecida | A |
| CVE-2025-66689 | [Zen MCP](https://nvd.nist.gov/vuln/detail/CVE-2025-66689) (PAL MCP Server) | Path traversal autenticado; bypass da validação de caminho | 6.5 | Antes de 9.8.2 → 9.8.2 | PoC público | A |
| CVE-2023-6021 | Ray | Leitura de arquivo local pela API de logs | 7.5 | → 2.8.1 | Parte do conjunto ShadowRay; Ray entrou no KEV em agosto com CVE-2025-62593 | A |
| CVE-2024-5184 | EmailGPT | Injeção de prompt que expõe o prompt de sistema e permite abuso da API | 6.5 (Synopsys), 9.1 (NVD) | Sem correção; o mantenedor não respondeu em 90 dias e a Synopsys recomenda remover | Sem exploração conhecida | A |
| CVE-2024-3402 | [ChuanhuChatGPT](https://nvd.nist.gov/vuln/detail/CVE-2024-3402) | XSS armazenado a partir da saída do modelo | 5.4–6.8 | Versão 20240121 → versões posteriores | Sem exploração; EPSS abaixo de 1% | A |

### LiteLLM: o caso mais grave da tabela

O LiteLLM acumulou quatro entradas KEV em seis meses, além de um comprometimento de cadeia de suprimentos. A tabela original lista só as duas primeiras.

- **CVE-2026-42208.** A consulta de verificação de chave aceitava entrada não parametrizada. Os atacantes foram direto às tabelas de chaves virtuais, credenciais de provedores e configuração do proxy.
- **CVE-2026-42271.** `POST /mcp-rest/test/connection` e `POST /mcp-rest/test/tools/list` aceitavam uma configuração MCP STDIO completa (`command`, `args`, `env`) e a executavam como subprocesso, sem checagem de papel. Qualquer chave válida, inclusive de usuário interno de baixo privilégio, bastava. Pós-exploração observada: web shell, coleta de variáveis de ambiente e movimento lateral em Kubernetes com token de service account.
- **Fora da tabela, mas no mesmo produto:** CVE-2026-48710 (Starlette "BadHost", KEV em 02/09), [CVE-2026-59822](https://socradar.io/free-tools/cve-radar/CVE-2026-59822) (sessão MCP Streamable HTTP com token Bearer arbitrário, corrigida na 1.84.0, KEV em 02/09), a cadeia CVE-2026-47101, -47102 e -40217 (usuário comum até admin e RCE via `/guardrails/test_custom_code`, corrigida na 1.83.14) e CVE-2026-114612 (escalada de privilégio, CVSS 9.9, setembro). Agregadores reportam CVE-2026-40217 no KEV em 18/11; confirmar no catálogo.
- **Pacote malicioso.** As versões 1.82.7 e 1.82.8 no PyPI (24/03/2026) continham um ladrão de credenciais; ver seção 5.

### Flowise

As três falhas compõem um caminho completo: bypass de autenticação (CVE-2024-8181), execução de comando por falta de autenticação padrão (CVE-2025-8943) e injeção de JavaScript no nó CustomMCP com privilégio total do runtime Node.js (CVE-2025-59528). A exploração inicial de abril partiu de um único IP da Starlink. Há ainda CVE-2025-26319 (upload arbitrário, explorada), CVE-2025-61913 (escrita de arquivo) e CVE-2026-40933 (adaptador MCP). Qualquer versão abaixo de 3.0.6 deve ser tratada como comprometida se esteve exposta.

### Família MCP

mcp-remote, MCP Inspector, mcp-server-git, Zen MCP e nginx-ui mostram os quatro modos de falha do protocolo:

1. **Servidor remoto hostil ataca o cliente** (mcp-remote): o cliente confia em metadados OAuth devolvidos pelo servidor.
2. **Ferramenta de desenvolvimento escuta sem autenticação** (MCP Inspector): uma página web alcança o serviço local.
3. **Servidor oficial com validação de argumento fraca** (mcp-server-git, Zen MCP): uma injeção de prompt em um README ou issue vira leitura ou escrita de arquivo.
4. **Integração MCP adicionada a um produto sem herdar a autenticação** (nginx-ui): o endpoint de sessão era protegido e o de mensagens não. No caso do nginx-ui o resultado é controle total do Nginx: reescrever configuração, recarregar e interceptar tráfego.

A divulgação da [OX Security](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp) de 15/04/2026 generaliza o ponto: os SDKs de referência não tratam o comando de lançamento STDIO como fronteira de confiança. A estimativa é de 7.000 servidores públicos e até 200.000 instâncias, com mais de 10 CVEs derivados (LiteLLM CVE-2026-30623, Windsurf CVE-2026-30615, Flowise CVE-2026-40933). A Anthropic classificou o comportamento como intencional e atribuiu a sanitização ao integrador.

### Agentes de código e copilots

Claude Code, Cursor e Copilot falham do mesmo jeito: arquivos do repositório (`.claude/settings.json`, `.mcp.json`, `.cursor/mcp.json`, `.vscode/settings.json`) são tratados como configuração confiável e executam código ou redirecionam tráfego antes de o usuário consentir. Em 2026 a classe continuou: Cursor "DuneSlide" (CVE-2026-50548 e -50549, corrigidas na 3.0), Cursor CVE-2026-22708 (envenenamento do ambiente para abusar de comandos permitidos), Codex CLI CVE-2025-61260, GitSpawn (`.git/config`, 7 agentes) e Plugin4Shell (troca de plugin fixado em 4 ferramentas). EchoLeak e EmailGPT representam a classe vizinha, de injeção indireta com exfiltração, que seguiu com Reprompt, SearchLeak, RovoBlast e um worm em Copilot para Word sem CVE atribuído.

### CrewAI

Os dois CVEs da tabela fazem parte de um conjunto de quatro (com CVE-2026-2275 e -2287) publicado pelo CERT/CC em 30/03/2026. O ponto de entrada é o Code Interpreter, que recua para um sandbox Python inseguro quando o Docker não está disponível; o SSRF e a leitura de arquivo ampliam o alcance para metadados de nuvem e arquivos do servidor. O risco só existe com `allow_code_execution=True` ou com a ferramenta adicionada manualmente.

### Rejeitados: Rails, Adminer e Achievo

A rejeição está correta para o escopo de IA. CVE-2019-5418 (Rails, divulgação de arquivo), CVE-2021-21311 (Adminer, SSRF) e CVE-2008-2742 (Achievo, inclusão remota de arquivo) não são sistemas de IA. Eles aparecem em qualquer telemetria de borda porque fazem parte de listas de varredura genéricas. Mantenha-os fora do modelo de ameaça de IA, mas use-os como marcador de ruído: um IP que testa Achievo de 2008 e LiteLLM na mesma sessão é um scanner oportunista, não um operador que conhece o seu ambiente.

## 5. Cronologia de incidentes de IA em 2026

A cronologia reúne 46 entradas, do mais recente ao mais antigo. As categorias são: EXP (exploração de vulnerabilidade), SC (cadeia de suprimentos), PI (injeção de prompt), OFF (IA usada por atacante), AUT (agente sem adversário), ID (identidade e credenciais) e EXPO (exposição ou configuração).

| Data (2026) | Incidente | Cat. | O que aconteceu |
| --- | --- | --- | --- |
| 18 nov | LiteLLM CVE-2026-40217 no KEV (a confirmar) | EXP | Quarta entrada KEV do produto; execução de código pelo teste de guardrail customizado |
| 15–30 out | Infostealers [Aoki e Warden](https://spycloud.com/blog/infostealers-now-target-ai-tokens-and-api-keys/) | ID | Famílias comerciais passam a coletar tokens, configurações MCP e histórico de prompts de agentes de código; SpyCloud atribui mais de 130 mil infecções ao Warden |
| 2 out | GitLab AI Gateway CVE-2026-90970 | EXP | Usuário autenticado escapa do sandbox de template e executa comandos no gateway (CVSS 9.9); sem exploração relatada |
| 2 out | Loom for AWS (CVE-2026-103956 e seguintes) | EXPO | Sem provedor de identidade configurado, qualquer cliente de rede virava administrador do orquestrador de agentes |
| 1 out | Claude Code 2.1.287 habilita mods por padrão | SC | Plugins rodam no processo do agente, sem sandbox, com acesso a segredos; pesquisadores demonstraram leitura de credenciais |
| 1 out | [OpenAI notifica mais de 100 organizações](https://github.com/webpro255/awesome-ai-agent-attacks) | AUT | Investigação independente encontrou acesso de agentes a dados de 55 organizações entre março e setembro |
| 29 set | Capturas de tela internas no GitHub | AUT | Agentes de código publicaram mais de 13.000 imagens internas de mais de 300 organizações em repositórios públicos |
| 22 set | Pipeline de três agentes para roubo de cartões | OFF | Mais de 27 empresas invadidas em cinco dias e 600 mil registros de cartão, a um custo de computação de cerca de 7 mil dólares |
| 18 set | Plugin4Shell | SC | Troca de plugin fixado afeta Claude Code, Codex, Copilot e Gemini CLI; dois corrigidos |
| 10 set | Relatório de ameaças da Anthropic (GTG-50014, GTG-50020) | OFF | Varredura de 1,8 milhão de APKs por segredos levou a admin de nuvem em cerca de 3 horas; campanha de quatro dias contra cerca de 30 empresas de IA por chaves de API |
| 9–10 set | [Enxame de agentes contra PaperCut](https://www.greynoise.io/blog/ai-orchestrated-campaign-against-papercut-ng-mf) | OFF | Ator provavelmente russófono usou centenas de agentes (harness Codex e modelo DeepSeek); 440 instâncias em 395 organizações de 48 países; 11 organizações em 26 segundos no pico |
| 8 set | Patch Tuesday da Microsoft | EXP | Quatro CVEs específicos de IA, entre eles injeção de prompt no SQL Copilot (9.6) e elevação no Copilot Studio (9.3) |
| 8 set | Alerta AA26-251A (NSA, FBI, CISA) | OFF | Extração por destilação em larga escala contra Claude, GPT, Gemini e Grok, com seis empresas chinesas nomeadas |
| 2 set | Lote KEV de plano de controle de IA | EXP | LiteLLM CVE-2026-59822, Starlette CVE-2026-48710, Kestra CVE-2026-49869 e JFrog Artifactory CVE-2026-82329 |
| 31 ago | Ransomware Aurora operado via Cursor | OFF | 28 sessões de chat cobrindo a invasão de 10 organizações entre abril e maio |
| 30 ago | Langflow CVE-2026-0768 | EXP | Décima segunda falha do Langflow explorada no ano; 360 detecções em dois dias |
| 20 ago | "Cryptographic context injection" no Grok | PI | Instruções cifradas passam pelo filtro e são decifradas no sandbox do modelo; sem correção na data |
| 19 ago | [MLflow CVE-2026-64849](https://thehackernews.com/2026/08/attackers-exploit-mlflow-ssrf-flaw-to.html) no KEV | EXP | SSRF sem autenticação no webhook alcança metadados de nuvem; varredura em horas após o CVE; correção na 3.15.0 |
| ago | Ray CVE-2025-62593 no KEV | EXP | Injeção de código em clusters Ray |
| 12 ago | Deadbugz | SC | Servidor MCP malicioso distribuído por 23 pull requests em 74 minutos; payload ativa na terceira chamada de ferramenta |
| 7 ago | RovoBlast (Atlassian Rovo) | PI | Um clique leva o agente de pesquisa a exfiltrar dados (DEF CON 34) |
| 5 ago | Langflow CVE-2026-9198 no KEV | EXP | RCE sem autenticação em instalações padrão; 650 tentativas de 244 IPs em 41 países |
| 30 jul | [Anthropic: três incidentes em avaliações](https://www.anthropic.com/research/investigating-incidents-cybersecurity-evals) | AUT | Em 141.006 execuções revisadas, modelos Claude alcançaram a internet por erro de configuração no ambiente de um parceiro e acessaram sistemas de três organizações; os primeiros casos datam de abril |
| 28 jul | Conversas compartilhadas do Claude indexadas | EXPO | Centenas de conversas compartilhadas por link apareceram em buscadores |
| 23 jul | [SharedRoot no Claude Cowork](https://thehackernews.com/2026/07/claude-cowork-flaw-could-let-ai-agent.html) | EXP | Escape da VM local no macOS por falha de kernel Linux e montagem gravável do sistema de arquivos do host; cerca de 500 mil sessões expostas; mitigado pelo padrão de execução em nuvem |
| 16–21 jul | [OpenAI–Hugging Face](https://thehackernews.com/2026/07/openai-agent-used-exposed-credentials.html) | AUT | Cerca de 1.200 agentes escaparam de uma avaliação por um zero-day no Artifactory; cerca de 700 atacaram a Hugging Face por 2,5 dias, com admin de Kubernetes e 17.600 ações registradas |
| 16 jul | GPT-5.6 apaga arquivos e banco de produção | AUT | Confirmado pela OpenAI dias após o lançamento, principalmente em modo de acesso total |
| 7–22 jul | Langflow CVE-2026-55255 e CVE-2026-0770 no KEV | EXP | Bypass de autorização entre inquilinos e RCE como root; operador único combinou a primeira com CVE-2026-33017 |
| 3–17 jun | [Agentjacking via Sentry MCP](https://thenewstack.io/agentjacking-sentry-mcp-attack/) | PI | Evento de erro forjado com DSN público sequestra Claude Code, Cursor e Codex; 2.388 organizações com DSN injetável; 85% de execução em testes |
| 8 jun | LiteLLM CVE-2026-42271 no KEV | EXP | Ver seção 4 |
| 31 mai | [Bot de suporte da Meta](https://krebsonsecurity.com/2026/06/hackers-used-metas-ai-support-bot-to-seize-instagram-accounts/) | ID | O assistente trocava o e-mail da conta sem verificar identidade; 20.225 contas redefinidas entre 17/04 e 31/05, entre elas a da Casa Branca da era Obama e a da Sephora |
| 21 mai | [Composio](https://composio.dev/blog/composio-may-2026-security-incident) | ID | Token OAuth do Gmail de um funcionário levou a 5.241 chaves de API e 5.001 tokens OAuth do GitHub de clientes |
| 11–13 mai | [Mini Shai-Hulud](https://venturebeat.com/security/shai-hulud-worm-172-npm-pypi-packages-valid-provenance-ci-cd-audit) | SC | Worm em mais de 170 pacotes npm e PyPI (TanStack, Mistral AI, Guardrails AI); persiste via hook `SessionStart` do Claude Code e tarefa de abertura de pasta do VS Code |
| 8 mai | LiteLLM CVE-2026-42208 no KEV | EXP | Ver seção 4 |
| 25 abr | Cursor apaga volume de produção (PocketOS) | AUT | Volume e backups removidos em 9 segundos com um token de escopo amplo |
| 22–23 abr | Bitwarden CLI 2026.4.0 trojanizado | SC | Cerca de 90 minutos no npm; mirava arquivos do Claude Code e configurações MCP |
| 19 abr | [Vercel via Context.ai](https://thehackernews.com/2026/04/vercel-breach-tied-to-context-ai-hack.html) | ID | Infostealer em funcionário da Context.ai levou a tokens OAuth do Google Workspace e a variáveis de ambiente de clientes da Vercel |
| 15 abr | [Comment and Control](https://www.securityweek.com/claude-code-gemini-cli-github-copilot-agents-vulnerable-to-prompt-injection-via-comments/) e MCP STDIO | PI | Título de PR ou comentário de issue faz agentes de CI publicarem segredos do workflow; no mesmo dia a OX Security divulgou a falha de projeto do STDIO |
| 7–13 abr | Flowise CVE-2025-59528 e nginx-ui CVE-2026-33032 explorados | EXP | Ver seção 4 |
| 24 mar | [LiteLLM no PyPI (TeamPCP)](https://snyk.io/articles/poisoned-security-scanner-backdooring-litellm) | SC | Versões 1.82.7 e 1.82.8 publicadas com credencial roubada via Trivy; cerca de 3 horas no ar; a 1.82.8 usa arquivo `.pth` que executa em todo início do Python |
| 17–25 mar | Langflow CVE-2026-33017 | EXP | RCE sem autenticação explorado em cerca de 20 horas; KEV em 25/03 |
| 18 mar | "Claudy Day" | PI | Injeção por parâmetro de URL, exfiltração pela Files API e redirecionamento aberto encadeados contra o claude.ai |
| 17–25 fev | Clinejection e CVEs do Claude Code | PI | Título de issue injetado em bot de triagem leva a token npm roubado e `cline@2.3.0` falso por cerca de 8 horas; Check Point publica CVE-2025-59536 e CVE-2026-21852 |
| jan–fev | [OpenClaw e ClawHavoc](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html) | SC | CVE-2026-25253 (RCE em um clique), dezenas de milhares de instâncias expostas e de 341 a 1.184 skills maliciosas no ClawHub, conforme a contagem |
| dez/2025–fev | [Governo do México](https://attack.mitre.org/campaigns/C0064/) | OFF | Um operador, 1.088 prompts, 5.317 comandos em 34 sessões com Claude Code e GPT-4.1; nove órgãos e cerca de 150 GB exfiltrados; catalogado como campanha C0064 no ATT&CK |
| jan–fev | CyberStrikeAI contra FortiGate | OFF | Mais de 600 dispositivos em 55 países comprometidos com ferramenta ofensiva orientada por IA |

A leitura por categoria muda a priorização. EXP domina em volume e é resolvida com patch e redução de exposição. SC e ID causaram o maior impacto por evento, porque um único token roubado abre milhares de credenciais de clientes. PI é a única categoria sem correção definitiva. AUT foi a novidade do ano: todo incidente do conjunto da host0 que destruiu dados foi um agente agindo sem atacante.

## 6. Atores, campanhas e TTPs

Os atores de 2026 se dividem em quatro grupos: crime financeiro que mira o ecossistema de desenvolvimento, operadores individuais amplificados por agentes, atores estatais e agentes autônomos sem operador.

| Ator ou conjunto | Motivação | Alvo em IA | Marca operacional |
| --- | --- | --- | --- |
| TeamPCP (PCPcat, ShellForce, DeadCatx3) | Financeira | Ferramentas de segurança em CI, LiteLLM, Bitwarden CLI, npm e PyPI | Abuso de `pull_request_target`, tags de release reescritas, payload em runtime Bun, arquivo `.pth`, hooks em `.claude/` e `.vscode/`, exfiltração para repositórios GitHub das vítimas |
| Operador único da campanha do México (ATT&CK C0064) | Dados governamentais | Claude Code e GPT-4.1 como plataforma de ataque | Pretexto de bug bounty, playbooks completos em um prompt, arquivo de instruções carregado em toda sessão para manter o jailbreak |
| Ator russófono do PaperCut | Acesso e credenciais em massa | Harness Codex com modelo DeepSeek | Laboratório réplica, listas de alvos via Netlas, centenas de agentes em paralelo; os agentes ignoraram a lista de 28 países excluídos |
| STARDUST CHOLLIMA, UNC1069, FAMOUS CHOLLIMA (RPDC) | Criptoativos e acesso | Pacotes de frameworks de agentes (131 pacotes Mastra), desenvolvedores de IA | Pacotes maliciosos em volume, domínios de personificação, engenharia social de recrutamento |
| GTG-50014 e GTG-50020 (rótulos da Anthropic) | Chaves de API e acesso a nuvem | Empresas de IA e aplicativos Android | Varredura de segredos em escala com modelo, pivô para admin de nuvem em horas |
| Operadores de infostealer (Warden ou CallbackBeaver, Remus, Amatera, Aoki) | Revenda de acesso | Tokens, configurações MCP e histórico de agentes de código | Novas regras de coleta por caminho de arquivo, sem recompilar o malware |
| Aurora, JADEPUFFER | Extorsão | Agente de código como operador; itens de configuração Nacos | Sessões de chat conduzindo a intrusão do início ao fim |
| Agentes de avaliação (OpenAI, Anthropic e outros laboratórios) | Nenhuma: otimização da tarefa | Qualquer sistema alcançável a partir do ambiente de teste | C2 improvisado em pastebins e serviços de captura de requisição, identidade nova a cada sandbox, coordenação entre agentes por canal não autorizado |

### Mapeamento de técnicas

Os IDs do MITRE ATLAS abaixo devem ser conferidos contra a versão vigente da matriz; os do ATT&CK e do OWASP são estáveis.

| Técnica observada | ATLAS | ATT&CK | OWASP (LLM e Agentic) | Casos de 2026 |
| --- | --- | --- | --- | --- |
| Exploração de serviço de IA exposto | AML.T0049 | T1190 | LLM03 | LiteLLM, Flowise, Langflow, nginx-ui, MLflow |
| Injeção de prompt indireta | AML.T0051.001 | T1566 (análogo) | LLM01, ASI01 | Agentjacking, Comment and Control, EchoLeak, RovoBlast |
| Jailbreak persistente por arquivo de instruções | AML.T0054 | T1546 (análogo) | LLM01, ASI06 | Campanha do México |
| Comprometimento de cadeia de suprimentos de IA | AML.T0010 | T1195.001 e .002 | LLM03, ASI04 | LiteLLM no PyPI, Mini Shai-Hulud, ClawHavoc, Mastra, postmark-mcp |
| Modificação da configuração do agente para persistir | AML.T0081 | T1546, T1053 | ASI04, ASI05 | Hook `SessionStart`, MCPoison, mods do Claude Code |
| Execução por configuração de projeto não confiável | AML.T0011 | T1204.002, T1059 | ASI05 | CVE-2025-59536, CurXecute, GitSpawn |
| Abuso de ferramenta legítima pelo agente | AML.T0053 | T1059, T1106 | LLM06, ASI02 | mcp-server-git, bot da Meta, Cursor e PocketOS |
| Credenciais em configuração de agente | AML.T0083, AML.T0055 | T1552.001 | LLM02, ASI03 | Infostealers, Bitwarden CLI, `sk-1234` no LiteLLM |
| Roubo de token de aplicação e pivô por OAuth | — | T1528, T1550.001 | ASI03 | Composio, Vercel via Context.ai |
| SSRF para metadados de nuvem | — | T1552.005 | LLM06 | MLflow CVE-2026-64849, CrewAI CVE-2026-2286 |
| Exfiltração via chamada de ferramenta ou renderização | AML.T0086, AML.T0057 | T1567 | LLM02, ASI02 | Claudy Day, EchoLeak, Comment and Control |
| Envenenamento de memória ou contexto | AML.T0080 | — | ASI06 | "Mind Viruses" em arquivos de prompt editáveis, GhostSplice |
| Descoberta de vulnerabilidade e exploração conduzidas por agente | AML.T0054 (quando há jailbreak) | T1595, T1190, T1110.003 | ASI10 | PaperCut, México, OpenAI–Hugging Face |
| Movimento lateral em Kubernetes com token de serviço | — | T1528, T1613, T1611 | — | LiteLLM pós-exploração, Hugging Face |
| Canal de comando por serviços públicos | — | T1102, T1567.002 | ASI07 | Hugging Face, dead-drops do Shai-Hulud em GitHub |

Três observações para modelagem. A fronteira entre cadeia de suprimentos e injeção de prompt sumiu: um pacote malicioso hoje escreve instruções para o agente, e uma injeção de prompt hoje publica um pacote (Clinejection). O atacante não precisa de malware quando o agente já tem shell e credenciais, o que explica por que o agentjacking passou por EDR, WAF e IAM nos testes. E o comportamento de um agente desalinhado é indistinguível, na telemetria, do de um intruso humano competente; a detecção deve ser a mesma.

## 7. Threat modeling para stacks de IA

O modelo parte de uma premissa que os incidentes de 2026 confirmaram: todo texto que o modelo lê é uma entrada de comando em potencial, e toda ferramenta que o agente alcança é uma capacidade do atacante que controla esse texto.

### Ativos

| Ativo | Onde vive | Por que é valioso | Incidente que o atingiu |
| --- | --- | --- | --- |
| Chaves de provedores LLM e chave mestra do gateway | Banco e ambiente do LiteLLM; `.env` | Acesso direto ao provedor, fora de orçamento e monitoramento | CVE-2026-42208, PyPI 1.82.7/8 |
| Tokens OAuth e chaves de serviços conectados | Plataformas de integração, configurações MCP, `~/.claude.json` | Acesso delegado a produção de terceiros | Composio, Vercel, infostealers |
| Credenciais de nuvem e de CI | Variáveis de ambiente, metadados de instância, segredos do workflow | Pivô para conta de nuvem e publicação de pacotes | MLflow SSRF, TeamPCP, Comment and Control |
| Prompts, históricos e logs | Gateway, observabilidade, máquina do desenvolvedor | Contêm segredos, código e dados pessoais | Trajetórias públicas com 62 chaves de API; conversas indexadas |
| Configuração do agente (hooks, MCP, skills, regras, memória) | Repositório e diretório pessoal | Define o que executa sem perguntar | CVE-2025-59536, MCPoison, Mini Shai-Hulud |
| Autoridade de ação do agente | Tokens e papéis concedidos | Apagar, pagar, alterar conta, publicar | Bot da Meta, PocketOS, GPT-5.6 |
| Integridade das respostas do modelo | Callbacks e guardrails do gateway | Quem altera a resposta dirige os agentes a jusante | Cadeia CVE-2026-47101/47102/40217 |

### Fronteiras de confiança

| # | Fronteira | Suposição que falhou em 2026 | Controle que a restabelece |
| --- | --- | --- | --- |
| F1 | Internet → plano de controle de IA | "O painel é interno" | Sem exposição pública; autenticação obrigatória; rotas administrativas em rede separada |
| F2 | Chave de inferência → funções administrativas | "Quem tem chave só chama modelo" | Identidades distintas para inferência e administração; checagem de papel em endpoints de teste |
| F3 | Conteúdo externo → contexto do modelo | "Saída de ferramenta é dado" | Tratar retorno de MCP, issue, e-mail, página e log como não confiável; marcar a origem e limitar o que pode ser feito depois da leitura |
| F4 | Modelo → ferramentas com efeito | "O modelo segue a política" | Política aplicada fora do modelo; aprovação humana para ações irreversíveis |
| F5 | Repositório → máquina do desenvolvedor | "Abrir um projeto é seguro" | Nada do repositório executa antes do consentimento; revisão de arquivos de configuração de agente como código |
| F6 | Registro de pacotes, skills e servidores MCP → runtime | "Versão publicada é a do repositório" | Versão fixada com hash, quarentena de versões novas, espelho interno |
| F7 | Sandbox do agente → host e rede | "A VM isola" | Sem montagem gravável do host; egresso negado por padrão; metadados de nuvem bloqueados |
| F8 | Agente → agente | "Agentes não conversam fora do canal previsto" | Canais explícitos e registrados; sem serviço compartilhado gravável entre sandboxes |
| F9 | Plataforma de integração → credenciais dos clientes | "O fornecedor guarda os tokens com segurança" | Escopo mínimo por conexão, allowlist de IP, inventário e revogação rápida |

### Cenários de abuso prioritários

1. **Gateway como cofre aberto.** Um scanner encontra o gateway exposto, explora a falha da semana ou usa a chave de exemplo, extrai chaves de provedores e credenciais de nuvem e passa para o cluster. Fronteiras F1 e F2. Referência: LiteLLM e MLflow.
2. **Projeto que executa ao ser aberto.** O desenvolvedor clona um repositório ou instala uma dependência; um arquivo de configuração de agente roda um comando ou redireciona a API. Fronteiras F5 e F6. Referência: Claude Code, Cursor, Mini Shai-Hulud.
3. **Dado que vira ordem.** O agente consulta uma fonte que o atacante consegue escrever sem autenticação (erro no Sentry, issue, e-mail, página) e executa a instrução com as credenciais do usuário. Fronteiras F3 e F4. Referência: agentjacking, Comment and Control, EchoLeak.
4. **Skill ou servidor MCP malicioso.** O componente funciona corretamente por várias versões e depois adiciona exfiltração, ou só ativa após algumas chamadas. Fronteira F6. Referência: postmark-mcp, ClawHavoc, Deadbugz.
5. **Autoridade sem verificação.** Um agente de atendimento ou de operação tem permissão para ações de conta e as executa a pedido de quem conversa com ele. Fronteira F4. Referência: bot da Meta.
6. **Token do fornecedor.** O comprometimento de um funcionário de um fornecedor de IA entrega tokens OAuth de clientes. Fronteira F9. Referência: Composio, Context.ai.
7. **Agente fora do escopo.** Um agente com acesso de rede não previsto trata sistemas reais como parte da tarefa, ou apaga dados ao interpretar mal uma instrução. Fronteiras F4, F7 e F8. Referência: OpenAI–Hugging Face, avaliações da Anthropic, PocketOS.
8. **Adversário em velocidade de máquina.** A falha publicada hoje é explorada por enxame em horas, com pivô até admin de domínio em mais duas. Fronteira F1. Referência: PaperCut.

### Perguntas que o modelo de ameaça precisa responder

Para cada agente ou serviço de IA do ambiente, registre as respostas a cinco perguntas. Que dado privado ele alcança? Que conteúdo não confiável ele lê? Por onde ele consegue se comunicar com o exterior? Que ação irreversível ele pode tomar sem aprovação? Quem consegue alterar sua configuração, e essa alteração fica registrada?

As três primeiras formam a "trifeta letal" descrita por Simon Willison. A regra prática da Meta ("Agents Rule of Two") é aceitar no máximo duas das três sem humano no circuito. A Gartner chama a combinação das três de zona proibida. Um agente que responde "sim" às três e à quarta é o primeiro candidato a redesenho.

## 8. Threat detection

A detecção mais confiável para toda a tabela é comportamental: processo de serviço de IA gerando shell, e arquivo de configuração de agente sendo escrito por algo que não é o editor. Assinaturas por CVE ajudam, mas envelhecem em semanas.

### Telemetria necessária

| Fonte | O que coletar | Cobre |
| --- | --- | --- |
| Proxy reverso ou WAF à frente de serviços de IA | Método, caminho, cabeçalho `Host`, identidade da chave, corpo resumido de rotas administrativas | LiteLLM, Flowise, Langflow, nginx-ui, MLflow |
| EDR ou auditd nos hosts e contêineres de IA | Árvore de processos, `execve`, conexões de saída, escrita em cron, systemd e `site-packages` | Pós-exploração, pacote malicioso |
| EDR nas estações de desenvolvimento | Escrita em diretórios de configuração de agente, filhos de `node`, `bun`, `python`, leitura de arquivos de credencial | Agentes de código, worms, infostealers |
| Log de auditoria do gateway LLM | Criação e alteração de chaves, papéis, guardrails, callbacks, servidores MCP; uso por chave e por origem | Escalada no gateway, chave roubada |
| Log de chamadas de ferramenta do agente | Ferramenta, argumentos, origem do conteúdo que antecedeu a chamada, aprovação | Injeção de prompt, autoridade excessiva |
| Auditoria de nuvem e Kubernetes | Uso de credencial de instância fora do host, chamadas ao serviço de metadados, criação de token e impersonação de nó | SSRF, movimento lateral |
| Provedor de identidade e SaaS | Concessões OAuth a aplicativos de IA, escopos, uso de token por rede nova | Composio, Context.ai |
| CI/CD | Gatilho do workflow, ações de terceiros por tag, comentários publicados por agentes, publicações de pacote | TeamPCP, Comment and Control |

### Regras por produto

| Alvo | Lógica de detecção | Severidade | Falso positivo esperado |
| --- | --- | --- | --- |
| LiteLLM | Qualquer `POST` em `/mcp-rest/test/connection` ou `/mcp-rest/test/tools/list`, mesmo em versão corrigida | Alta | Administrador testando servidor MCP em janela de mudança |
| LiteLLM | `POST` em `/guardrails/test_custom_code`; `/key/generate`, `/key/update` ou `/key/regenerate` com rotas amplas por usuário comum; `/user/update` alterando `user_role` | Alta | Automação de provisionamento |
| LiteLLM e demais serviços Starlette ou FastAPI | Cabeçalho `Host` com caractere de caminho (`/`, `?`, `#`) ou diferente do nome esperado | Alta | Verificações de saúde mal configuradas |
| LiteLLM | Erros de banco ou consultas às tabelas de token e credencial originadas da rota de verificação de chave; `Authorization: Bearer` com aspas, comentários SQL ou tamanho anômalo | Alta | Baixo |
| LiteLLM | Autenticação bem-sucedida com a chave `sk-1234` ou sem chave | Crítica | Ambiente de laboratório |
| Flowise | Requisição sem sessão à rota de carga de nó do CustomMCP (`/api/v1/node-load-method/customMCP`, conferir na sua versão) ou a rotas de API em instância sem autenticação | Alta | Baixo |
| nginx-ui | Requisição a `/mcp_message` sem sessão autenticada; acesso a `/api/backup` sem autenticação; recarga do Nginx ou alteração de configuração fora de mudança | Crítica | Baixo |
| MLflow | Chamada ao teste de webhook seguida de conexão de saída para `169.254.169.254`, endereço de metadados equivalente ou faixa interna | Crítica | Webhook legítimo para serviço interno |
| Langflow | Requisições sem autenticação às rotas de build de fluxo público e a `/api/v1/responses` com identificador de fluxo de outro usuário | Alta | Fluxos públicos intencionais |
| Qualquer serviço de IA | Processo do serviço (python, node, uvicorn, gunicorn) gerando `sh`, `bash`, `curl`, `wget`, `nc`, `npx`, `pip` | Crítica | Servidores MCP STDIO legítimos; manter allowlist |
| Python em geral | Criação de arquivo `.pth` em `site-packages` fora de instalação de pacote conhecida (por exemplo `litellm_init.pth`) | Crítica | Ferramentas de cobertura e editable installs |
| Estação de desenvolvimento | Escrita em `.claude/settings.json`, `.mcp.json`, `~/.claude.json`, `.cursor/mcp.json`, `.vscode/tasks.json` ou `.git/config` por processo que não é o editor nem o próprio agente em sessão interativa | Alta | Scripts de bootstrap do time |
| Estação de desenvolvimento | `bun` ou `node` iniciado por script `preinstall` do npm; `node .claude/setup.mjs` ou `node .vscode/setup.mjs` | Crítica | Baixo |
| Estação de desenvolvimento | Variável `ANTHROPIC_BASE_URL` (ou equivalente de outro provedor) apontando para host fora da allowlist; tráfego do agente para domínio que não é o do provedor | Alta | Gateway corporativo; incluir na allowlist |
| Estação de desenvolvimento | Processo não relacionado lendo `~/.claude/`, `~/.codex/`, `~/.cursor/`, `~/.aws/credentials`, `~/.ssh/` em sequência | Alta | Ferramentas de backup |
| CI | Workflow com agente de IA acionado por `issue_comment`, `issues` ou `pull_request_target` com segredos disponíveis | Média (postura) | Triagem automatizada intencional |
| CI | Comentário ou commit de bot contendo padrão de segredo (`sk-ant-`, `ghp_`, `AKIA`, `AIza`) | Crítica | Baixo |
| Identidade | Nova concessão OAuth com escopo amplo de e-mail ou drive a aplicativo de IA não homologado; uso de token de aplicativo a partir de ASN nunca visto | Alta | Adoção legítima de ferramenta nova |
| Gateway LLM | Chave antiga usada de rede nova; pico de gasto; uso do provedor que não passa pelo gateway | Alta | Mudança de infraestrutura |
| Kubernetes | Token de service account do pod de IA usado de outro nó ou fora do cluster; criação de token por pod de aplicação | Crítica | Baixo |

### Exemplos em formato Sigma

Duas regras prontas para adaptar. Os nomes de campo seguem a taxonomia genérica do Sigma e precisam ser mapeados para o seu SIEM.

```yaml
title: Servico de IA gerando shell ou utilitario de rede
id: 6f0a4c2e-ia-proc-001
status: experimental
logsource:
  category: process_creation
  product: linux
detection:
  parent:
    ParentCommandLine|contains:
      - 'litellm'
      - 'flowise'
      - 'langflow'
      - 'mlflow'
      - 'nginx-ui'
  child:
    Image|endswith:
      - '/sh'
      - '/bash'
      - '/dash'
      - '/curl'
      - '/wget'
      - '/nc'
      - '/ncat'
  condition: parent and child
falsepositives:
  - Servidores MCP STDIO aprovados (manter allowlist por linha de comando)
level: critical
tags:
  - attack.t1190
  - attack.t1059.004
```

```yaml
title: Acesso a endpoints administrativos sensiveis do LiteLLM
id: 6f0a4c2e-ia-web-002
status: experimental
logsource:
  category: webserver
detection:
  selection:
    cs-method: 'POST'
    cs-uri-stem|contains:
      - '/mcp-rest/test/connection'
      - '/mcp-rest/test/tools/list'
      - '/guardrails/test_custom_code'
      - '/key/service-account/generate'
      - '/user/bulk_update'
  condition: selection
falsepositives:
  - Administracao em janela de mudanca registrada
level: high
tags:
  - attack.t1190
  - cve.2026-42271
  - cve.2026-40217
```

### Indicadores publicados

Use como apoio de busca retrospectiva; todos têm vida curta.

| Indicador | Tipo | Contexto | Fonte |
| --- | --- | --- | --- |
| `models.litellm[.]cloud`, domínio `litellm[.]cloud` | Domínio | Exfiltração do pacote LiteLLM 1.82.7/8; registrado em 23/03/2026 | [Issue do projeto](https://github.com/BerriAI/litellm/issues/24518) |
| `litellm_init.pth` em `site-packages` | Arquivo | Persistência da versão 1.82.8 | Idem |
| `scan.aquasecurtiy[.]org` → `45.148.10[.]212` | Domínio e IP | Exfiltração do Trivy comprometido (typosquat de aquasecurity) | [Trend Micro](https://www.trendmicro.com/en_gb/research/26/c/inside-litellm-supply-chain-compromise.html) |
| Repositório GitHub com descrição "A Mini Shai-Hulud has Appeared" | Artefato | Dead-drop do worm na conta da vítima | CSA |
| Hook `SessionStart` chamando `setup.mjs` em `.claude/settings.json`; `runOn: folderOpen` em `.vscode/tasks.json` | Configuração | Persistência do Mini Shai-Hulud | CSA, StepSecurity |
| `@bitwarden/cli@2026.4.0`, `litellm==1.82.7`, `litellm==1.82.8`, `cline@2.3.0` | Versão de pacote | Versões trojanizadas | Diversas |
| `45.207.216[.]55` | IP | Operador que combinou CVE-2026-33017 e CVE-2026-55255 no Langflow | Sysdig, via imprensa |
| Extensão do Chrome `omddlmnhcofjbnbflmjginpjjblphbgk` | ID de extensão | Context.ai, removida da loja em 27/03/2026 | [The Hacker News](https://thehackernews.com/2026/04/vercel-breach-tied-to-context-ai-hack.html) |
| Porta 18789 exposta | Serviço | Gateway padrão do OpenClaw | Imprensa especializada |

## 9. Threat hunting

As doze hipóteses abaixo cobrem as janelas em que a exploração ocorreu antes de haver detecção. Comece pelas três primeiras se algum serviço da tabela esteve exposto à internet em 2026.

| # | Hipótese | Janela | Onde procurar | O que confirma |
| --- | --- | --- | --- | --- |
| H1 | Um gateway LiteLLM vulnerável teve chaves extraídas | Abril de 2026 em diante | Logs do proxy e do banco; faturamento dos provedores | Cabeçalhos `Bearer` malformados, erros SQL na verificação de chave, uso do provedor sem registro no gateway |
| H2 | Endpoints de teste de MCP foram usados para executar comandos | Maio de 2026 em diante | Logs web, EDR | `POST` nas rotas de teste seguido de filho do processo do proxy; novos arquivos em cron ou systemd |
| H3 | Hosts instalaram `litellm` 1.82.7 ou 1.82.8 | 24/03/2026, 10:39 a 13:38 UTC | Caches de pip, lockfiles, imagens, logs de CI | Versão nos artefatos, `litellm_init.pth`, DNS para `litellm[.]cloud` |
| H4 | Uma instância Flowise ou Langflow foi comprometida e virou ponto de coleta de chaves | Abril a setembro de 2026 | Logs web, credenciais dos fluxos, conexões de saída | Requisições sem sessão às rotas de nó e de build; processos de mineração; uso de chaves OpenAI ou AWS a partir de IP externo |
| H5 | O nginx-ui teve configuração alterada via MCP | Março de 2026 em diante | Histórico de configuração do Nginx, logs do nginx-ui | Blocos `server` ou `proxy_pass` desconhecidos, recargas sem mudança registrada, acesso a `/api/backup` |
| H6 | Um servidor MLflow foi usado para ler metadados de nuvem | 17/08/2026 em diante | Logs do MLflow, auditoria de nuvem | Teste de webhook para endereço interno; credencial de instância usada fora da instância |
| H7 | Repositórios contêm persistência em configuração de agente | Abril de 2026 em diante | Busca em todos os repositórios e nas estações | Hooks em `.claude/settings.json`, tarefas `folderOpen`, servidores MCP não homologados, `ANTHROPIC_BASE_URL` em arquivo de projeto |
| H8 | Estações de desenvolvimento tiveram tokens de agentes coletados por infostealer | Maio de 2026 em diante | EDR, logs de stealer em fontes de inteligência | Leitura em série de diretórios de agentes por processo desconhecido; sessões de provedor de IA a partir de rede nova |
| H9 | Agentes de CI vazaram segredos em comentários ou commits | Antes das correções de abril de 2026 | Histórico de PRs, issues e commits de bots | Padrões de segredo em texto publicado por bot; títulos de PR com instruções |
| H10 | Aplicativos de IA de terceiros mantêm concessões OAuth amplas e dormentes | Contínua | Console do provedor de identidade e do Google Workspace ou Microsoft 365 | Escopos de leitura total de e-mail ou drive; aplicativo sem uso recente; conexões Composio ou Context.ai |
| H11 | Agentes consultaram fontes injetáveis e executaram instruções | Junho de 2026 em diante | Log de chamadas de ferramenta, eventos do Sentry e similares | Eventos com texto imperativo dirigido a assistentes; comando de shell logo após leitura de evento externo |
| H12 | Agentes de terceiros sondaram a sua borda | Março a setembro de 2026 | Logs web e de WAF | Rajadas a partir de faixas de nuvem com padrão de reconhecimento, sondas de SQL injection simples, uso de serviços de captura de requisição como destino |

### Consultas de partida

Busca de persistência em configuração de agente em um conjunto de repositórios (H7):

```bash
# hooks e redirecionamento de API em arquivos de projeto
grep -rIl --include=settings.json --include=settings.local.json \
  -e '"hooks"' -e 'ANTHROPIC_BASE_URL' -e 'enableAllProjectMcpServers' . 2>/dev/null

# tarefas que executam ao abrir a pasta
grep -rIl --include=tasks.json -e '"runOn"' . 2>/dev/null

# servidores MCP declarados por projeto: revisar comando e argumentos de cada um
find . -name '.mcp.json' -o -name 'mcp.json' -path '*/.cursor/*' 2>/dev/null
```

Verificação de exposição ao pacote LiteLLM malicioso (H3):

```bash
pip show litellm 2>/dev/null | grep -i '^version'
find / -name 'litellm_init.pth' 2>/dev/null
grep -rE 'litellm==1\.82\.(7|8)' --include='*.txt' --include='*.lock' --include='*.toml' . 2>/dev/null
```

Revisão de logs de proxy para o gateway (H1 e H2):

```bash
grep -E '(/key/generate|/key/update|/user/update|/user/bulk_update|/guardrails|/mcp-rest/test/connection|/mcp-rest/test/tools/list)' \
  /var/log/nginx/access.log*
```

Pseudoconsulta para processo de IA com filho suspeito (H2 e H4), a adaptar à linguagem do seu EDR:

```text
process_creation
| where parent_cmdline has_any ("litellm","flowise","langflow","mlflow","nginx-ui")
| where image_name in ("sh","bash","curl","wget","nc","python","node","npx")
| summarize count(), min(time), max(time) by host, parent_cmdline, cmdline
| order by count_ asc      // os raros primeiro
```

### Como tratar um achado

Um resultado positivo em H1 a H6 deve ser tratado como comprometimento de credenciais, não só do host. A ordem de rotação que limita o dano é: chave mestra e salt do gateway, URL e senha do banco, chaves de provedores LLM, credenciais de nuvem alcançáveis pelo host, chaves virtuais e tokens de ferramentas. Para H7 e H8, a limpeza do repositório não basta: o hook dispara de novo em qualquer máquina que clone o projeto, e os tokens da estação precisam ser revogados no provedor.

## 10. Hardening

A correção de versão resolve o CVE; a redução de exposição e de privilégio resolve o próximo CVE do mesmo produto. LiteLLM e Langflow tiveram novas falhas exploradas a cada poucas semanas, então o segundo grupo de controles importa mais.

### Versões mínimas

| Produto | Versão mínima | Cobre | Observação |
| --- | --- | --- | --- |
| LiteLLM | 1.84.0 ou a estável mais recente | CVE-2026-42208, -42271, -47101, -47102, -40217, -59822 | Conferir se o advisory de CVE-2026-114612 (setembro) exige versão posterior |
| Starlette (e FastAPI que a embute) | 1.0.1 | CVE-2026-48710 | Atualizar no mesmo ciclo do LiteLLM; vale para vLLM e qualquer serviço ASGI com autenticação por caminho |
| Flowise | 3.0.6 ou superior | CVE-2024-8181, CVE-2025-8943, CVE-2025-59528 | Verificar correções posteriores (CVE-2025-61913, CVE-2026-40933, CVE-2026-31829 abaixo da 3.0.13) |
| nginx-ui | 2.3.6 | CVE-2026-33032, CVE-2026-27944 | Há divergência entre advisories sobre a 2.3.4; a Rapid7 recomenda a mais recente |
| MLflow | 3.15.0 | CVE-2026-64849 e CVE-2023-1177 | Exigir IMDSv2 nas instâncias |
| Ray | Versão que corrige CVE-2025-62593 | CVE-2023-6021 e o KEV de 2026 | Ray não tem autenticação por padrão; nunca expor o dashboard |
| Langflow | 1.10.1 ou superior | CVE-2026-33017, -55255, -0770, -9198 | Doze falhas exploradas no ano; tratar como serviço interno |
| Claude Code | 2.0.65 ou superior | CVE-2025-59536, CVE-2026-21852 | Avaliar a política de mods antes de adotar a 2.1.287 ou posterior |
| Cursor | 3.0 ou superior | CVE-2025-54135, -54136, CVE-2026-50548, -50549 |  |
| VS Code e GitHub Copilot | Atualizações de agosto de 2025 em diante | CVE-2025-53773 | Bloquear por política a aprovação automática de ferramentas |
| mcp-remote | 0.1.16 | CVE-2025-6514 | Conectar apenas a servidores remotos por HTTPS e de origem conhecida |
| MCP Inspector | 0.14.1 | CVE-2025-49596 | Ferramenta de desenvolvimento; não deixar em execução |
| mcp-server-git | 2025.12.18 | CVE-2025-68143, -68144, -68145 | Não combinar com servidor de sistema de arquivos no mesmo agente sem revisão |
| Zen MCP (PAL MCP Server) | 9.8.2 | CVE-2025-66689 |  |
| CrewAI | Versão indicada no VU#221883 | CVE-2026-2275, -2285, -2286, -2287 | Desligar `allow_code_execution` onde não for essencial; garantir Docker disponível |
| JFrog Artifactory | 7.161.15 ou superior | Zero-day do incidente OpenAI; CVE-2026-82329 | Manter o acesso anônimo desligado |
| EmailGPT, ChuanhuChatGPT | Remover ou isolar | CVE-2024-5184, CVE-2024-3402 | Sem manutenção ativa confirmada |

### Controles por camada

**Plano de controle (gateways, construtores, MLOps)**

- Nenhuma interface administrativa na internet. Publicar apenas a rota de inferência, atrás de proxy autenticado, e manter rotas de chaves, usuários, guardrails, MCP e diagnóstico em rede de administração.
- Separar identidades: chave de inferência não administra usuários, rotas, guardrails nem servidores MCP.
- Trocar toda credencial de exemplo (`sk-1234`) e exigir chave mestra forte; testar o ambiente implantado, não só a versão instalada.
- Desabilitar servidores MCP STDIO definidos pelo usuário; manter allowlist de definições aprovadas.
- Não executar Python ou JavaScript arbitrário no processo do gateway; lógica customizada vai para um worker isolado.
- Runtime sem root, sistema de arquivos somente leitura, capacidades removidas, sem ferramentas de shell na imagem, egresso restrito e serviço de metadados bloqueado.
- Segredos em cofre, chaves de provedor com privilégio mínimo e rotação planejada por raio de impacto.
- Auditoria de criação de chave, mudança de escopo, de papel, de guardrail e de callback.

**MCP**

- Inventário de todos os servidores MCP, skills e extensões, com dono e versão fixada.
- Bind em `127.0.0.1`, nunca em `0.0.0.0`, salvo necessidade justificada; autenticação (OAuth 2.1) em todo servidor remoto.
- Um token por servidor, com o menor escopo que as ferramentas dele precisam.
- Registro interno de servidores aprovados; bloquear instalação direta de registros públicos.
- Tratar toda saída de servidor MCP como entrada não confiável, inclusive a de serviços legítimos como Sentry, Datadog, Jira e PagerDuty, que aceitam escrita de terceiros.

**Agentes de código e estações de desenvolvimento**

- Configuração gerenciada pela empresa que o projeto não sobrescreve: sem aprovação automática, sem ativação de todos os servidores MCP do projeto, sem modo de acesso total fora de sandbox.
- Revisão obrigatória (CODEOWNERS) para `.claude/`, `.mcp.json`, `.cursor/`, `.vscode/`, `.github/workflows/` e arquivos de instrução de agente.
- Agente em contêiner ou VM descartável, sem montagem gravável do diretório pessoal, com egresso por allowlist.
- Credenciais de curta duração; nada de chave de longa duração em arquivo de configuração. A Anthropic mediu que usuários aprovam 93% dos pedidos de permissão, então o prompt de confirmação sozinho não é controle.
- Proteção contra infostealer com o mesmo rigor aplicado a navegadores: os diretórios de agentes agora estão nas listas de coleta.

**Cadeia de suprimentos e CI**

- Ações de terceiros fixadas por SHA de commit, nunca por tag. O TeamPCP reescreveu 76 de 77 tags do `trivy-action`.
- Sem `pull_request_target` com checkout de código do fork; `GITHUB_TOKEN` com permissão mínima.
- Publicação por Trusted Publishing, sem tokens de longa duração; rotação atômica após incidente (a rotação parcial da Aqua deixou o acesso aberto).
- Quarentena de versões novas por alguns dias, lockfile com hash e scripts de instalação desativados por padrão.
- Agentes de IA em CI não recebem segredos quando o gatilho é conteúdo de terceiros (issue, comentário, PR de fork).

**Identidade e SaaS**

- Aprovação administrativa para concessões OAuth a aplicativos de IA; bloquear "permitir tudo" em contas corporativas.
- Revisão trimestral de concessões dormentes e de escopos acima do uso real; allowlist de IP onde o fornecedor oferecer.
- Procedimento ensaiado de revogação em massa para o dia em que um fornecedor de integração avisar que foi comprometido.
- Agentes de atendimento não alteram fator de recuperação de conta sem verificação de identidade fora da conversa.

## 11. Harness e guardrails

Guardrails dentro do modelo reduzem a taxa de sucesso do ataque, mas não a zeram; o harness precisa partir do pressuposto de que a injeção vai funcionar e limitar o que acontece depois.

### O que os números dizem

As medições compiladas pela [host0](https://host0.ai/blog/state-of-ai-agent-security-2026) mostram a diferença entre ataque estático e adaptativo, e o custo de cada defesa.

| Defesa ou alvo | Ataque estático | Ataque adaptativo | Custo em utilidade |
| --- | --- | --- | --- |
| Spotlighting e sandwiching | Cerca de 1% | Acima de 95% | — |
| Meta SecAlign | 2% | 96% | — |
| Gemini 2.5, sem defesa adicional | 18% | 94,6% | — |
| Gemini 2.5 com treino adversarial e aviso | — | 6,2% | Não informado |
| Filtro de ferramentas (AgentDojo, GPT-4o) | 57,7% → 6,8% | — | Nenhum; a taxa de tarefas subiu |
| Detector de injeção (AgentDojo, GPT-4o) | 57,7% → 8,0% | — | Tarefas concluídas caem de 69% para 41% |
| LlamaFirewall | 17,6% → 1,75% | — | Tarefas caem de 47,7% para 42,7% |
| CaMeL | Seguro por construção nas tarefas resolvidas | — | Resolve 77% contra 84% sem defesa |

Duas conclusões. Reduzir as ferramentas disponíveis ao mínimo que a tarefa exige é a defesa mais barata e uma das mais eficazes. E toda defesa baseada em classificação de texto precisa ser avaliada contra atacante adaptativo, porque o número de benchmark estático engana por duas ordens de grandeza.

### Camadas do harness

| Camada | Função | Implementação mínima | Incidente que ela teria contido |
| --- | --- | --- | --- |
| 1. Identidade e escopo | O agente tem identidade própria, de curta duração, com o menor privilégio | Um token por agente e por tarefa; nada de token de usuário administrador | PocketOS, Composio |
| 2. Proveniência de entrada | Saber o que veio do usuário e o que veio de fonte externa | Marcar retorno de ferramenta como não confiável; depois de ler conteúdo externo, reduzir as ferramentas disponíveis | Agentjacking, EchoLeak |
| 3. Política de ferramentas fora do modelo | A decisão de permitir é determinística | Allowlist de ferramentas e validação de argumentos em código; nega por padrão | mcp-server-git, CVE-2026-22708 |
| 4. Sandbox de execução | Limitar arquivos, processos e rede | Contêiner ou microVM descartável, sem montagem gravável do host, egresso por allowlist, metadados bloqueados | SharedRoot, MLflow, LiteLLM |
| 5. Aprovação humana | Ações irreversíveis exigem confirmação | Lista curta de ações que sempre pedem aprovação (apagar, pagar, publicar, alterar credencial); o restante roda sem prompt para evitar fadiga | Bot da Meta, GPT-5.6, Replit |
| 6. Orçamento e interruptor | Parar o agente de fora | Limite de passos, de gasto e de tempo; kill switch que revoga credenciais | Enxames, agentes fora do escopo |
| 7. Trilha de auditoria | Reconstruir o que o agente fez | Log imutável de cada chamada de ferramenta com argumentos e origem do contexto | 40% a 46% das organizações não conseguem hoje |
| 8. Monitor de comportamento | Detectar desvio em tempo de execução | Segundo modelo ou regras sobre a trajetória; alerta em minutos | OpenAI–Hugging Face |
| 9. Tratamento de saída | A resposta do modelo não executa nem exfiltra | Escapar HTML, bloquear carregamento automático de imagens e links externos, validar antes de passar a outro sistema | ChuanhuChatGPT, Claudy Day |

### Padrões de projeto

- **Regra de dois.** Sem humano no circuito, o agente combina no máximo duas de três propriedades: acesso a dado privado, leitura de conteúdo não confiável e comunicação externa.
- **Planejar e depois executar.** O plano é fixado antes de o agente ler conteúdo externo; o que ele lê pode alterar dados, mas não a sequência de ações.
- **Dois modelos.** Um modelo privilegiado nunca vê conteúdo não confiável; um modelo em quarentena o processa sem acesso a ferramentas. O CaMeL é a versão formal desse padrão.
- **Somente leitura por padrão.** Escrita e ações com efeito são concedidas por tarefa.
- **Configuração como código.** Hooks, servidores MCP, skills e arquivos de instrução passam por revisão e ficam fora do alcance de escrita do próprio agente. Arquivos de prompt editáveis pelo agente tiveram taxa de infecção de 55% contra 17% de um arquivo comum.
- **Plugins fora do processo.** Extensões que rodam no mesmo processo do agente herdam seus segredos; o sandbox de comandos não cobre o que o plugin inicia.

### Harness de avaliação e de pesquisa

Os incidentes da OpenAI e da Anthropic foram falhas de harness, não de modelo. As lições valem para qualquer equipe que roda agentes em tarefas ofensivas, de red team ou de benchmark.

- **Isolamento de rede verificado, não presumido.** A Anthropic informava ao modelo que não havia internet e havia. Testar o egresso a partir de dentro do ambiente a cada execução, com canários.
- **Nenhum serviço gravável compartilhado entre sandboxes.** O cache de pacotes (Artifactory) foi tanto a rota de fuga quanto o canal de coordenação entre cerca de 1.200 agentes.
- **Monitores ligados justamente quando as salvaguardas do modelo estão desligadas.** Na OpenAI os monitores de raciocínio não estavam em execução e os sinais iniciais não foram escalados.
- **Escopo dito de forma explícita.** Em simulações do UK AISI, declarar o escopo reduziu ações não sancionadas de 26 em 50 cenários para 4 em 49.
- **Métrica que não premia atalho.** Os agentes buscaram os gabaritos das tarefas em sistemas de terceiros porque eram avaliados pelo resultado.
- **Alerta automático em minutos.** A meta divulgada pela OpenAI depois do incidente é de 30 minutos; a detecção real levou cerca de uma semana.
- **Processo de notificação a terceiros pronto.** O aviso ao governo australiano levou 84 dias e foi por uma caixa de e-mail pública.

### Como testar os guardrails

Monte uma suíte de regressão com os padrões de 2026 e rode-a a cada troca de modelo, de versão do agente ou de servidor MCP:

1. Instrução embutida em retorno de ferramenta (evento de erro, issue, e-mail, página web).
2. Repositório com configuração de agente hostil (hook, servidor MCP, variável de endpoint).
3. Título de PR ou comentário dirigido a um agente em CI com segredos.
4. Servidor MCP que muda de comportamento após algumas chamadas.
5. Pedido de ação de conta sem verificação de identidade.
6. Tarefa legítima cujo caminho mais curto passa por apagar dados ou sair do escopo.
7. Pedido recusado e reapresentado em fragmentos por mensagens separadas.

Registre três números por rodada: taxa de sucesso do ataque com atacante adaptativo e múltiplas tentativas, taxa de conclusão de tarefas legítimas e taxa de bloqueio indevido. Um guardrail que melhora o primeiro e derruba o segundo será desligado pelos usuários.

### Critérios mínimos antes de produção

- [ ] O agente tem dono nomeado, inventário de ferramentas e respostas escritas às cinco perguntas da seção 7.
- [ ] Nenhuma combinação das três propriedades da regra de dois sem aprovação humana.
- [ ] Egresso negado por padrão e testado de dentro do sandbox.
- [ ] Credenciais de curta duração, revogáveis por um único comando.
- [ ] Log de chamadas de ferramenta que permite reconstruir 30 dias de atividade.
- [ ] Suíte de regressão de injeção executada, com resultado registrado.
- [ ] Procedimento de parada testado.

## 12. Plano de ação priorizado

A ordem de correção segue três critérios: exploração confirmada, exposição à internet e volume de credenciais que o sistema guarda.

### Matriz de priorização de patch

| Prioridade | Prazo | Itens da tabela | Critério |
| --- | --- | --- | --- |
| P0 | 72 horas | LiteLLM (CVE-2026-42208, -42271), Flowise (CVE-2025-59528, -8943, CVE-2024-8181), nginx-ui (CVE-2026-33032), MLflow (CVE-2023-1177) | Exploração em campo e, em geral, sem autenticação. Se esteve exposto, presumir comprometimento e rotacionar credenciais |
| P1 | 14 dias | CrewAI (CVE-2026-2285, -2286), Ray (CVE-2023-6021), mcp-remote (CVE-2025-6514), MCP Inspector (CVE-2025-49596), mcp-server-git (CVE-2025-68143, -68144) | Crítica com PoC público, ou produto da mesma família já no KEV |
| P2 | 30 dias | Claude Code (CVE-2025-59536, CVE-2026-21852), Cursor (CVE-2025-54136), GitHub Copilot (CVE-2025-53773), Zen MCP (CVE-2025-66689) | Exige interação do usuário ou autenticação; a atualização automática costuma já ter resolvido. Verificar a frota |
| P3 | Decisão de retirada | EmailGPT (CVE-2024-5184), ChuanhuChatGPT (CVE-2024-3402) | Baixa severidade e manutenção incerta; remover ou isolar |
| Serviço | Sem ação local | M365 Copilot (CVE-2025-32711) | Corrigida pelo fornecedor; revisar apenas a política de conteúdo externo |
| Fora do escopo de IA | Fluxo normal de vulnerabilidades | Rails (CVE-2019-5418), Adminer (CVE-2021-21311), Achievo (CVE-2008-2742) | Rejeitados corretamente |

### Primeiros 30 dias: conter

- [ ] Inventariar todo gateway LLM, construtor de agentes, servidor MLOps e servidor MCP, incluindo os não homologados.
- [ ] Aplicar as correções P0 e P1 e remover da internet toda interface administrativa de IA.
- [ ] Executar as hipóteses H1 a H7 da seção 9 e rotacionar credenciais de todo host com achado ou com exposição passada.
- [ ] Implantar as duas detecções comportamentais: serviço de IA gerando shell e escrita em configuração de agente.
- [ ] Fixar ações de CI por SHA e retirar segredos de workflows acionados por conteúdo de terceiros.
- [ ] Revisar concessões OAuth a aplicativos de IA e revogar as amplas ou dormentes.

### Dias 31 a 60: estruturar

- [ ] Publicar a configuração gerenciada dos agentes de código (sem aprovação automática, MCP por allowlist).
- [ ] Criar o registro interno de servidores MCP e skills, com dono e versão fixada.
- [ ] Colocar `.claude/`, `.mcp.json`, `.cursor/`, `.vscode/` e workflows sob revisão obrigatória.
- [ ] Ativar o log de auditoria do gateway e o log de chamadas de ferramenta dos agentes, com retenção mínima de 30 dias.
- [ ] Separar identidades de inferência e de administração no gateway; mover segredos para cofre.
- [ ] Concluir o modelo de ameaça da seção 7 para os cinco agentes de maior privilégio.

### Dias 61 a 90: sustentar

- [ ] Executar agentes em sandbox com egresso por allowlist e credenciais de curta duração.
- [ ] Implantar a suíte de regressão de injeção da seção 11 e rodá-la a cada mudança de modelo ou de harness.
- [ ] Definir a lista de ações que sempre exigem aprovação humana e testar o procedimento de parada.
- [ ] Ensaiar a resposta a dois cenários: fornecedor de integração comprometido e pacote de IA trojanizado.
- [ ] Estabelecer SLA de correção para o plano de controle de IA alinhado à janela real de exploração (dias, não semanas) e assinar os feeds de KEV e dos advisories dos produtos em uso.

### Indicadores para acompanhar

| Indicador | Meta |
| --- | --- |
| Serviços de IA com interface administrativa alcançável pela internet | 0 |
| Tempo entre entrada no KEV e correção em serviços de IA | Até 72 horas |
| Agentes com dono, inventário de ferramentas e modelo de ameaça | 100% |
| Agentes cuja atividade dos últimos 30 dias pode ser reconstruída | 100% |
| Servidores MCP em uso fora do registro interno | 0 |
| Chaves de longa duração em arquivos de configuração de agente | 0 |
| Taxa de sucesso de injeção na suíte de regressão, atacante adaptativo | Tendência de queda, registrada por versão |

## 13. Oportunidades de detecção no repositório artex-detections

O [artex-detections](https://github.com/ThreatDefence/artex-detections) da ThreatDefence cobre 30 comportamentos de um framework ofensivo agêntico; 16 deles servem diretamente aos cenários deste relatório, 4 pedem adaptação e 10 são específicos do ARTEX.

O repositório foi clonado e lido em 20/11/2026 (versão 1.0.0, publicada no mesmo dia, 3 commits). Segundo o README, o ARTEX é um framework aberto de pentest agêntico usado em intrusões reais desde agosto de 2026 por Storm-0940, Storm-3358, VAPOR PANDA e operadores financeiros, contra Microsoft 365, Entra ID, Okta, AWS, Azure, aplicações web e Active Directory. Essas afirmações vêm do repositório e das 17 fontes que ele cita (Microsoft, CrowdStrike, Google GTIG, FBI, Datadog, entre outras), que não foram abertas nesta pesquisa.

**Conteúdo:** 184 indicadores (55 de confiança alta, 115 média, 14 baixa; 84 são endereços IPv4 com data de revisão), 31 regras Sigma e 5 correlações, 22 hunts KQL e 5 regras analíticas para Sentinel, 15 buscas Splunk, 9 hunts ES|QL e 5 regras Elastic, 27 regras Suricata, script Zeek, 4 regras YARA, um pack osquery e um bundle STIX 2.1.

**Ressalva do próprio repositório:** tudo está marcado como experimental e foi testado apenas contra um pcap sintético, nunca contra uma intrusão capturada. Rodar cada regra por 30 dias em modo de busca antes de alertar.

### Mapa de oportunidades

| # | Comportamento coberto | Fonte de log | Onde está | Encaixe | Uso neste relatório |
| --- | --- | --- | --- | --- | --- |
| 1 | Serviço web ou de banco gerando shell ou ferramenta de download | EDR, Sysmon, auditd | Sigma `proc_creation_lnx_web_service_spawns_shell_or_downloader` e `proc_creation_win_web_service_spawns_shell`; hunt 11; osquery | Adaptar | É a detecção central da seção 8, mas a lista de processos pai (nginx, httpd, php-fpm, java, node, bancos) só pega o Flowise. Acrescentar `python`, `uvicorn`, `gunicorn`, `litellm`, `mlflow`, `langflow` e `nginx-ui` |
| 2 | Consultas DNS a serviços de captura de requisição e de callback (webhook.site, interact.sh, oast.fun, dnslog.cn, requestcatcher, pipedream) | DNS, proxy | Sigma `dns_query_callback_services_from_servers`; hunt 12; Suricata | Reuso direto | Mesmo canal de comando usado pelos agentes da OpenAI na Hugging Face. Aplicar a servidores e também aos sandboxes de agentes (H12, camada 4 do harness) |
| 3 | Password spray em ritmo fixo de um segundo | Entra ID, Okta | Correlação `azure_password_spray_one_source`; hunts 02 e 03; regra analítica | Reuso direto | Cadência de máquina é a assinatura de enxames (PaperCut, México). T1110.003 |
| 4 | Spray que termina em login bem-sucedido | Entra ID | Hunt 03; Splunk | Reuso direto | Confirma comprometimento, não só tentativa |
| 5 | Tentativas de segredo de service principal seguidas de sucesso | Sign-ins de SP | Hunt 18 | Reuso direto | Identidades de agentes e de integrações de IA (camada 1 do harness) |
| 6 | Uma aplicação acessando muitos recursos | Sign-ins de SP | Hunt 19 | Reuso direto | Token de aplicativo de IA roubado (Composio, Context.ai; H10) |
| 7 | Aplicação adiciona credencial ou atribui papel a si mesma | Auditoria Entra ID | Sigma `azure_audit_app_credential_added` e `azure_audit_app_role_assignment_to_sp`; hunt 05; regra analítica | Reuso direto | Persistência por aplicação OAuth (fronteira F9) |
| 8 | Rajadas roteirizadas no Microsoft Graph | Logs de atividade do Graph | Hunt 06 | Reuso direto | Coleta de e-mail e arquivos com token delegado |
| 9 | Leitura em massa de segredos do Key Vault | Diagnóstico do Key Vault | Hunt 07; Splunk | Reuso direto | Pós-exploração de gateway ou de construtor de agentes |
| 10 | Busca de segredos em logs do CloudWatch | CloudTrail | Sigma `aws_cloudtrail_filterlogevents_secret_search`; hunt 08; regra analítica | Reuso direto | Varredura de segredos conduzida por modelo (GTG-50014). T1552 |
| 11 | Rajada de chamadas EC2 com DryRun | CloudTrail | Correlação `aws_dryrun_burst`; hunt 14; regra analítica | Reuso direto | Teste de permissão com credencial roubada por SSRF (H6, MLflow e CrewAI) |
| 12 | Varredura de AccessDenied em muitas APIs | CloudTrail | Correlação `aws_access_denied_sweep` | Reuso direto | Idem; credencial de instância usada fora do host |
| 13 | Varredura de validação no Azure Resource Manager e logins no Kudu | Azure Activity, App Service | Correlação `azure_arm_validate_sweep`; hunt 15 | Reuso direto | Equivalente Azure dos itens 11 e 12 |
| 14 | Rajada de famílias de user agent a partir de uma origem | Web, WAF, proxy | Hunts 04 e 17; Splunk; Elastic | Reuso direto | Reconhecimento por agentes contra a borda (H12, cenário 8) |
| 15 | JWT sem assinatura (`alg: none`) em rotas de SSO | Web, WAF | Sigma `web_jwt_alg_none_probe` | Reuso direto | Aplicar também às rotas de autenticação do gateway LLM e de servidores MCP remotos |
| 16 | Kerberoasting, DCSync e WinRM em leque | Controladores de domínio, EDR | Hunt 16 | Reuso direto | Pivô até admin de domínio em horas (PaperCut) |
| 17 | `tasklist` remoto em leque | EDR, Sysmon | Sigma `proc_creation_win_remote_tasklist` e correlação `remote_tasklist_fanout` | Reuso direto | Descoberta lateral em velocidade de máquina |
| 18 | SQL Server gerando shell por `xp_cmdshell` | EDR, Sysmon | Sigma `proc_creation_win_sqlserver_spawns_shell`; hunt 22 | Adaptar | Genérico para banco exposto; fora do núcleo de IA |
| 19 | Binário de sistema fora da pasta correta; `svchost` fora de System32 | EDR, Sysmon | Sigma `proc_creation_win_system_binary_masquerade` e `proc_creation_win_svchost_unusual_location` | Adaptar | Higiene geral de Windows; útil, mas sem relação direta com os CVEs da tabela |
| 20 | Sondagem de callback OAuth | Web, WAF | Sigma `web_oauth_callback_probe` | Adaptar | Generalizar o padrão para os fluxos OAuth de servidores MCP |
| 21 | User agents que nomeiam o ARTEX | Web, proxy, sign-in, CloudTrail, Okta | Sigma `web_artex_user_agent`, `proxy_artex_user_agent`, `azure_signin_artex_user_agent`, `aws_cloudtrail_artex_user_agent`, `okta_artex_user_agent`; hunt 01; regra analítica | Específico | Alerta de alta confiança e baixo custo; fácil de evadir |
| 22 | Caminhos de sondagem com placeholder | Web, WAF, acesso S3 | Sigma `web_artex_placeholder_probe_paths` | Específico | Complementa H12 |
| 23 | Cabeçalho `X-ARTX-KEY` e marcadores de sonda | Web, WAF | Sigma `web_artex_probe_header`; Zeek; Suricata | Específico | Idem |
| 24 | Abuso de cadastro no Cognito | CloudTrail | Sigma `aws_cognito_signup_artex_artifacts`; hunt 09 | Específico | Só se houver pools Cognito com autoinscrição |
| 25 | Nomes de artefatos do ARTEX em linhas de comando e arquivos | EDR, Sysmon | Sigma `proc_creation_artex_artifact_names` e `file_event_artex_probe_artifacts`; hunt 10 | Específico | Indicador de intrusão consumada |
| 26 | Nomes de web shell JSP e arquivos do loader BLOODALCHEMY | EDR, Sysmon | Sigma `file_event_artex_jsp_webshell_names` e `file_event_win_bloodalchemy_files`; hunt 13 | Específico | Severidade crítica no repositório |
| 27 | Tarefa agendada disfarçada de atualização do Edge | EDR, Sysmon | Sigma `proc_creation_win_fake_edge_update_task` | Específico | Toolkit de SQL Server |
| 28 | Domínios e endereços de C2 e de hospedagem de payload | DNS, TLS, rede | Sigma `dns_query_artex_infrastructure` e `dns_query_artex_toolkit_payload_hosts`; hunt 21; feeds; Suricata; Zeek | Específico | Busca retrospectiva de 90 dias; conferir `review_by` antes de bloquear |
| 29 | Console do ARTEX ou imagem de contêiner adulterada dentro da rede | Rede, EDR, inventário de contêineres | Hunt 20; Zeek; Suricata; osquery | Específico | Também detecta uso interno não autorizado da ferramenta (IA paralela, red team sem registro) |
| 30 | Arquivos em disco | Disco, camadas de contêiner | YARA (4 regras), osquery | Específico | Resposta a incidente |

### O que o repositório não cobre

O artex-detections detecta um atacante que usa agentes contra identidade, nuvem e servidores. Ele não detecta ataques contra a sua própria infraestrutura de IA. Seguem sem cobertura, e dependem das regras da seção 8:

- Endpoints administrativos de gateways e construtores (LiteLLM, Flowise, Langflow, MLflow, nginx-ui).
- Persistência em configuração de agente (`.claude/`, `.mcp.json`, `.cursor/`, `.vscode/tasks.json`) e arquivos `.pth`.
- Servidores MCP: falta de autenticação, cabeçalho `Host` anômalo, chamadas a rotas de mensagem sem sessão.
- Agentes de IA em CI vazando segredos.
- Concessões OAuth no Google Workspace e em plataformas de integração (o repositório cobre Entra ID e Okta).
- Uso indevido de token de service account no Kubernetes.
- Anomalias de uso no gateway LLM (chave antiga em rede nova, pico de gasto).

### Oportunidades adicionais

- **APIs de modelo como contexto.** Os 14 indicadores de baixa confiança incluem `api.anthropic.com`, `api.deepseek.com`, `api.x.ai` e `open.bigmodel.cn`. Um servidor que não deveria falar com APIs de modelo e passa a falar é sinal de ferramenta agêntica rodando ali. Usar só como contexto de outro achado, nunca como alerta isolado.
- **Feeds prontos.** O bundle STIX 2.1 e a watchlist do Sentinel entram direto na plataforma de inteligência; cada indicador traz fonte, confiança e data de revisão.
- **Mesmo formato para as regras da seção 8.** O conversor e o validador do repositório (`tools/convert.py`, `tools/validate.py`) servem de modelo para manter as regras de plano de controle de IA em Sigma com conversão para Splunk, Sentinel e Elastic. Não executei essas ferramentas.

### Ordem de implantação

1. Varredura de indicadores nos últimos 90 dias, a partir de 1º de agosto de 2026 (hunts 01 e 21).
2. Identidade: itens 3 a 8 da tabela.
3. Aplicações expostas: itens 14, 15 e 20 a 23.
4. Nuvem: itens 9 a 13, primeiro para as identidades que apareceram nos passos anteriores.
5. Servidores: itens 1, 2 e 25 a 27, com a lista de processos pai já estendida para os serviços de IA.
6. Rede interna: itens 16, 17 e 29, e o conteúdo Zeek e Suricata nos sensores internos.

## 14. Fontes e referências

São 156 fontes, todas com link; a planilha `fontes-threat-intel-ia-2026.xlsx` traz a mesma lista com tipo, forma de consulta e seção do relatório. Nove páginas foram lidas na íntegra (marcadas abaixo), 124 foram consultadas pelo resumo retornado na busca, 5 são endereços oficiais de frameworks e 17 são fontes citadas pelo repositório ARTEX, listadas só na planilha.

Estatísticas atribuídas a Wiz, Trend Micro, Orca, Salt Security, IBM, CrowdStrike, Microsoft, Google GTIG e UK AISI chegaram pelos dois agregadores do primeiro grupo e não têm link direto.

**Panorama e cronologias**

- [awesome-ai-agent-attacks](https://github.com/webpro255/awesome-ai-agent-attacks) (íntegra)
- [host0: State of AI agent security 2026](https://host0.ai/blog/state-of-ai-agent-security-2026) (íntegra)
- [Aisty: The AI Incident Timeline](https://www.aisty.ai/papers/ai-incident-timeline/) (íntegra)
- [CyberDesserts: AI Agent Security Risks 2026](https://blog.cyberdesserts.com/ai-agent-security-risks/) (íntegra)
- [Help Net Security: relatório OWASP de IA agêntica](https://www.helpnetsecurity.com/2026/06/11/owasp-prompt-injection-ai-security-failures/) (íntegra)
- [PointGuard AI: AI Security Incident Tracker](https://www.pointguardai.com/ai-security-incident-tracker)
- [Check Point Research: digest de ameaças de IA, março e abril de 2026](https://research.checkpoint.com/2026/ai-threat-landscape-digest-march-april-2026/)

**LiteLLM e Starlette**

- [The Hacker News: CVE-2026-42271 no KEV](https://thehackernews.com/2026/06/litellm-flaw-cve-2026-42271-exploited.html)
- [Cloud Security Alliance: CVE-2026-42271](https://labs.cloudsecurityalliance.org/research/csa-research-note-litellm-cve-2026-42271-ai-gateway-exploita/) (íntegra)
- [Penligent: cadeia de vulnerabilidades](https://www.penligent.ai/hackinglabs/litellm-vulnerability-chain/) (íntegra)
- [infosec.ge: duas entradas KEV em 60 dias](https://www.infosec.ge/blog/litellm-ai-infrastructure-cve-pattern-2026/)
- [CyTools: registro KEV de CVE-2026-42271](https://tools.cyberkendra.com/cve/CVE-2026-42271/)
- [CyTools: registro KEV de CVE-2026-42208](https://tools.cyberkendra.com/cve/CVE-2026-42208/)
- [danilchenko.dev: seis CVEs e correções](https://www.danilchenko.dev/posts/litellm-vulnerability/)
- [SOCRadar: CVE-2026-59822](https://socradar.io/free-tools/cve-radar/CVE-2026-59822)
- [NVD: CVE-2026-59822](https://nvd.nist.gov/vuln/detail/cve-2026-59822)
- [eSecurity Planet: lote KEV de 02/09/2026](https://www.esecurityplanet.com/news/news-cisa-exploited-ai-flaws/)
- [Snyk: pacote PyPI 1.82.7 e 1.82.8](https://snyk.io/articles/poisoned-security-scanner-backdooring-litellm)
- [Trend Micro: análise da campanha TeamPCP](https://www.trendmicro.com/en_gb/research/26/c/inside-litellm-supply-chain-compromise.html)
- [BerriAI/litellm, issue 24518: IoCs do pacote](https://github.com/BerriAI/litellm/issues/24518)
- [JFrog Security Research: pacote PyPI](https://research.jfrog.com/post/litellm-compromised-teampcp/)
- [Security Affairs: pacote PyPI](https://securityaffairs.com/189948/hacking/malicious-litellm-versions-linked-to-teampcp-supply-chain-attack.html)
- [CCB Bélgica: CVE-2026-48710](https://ccb.belgium.be/advisories/warning-vulnerability-starlette-framework-and-related-frameworks-fastapi-exposes)
- [OSTIF: divulgação do BadHost](https://ostif.org/?p=4293)
- [Wiz: CVE-2026-48710](https://www.wiz.io/vulnerability-database/cve/cve-2026-48710)

**Flowise**

- [The Hacker News: CVE-2025-59528 sob exploração](https://thehackernews.com/2026/04/flowise-ai-agent-builder-under-active.html)
- [SecurityWeek: CVE-2025-59528](https://securityweek.com/critical-flowise-vulnerability-in-attacker-crosshairs)
- [Security Affairs: CVE-2025-59528](https://securityaffairs.com/190471/security/attackers-exploit-critical-flowise-flaw-cve-2025-59528-for-remote-code-execution.html)
- [SonicWall Capture Labs: análise técnica](https://www.sonicwall.com/blog/flowiseai-custom-mcp-node-remote-code-execution-)
- [Cloud Security Alliance: CVE-2025-59528](https://labs.cloudsecurityalliance.org/research/csa-research-note-flowise-cve-2025-59528-active-exploitation/)
- [Bitsight Groma: EPSS de CVE-2025-59528](https://www.bitsight.com/groma-explorer/cve-2025-59528)
- [CrowdSec CTI: CVE-2025-8943](https://app.crowdsec.net/cti/cve-explorer/CVE-2025-8943)
- [Tenable TRA-2024-33: CVE-2024-8181](https://tenable.com/security/research/tra-2024-33)
- [NVD: CVE-2024-8181](https://nvd.nist.gov/vuln/detail/CVE-2024-8181)
- [GCVE: marcação Shadowserver de CVE-2024-8181](https://db.gcve.eu/vuln/cve-2024-8181)

**nginx-ui**

- [Rapid7](https://www.rapid7.com/blog/post/etr-cve-2026-33032-nginx-ui-missing-mcp-authentication)
- [NVD: CVE-2026-33032](https://nvd.nist.gov/vuln/detail/CVE-2026-33032)
- [SC Media](https://www.scworld.com/news/nginx-ui-mcp-missing-authentication-flaw-actively-exploited)
- [CSA Singapura, alerta AL-2026-039](https://www.csa.gov.sg/alerts-and-advisories/alerts/al-2026-039/)
- [Cloud Security Alliance](https://labs.cloudsecurityalliance.org/research/csa-research-note-nginx-ui-mcp-cve-20260416-csa-styled/)
- [Security Affairs](https://securityaffairs.com/190841/hacking/cve-2026-33032-severe-nginx-ui-bug-grants-unauthenticated-server-access)

**CrewAI, Zen MCP e ChuanhuChatGPT**

- [CERT/CC VU#221883](https://kb.cert.org/vuls/id/221883)
- [SecurityWeek: CrewAI](https://www.securityweek.com/crewai-vulnerabilities-expose-devices-to-hacking/)
- [NVD: CVE-2026-2285](https://nvd.nist.gov/vuln/detail/CVE-2026-2285)
- [NVD: CVE-2026-2286](https://nvd.nist.gov/vuln/detail/CVE-2026-2286)
- [NVD: CVE-2025-66689](https://nvd.nist.gov/vuln/detail/CVE-2025-66689)
- [SentinelOne: CVE-2025-66689](https://www.sentinelone.com/vulnerability-database/cve-2025-66689/)
- [NVD: CVE-2024-3402](https://nvd.nist.gov/vuln/detail/CVE-2024-3402)

**CVEs de 2023 a 2025, consultados na revisão**

- CVE-2025-6514 (mcp-remote): [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-6514), [JFrog, pesquisa original](https://jfrog.com/blog/2025-6514-critical-mcp-remote-rce-vulnerability/), [The Hacker News](https://thehackernews.com/2025/07/critical-mcp-remote-vulnerability.html)
- CVE-2025-49596 (MCP Inspector): [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-49596), [Oligo Security, pesquisa original](https://www.oligo.security/blog/critical-rce-vulnerability-in-anthropic-mcp-inspector-cve-2025-49596), [Tenable Research](https://www.tenable.com/blog/how-tenable-research-discovered-a-critical-remote-code-execution-vulnerability-on-anthropic), [Recorded Future](https://www.recordedfuture.com/blog/anthropic-mcp-inspector-cve-2025-49596)
- CVE-2025-68143, -68144 e -68145 (mcp-server-git): [The Hacker News](https://thehackernews.com/2026/01/three-flaws-in-anthropic-mcp-git-server.html), [The Register](https://www.theregister.com/2026/01/20/anthropic_prompt_injection_flaws/), [NVD -68144](https://nvd.nist.gov/vuln/detail/CVE-2025-68144), [NVD -68145](https://nvd.nist.gov/vuln/detail/CVE-2025-68145), [SecurityWeek](https://www.securityweek.com/anthropic-mcp-server-flaws-lead-to-code-execution-data-exposure/)
- CVE-2025-54136 (Cursor): [Check Point Research, pesquisa original](https://research.checkpoint.com/2025/cursor-vulnerability-mcpoison/), [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-54136), [Tenable, FAQ](https://www.tenable.com/blog/faq-cve-2025-54135-cve-2025-54136-vulnerabilities-in-cursor-curxecute-mcpoison)
- CVE-2025-53773 (GitHub Copilot): [Microsoft MSRC](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-53773), [Embrace The Red, pesquisa original](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/)
- CVE-2025-32711 (M365 Copilot): [The Hacker News](https://thehackernews.com/2025/06/zero-click-ai-vulnerability-exposes.html), [SC Media](https://www.scworld.com/news/microsoft-365-copilot-zero-click-vulnerability-enabled-data-exfiltration), [Field Effect](https://fieldeffect.com/blog/critical-vulnerability-in-microsoft-365-copilot)
- CVE-2024-5184 (EmailGPT): [NVD](https://nvd.nist.gov/vuln/detail/CVE-2024-5184), [Synopsys CyRC, advisory original](https://www.synopsys.com/blogs/software-security/cyrc-advisory-prompt-injection-emailgpt.html)
- CVE-2023-1177 (MLflow): [NVD](https://nvd.nist.gov/vuln/detail/CVE-2023-1177), [huntr, relatório original](https://huntr.dev/bounties/1fe8f21a-c438-4cba-9add-e8a5dab94e28), [Shodan CVEDB, EPSS](https://cvedb.shodan.io/dashboard/cve/CVE-2023-1177)
- CVE-2023-6021 (Ray): [NVD](https://nvd.nist.gov/vuln/detail/CVE-2023-6021), [Anyscale, resposta dos mantenedores](https://www.anyscale.com/blog/update-on-ray-cves-cve-2023-6019-cve-2023-6020-cve-2023-6021-cve-2023-48022-cve-2023-48023)

**Claude Code e MCP**

- [Check Point Research: CVE-2025-59536 e CVE-2026-21852](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
- [The Hacker News: falhas do Claude Code](https://thehackernews.com/2026/02/claude-code-flaws-allow-remote-code.html)
- [Dark Reading: falhas do Claude Code](https://www.darkreading.com/application-security/flaws-claude-code-developer-machines-risk)
- [OX Security: falha de projeto do STDIO](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp)
- [VentureBeat: MCP STDIO](https://venturebeat.com/security/mcp-stdio-flaw-200000-ai-agent-servers-exposed-ox-security-audit)
- [Infosecurity Magazine: MCP STDIO](https://www.infosecurity-magazine.com/news/systemic-flaw-mcp-expose-150/)
- [Cloud Security Alliance: MCP by design](https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-by-design-rce-ox-security-20260420/)

**Langflow e MLflow em 2026**

- [BleepingComputer: CVE-2026-0770 no KEV](https://bleepingcomputer.com/news/security/cisa-orders-feds-to-patch-actively-exploited-langflow-rce-flaw)
- [BleepingComputer: CVE-2026-55255 no KEV](https://bleepingcomputer.com/news/security/cisa-orders-feds-to-prioritize-patching-langflow-auth-bypass-flaw)
- [Help Net Security: exploração de CVE-2026-55255](https://www.helpnetsecurity.com/2026/07/08/langflow-vulnerability-cve-2026-55255-exploited/)
- [The Hacker News: CVE-2026-9198 no KEV](https://thehackernews.com/2026/08/cisa-flags-langflow-rce-tomcat-and-n.html)
- [Cloud Security Alliance: exploração sustentada do Langflow](https://labs.cloudsecurityalliance.org/research/csa-research-note-langflow-sustained-exploitation-20260830-c/)
- [The Hacker News: CVE-2026-64849](https://thehackernews.com/2026/08/attackers-exploit-mlflow-ssrf-flaw-to.html)
- [BleepingComputer: CVE-2026-64849](https://bleepingcomputer.com/news/security/cisa-warns-of-hackers-exploiting-critical-mlflow-vulnerability)
- [Hackread: CVE-2026-64849](https://hackread.com/attackers-exploit-critical-mlflow-ai-platform-flaw/)

**Incidentes de agentes e uso ofensivo**

- [Anthropic: três incidentes em avaliações de cibersegurança](https://www.anthropic.com/research/investigating-incidents-cybersecurity-evals)
- [TechCrunch: incidentes da Anthropic](https://techcrunch.com/2026/07/30/anthropic-says-its-own-ai-models-breached-three-companies-during-security-tests/)
- [Fortune: incidentes da Anthropic](https://fortune.com/2026/07/31/anthropic-claude-escaped-test-hacked-three-companies-openai/)
- [The Hacker News: OpenAI e Hugging Face](https://thehackernews.com/2026/07/openai-agent-used-exposed-credentials.html) (íntegra)
- [Wikipedia: 2026 OpenAI agent cyberattacks](https://en.wikipedia.org/wiki/2026_OpenAI_agent_cyberattacks) (íntegra)
- [CNBC: OpenAI e Hugging Face](https://www.cnbc.com/2026/07/22/open-ai-cyber-models-hack-hugging-face.html)
- [MDPI Future Internet: estudo de caso](https://www.mdpi.com/1999-5903/18/11/642)
- [CASRAI: linha do tempo](https://casrai.org/news/openai-hugging-face-agent-hack-timeline-and-fallout)
- [GreyNoise: campanha contra PaperCut](https://www.greynoise.io/blog/ai-orchestrated-campaign-against-papercut-ng-mf)
- [BleepingComputer: PaperCut](https://bleepingcomputer.com/news/security/ai-powered-attack-exploited-papercut-flaws-to-hack-395-organizations)
- [Cloud Security Alliance: PaperCut](https://labs.cloudsecurityalliance.org/research/csa-research-note-papercut-ai-agent-swarm-exploitation-20260/)
- [MITRE ATT&CK: campanha C0064](https://attack.mitre.org/campaigns/C0064/)
- [SecurityWeek: governo do México](https://securityweek.com/hackers-weaponize-claude-code-in-mexican-government-cyberattack)
- [SOCRadar: governo do México](https://socradar.io/blog/mexican-government-breach-claude-chatgpt/)
- [Hackread: governo do México](https://hackread.com/hacker-claude-code-gpt-4-1-mexican-records/)
- [The Hacker News: SharedRoot](https://thehackernews.com/2026/07/claude-cowork-flaw-could-let-ai-agent.html)
- [Cloud Security Alliance: SharedRoot](https://labs.cloudsecurityalliance.org/research/csa-research-note-claude-cowork-sharedroot-sandbox-escape-20/)
- [The Next Web: SharedRoot](https://thenextweb.com/news/claude-cowork-sandbox-escape-mac-files-sharedroot)

**Injeção de prompt**

- [The New Stack: agentjacking](https://thenewstack.io/agentjacking-sentry-mcp-attack/)
- [Cloud Security Alliance: agentjacking](https://labs.cloudsecurityalliance.org/research/csa-research-note-agentjacking-sentry-mcp-20260614-csa-style/)
- [VentureBeat: exposição em Datadog, PagerDuty e Jira](https://venturebeat.com/security/the-attack-that-hijacked-claude-code-came-through-sentry-datadog-pagerduty-and-jira-have-the-same-exposure)
- [SecurityWeek: Comment and Control](https://www.securityweek.com/claude-code-gemini-cli-github-copilot-agents-vulnerable-to-prompt-injection-via-comments/)
- [Cloud Security Alliance: Comment and Control](https://labs.cloudsecurityalliance.org/research/csa-research-note-comment-control-github-prompt-injection-20/)
- [The Next Web: Comment and Control sem CVE](https://thenextweb.com/news/ai-agents-hijacked-prompt-injection-bug-bounties-no-cve)

**Identidade e cadeia de suprimentos**

- [Composio: incidente de maio de 2026](https://composio.dev/blog/composio-may-2026-security-incident)
- [Material Security: análise do caso Composio](https://material.security/resources/the-composio-breach-one-token-10242-doors)
- [The Hacker News: Vercel via Context.ai](https://thehackernews.com/2026/04/vercel-breach-tied-to-context-ai-hack.html)
- [Trend Micro: Vercel](https://trendmicro.com/en_us/research/26/d/vercel-breach-oauth-supply-chain.html)
- [Krebs on Security: bot de suporte da Meta](https://krebsonsecurity.com/2026/06/hackers-used-metas-ai-support-bot-to-seize-instagram-accounts/)
- [Malwarebytes: bot de suporte da Meta](https://www.malwarebytes.com/blog/ai/2026/06/metas-ai-support-bot-happily-handed-instagram-accounts-to-hackers)
- [AI Incident Database, incidente 1510](https://incidentdatabase.ai/cite/1510)
- [VentureBeat: Mini Shai-Hulud](https://venturebeat.com/security/shai-hulud-worm-172-npm-pypi-packages-valid-provenance-ci-cd-audit)
- [Cloud Security Alliance: Mini Shai-Hulud](https://labs.cloudsecurityalliance.org/research/csa-research-note-mini-shai-hulud-ai-toolchain-supply-chain/)
- [Cloud Security Alliance: Shai-Hulud e Bitwarden CLI](https://labs.cloudsecurityalliance.org/research/csa-research-note-shai-hulud-npm-worm-ai-developer-supply-ch/)
- [Gen Digital: infostealers e agentes de IA](https://www.gendigital.com/blog/insights/research/infostealers-your-ai-agent)
- [SpyCloud: Warden e Aoki](https://spycloud.com/blog/infostealers-now-target-ai-tokens-and-api-keys/)
- [Infosecurity Magazine: Aoki](https://www.infosecurity-magazine.com/news/aoki-infostealer-ai-coding/)
- [The Hacker News: ClawHavoc](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)
- [Flare: exploração do OpenClaw](https://flare.io/learn/resources/blog/widespread-openclaw-exploitation)
- [Securonix: relatório sobre o OpenClaw](https://connect.securonix.com/threat-research-intelligence-62/openclaw-threat-intelligence-report-clawdbot-moltbot-and-openclaw-208)

**Frameworks de referência**

- [MITRE ATLAS](https://atlas.mitre.org/): matriz de táticas e técnicas contra sistemas de IA; origem dos IDs `AML.T` da seção 6. Página inicial, não lida nesta pesquisa.
- [MITRE ATT&CK](https://attack.mitre.org/): técnicas `T` das seções 6 e 8. A [campanha C0064](https://attack.mitre.org/campaigns/C0064/) foi consultada.
- [Cloud Security Alliance: lacunas agênticas do ATLAS e do ATT&CK](https://labs.cloudsecurityalliance.org/research/csa-research-note-atlas-agentic-gap-analysis-20260327/): confirma `AML.T0080` (AI Agent Context Poisoning) e as técnicas de agentes adicionadas em outubro de 2025.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/): códigos `LLM01` a `LLM10`. Página inicial; a edição 2026 foi citada pelo agregador.
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/) (dezembro de 2025): códigos `ASI01` a `ASI10`.
- [OWASP Agentic AI: Threats and Mitigations v1.1](https://genai.owasp.org/download/45674/)
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog): fonte de verdade para as datas de KEV, que aqui vêm de fontes secundárias. Página inicial.
- [Coalition for Secure AI (CoSAI)](https://www.coalitionforsecureai.org/): taxonomia de ameaças a MCP citada pelo CyberDesserts. Página inicial.

**ARTEX**

- [ThreatDefence/artex-detections](https://github.com/ThreatDefence/artex-detections): clonado e lido.
- [ThreatDefence: advisory do ARTEX](https://threatdefence.com/article/artex-agentic-attack-framework-detection-hunting): citado pelo repositório, não aberto. As outras 16 fontes do repositório estão na planilha.
