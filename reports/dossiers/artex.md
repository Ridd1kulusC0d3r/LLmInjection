---
title: "Dossiê: ARTEX, framework ofensivo agêntico em uso por vários atores"
---

![Masthead](../../assets/reports/artex.svg)

<p class="rpt-head"><span>LLMI-DS-ARTEX · v0.1 rascunho</span><span class="tlp">TLP:CLEAR</span><span>Corte 2026-11-20</span></p>

<div class="injected" markdown="1">
Rascunho para revisão. O que tem `SRC-…` está nos datasets do repositório e foi lido no original até 2026-11-10. O que tem <span class="verify">A VERIFICAR</span> veio de outra sessão de pesquisa, interrompida antes de conferir os links; nada disso entrou em `data/`.
</div>

<div class="bluf" markdown="1">
ARTEX é descrito pelas fontes como plataforma open-source multiagente, guiada por LLM, de pentest e C2. Desde o fim de agosto de 2026 aparece em operações de atores de nexo China e Coreia do Norte, de um operador sinófono com motivação financeira e de grupos de extorsão. A novidade relatada é velocidade e escala, não técnica nova: em alguns casos, acesso privilegiado em nuvem em menos de três horas. Para o defensor, a prioridade é retro-hunt de credenciais e apps OAuth desde agosto e caça a consoles ARTEX expostos nos próprios ativos.
</div>

## 1. Julgamentos-chave

| # | Julgamento | Confiança | Base |
|---|---|---|---|
| J1 | O ganho do atacante com ARTEX é cadência e escala (operação contínua, muitos alvos em paralelo), não capacidade ofensiva nova. | <span class="conf conf-high">alta</span> | `SRC-MSFT-STORM-0940-ARTEX`, `SRC-CROWDSTRIKE-VAPOR-PANDA-2026-10`, `SRC-GTIG-ARTEX-2026-10` |
| J2 | Uma ferramenta pública usada por atores de nexos diferentes enfraquece atribuição baseada em ferramenta; a presença de ARTEX não indica o ator. | <span class="conf conf-high">alta</span> | 4 atores e 3 clusters sem nome nos datasets |
| J3 | O uso atual é inicial e de baixa sofisticação, mas amplo, e a porta de entrada típica é credencial já comprometida. | <span class="conf conf-med">média</span> | `SRC-GTIG-ARTEX-2026-10` (avaliação do GTIG) |
| J4 | É provável que TAG-217, o "UnSub" da CrowdStrike e o operador da Zscaler se sobreponham; nenhuma fonte afirma que são o mesmo ator. | <span class="conf conf-low">baixa</span> | `SRC-ZSCALER-ARTEX-GLOBAL` liga os relatos sem nomear o ator |

## 2. O que é (visão do defensor)

- **Arquitetura relatada:** agentes planejador e executores (CrowdStrike); divisão de trabalho entre modelos externos, como DeepSeek, GLM e Grok (Zscaler, que avisa que os IDs de modelo não foram verificados).
- **Origem e licença:** publicado no GitHub em julho de 2026, em Go, AGPL-3.0; repositório fechado em 8 de outubro, com forks e espelhos persistindo <span class="verify">A VERIFICAR</span> (FBI FLASH 2026-11-13, Censys).
- **Superfície exposta do próprio framework:** console web em portas não padrão e imagens Docker com backdoor circulando <span class="verify">A VERIFICAR</span> (pack MalwareMustDie MMD-072; Censys contou cerca de 1.465 hosts e a Check Point, 1.608 painéis ativos).
- **Fora do escopo:** instruções de uso, implantação ou configuração.

## 3. Linha do tempo

| Data | Evento | Fonte | Confiança |
|---|---|---|---|
| 2026-07 | ARTEX publicado no GitHub | FBI FLASH, Censys <span class="verify">A VERIFICAR</span> | — |
| 2026-08 (fim) | GTIG/Mandiant observam ARTEX em resposta a incidentes: grupos de extorsão e clusters suspeitos de nexo PRC | `SRC-GTIG-ARTEX-2026-10` | <span class="conf conf-high">confirmada</span> |
| 2026-08-04 a 10-04 | Prompts recuperados de operador sinófono, setores em 19 países | `SRC-ZSCALER-ARTEX-GLOBAL` | <span class="conf conf-high">alta</span> |
| 2026-09 a 10 | Intrusões em instituições financeiras sul-coreanas (TAG-217) | `SRC-RECORDEDFUTURE-TAG-217-ARTEX`, `SRC-CROWDSTRIKE-ARTEX-SOUTH-KOREA` | <span class="conf conf-med">média</span> |
| 2026-10-08 | Repositório original fica indisponível | FBI, Datadog, Check Point <span class="verify">A VERIFICAR</span> | — |
| 2026-10-10 a 14 | Storm-0940: password spraying em 327 contas de 8 organizações | `SRC-MSFT-STORM-0940-ARTEX` | <span class="conf conf-high">alta</span> |
| 2026-10 | Comprometimento do ConnectWise Cloud Backup, atribuído pela Microsoft ao Storm-0940; app afetado não significa dado acessado | `SRC-MSFT-STORM-0940-ARTEX` | <span class="conf conf-high">alta</span> |
| 2026-10 | VAPOR PANDA: 14+ países em 11 dias, pós-exploração confirmada em 9 organizações | `SRC-CROWDSTRIKE-VAPOR-PANDA-2026-10` | <span class="conf conf-high">confirmada</span> |
| 2026-10 (fim) | Pearl Sleet e Onyx Sleet passam a usar ARTEX | `SRC-MSFT-DPRK-AI-2026-10` | <span class="conf conf-high">confirmada</span> |
| 2026-10-22 | Wiz: Storm-0940 se expande para fornecedores de TI e software | Wiz <span class="verify">A VERIFICAR</span> | — |
| 2026-11-05 | Microsoft: segredos expostos no GitHub levados ao Key Vault em minutos; Check Point "Hacking on Autopilot"; Censys "Agentic Asbestos" | <span class="verify">A VERIFICAR</span> | — |
| 2026-11-06 | Microsoft: Storm-3358 mira o setor financeiro | <span class="verify">A VERIFICAR</span> | — |
| 2026-11-09 a 12 | Datadog (AWS), Unit 42, Arctic Wolf (fork "AntiFox"), Eye Security (resposta a incidente) | <span class="verify">A VERIFICAR</span> | — |
| 2026-11-13 | FBI FLASH-20261113-001 e pack de detecção MalwareMustDie MMD-072 | <span class="verify">A VERIFICAR</span> | — |
| 2026-11-16 | GTIG: atividade agêntica cruza um limiar; PentAGI customizado na Ásia | `[LLMI-20261120-05]` <span class="verify">A VERIFICAR</span> | — |

## 4. Quem usa

| Ator | Nexo | Uso relatado | Papel da IA | Fonte |
|---|---|---|---|---|
| Storm-0940 (GTIG: UNC7228, sobreposição) | China | varredura, spraying, abuso de OAuth e Graph | autonomous-operator | `SRC-MSFT-STORM-0940-ARTEX` |
| VAPOR PANDA | China | web shells, senhas de administrador de domínio, movimento lateral | autonomous-operator | `SRC-CROWDSTRIKE-VAPOR-PANDA-2026-10` |
| Pearl Sleet | Coreia do Norte | uso em operações desde o fim de outubro | — | `SRC-MSFT-DPRK-AI-2026-10` |
| Onyx Sleet | Coreia do Norte | uso citado; a Microsoft não diz para quê numa intrusão específica | — | `SRC-MSFT-DPRK-AI-2026-10` |
| TAG-217 / UnSub | não declarado | setor financeiro sul-coreano | — | `SRC-RECORDEDFUTURE-TAG-217-ARTEX`, `SRC-CROWDSTRIKE-ARTEX-SOUTH-KOREA` |
| Operador sinófono sem nome | financeiro (provável) | 19 países, vários modelos | — | `SRC-ZSCALER-ARTEX-GLOBAL` |
| Grupos de extorsão sem nome | financeiro | reconhecimento até extorsão por roubo de dados | — | `SRC-GTIG-ARTEX-2026-10` |
| Storm-3358 | Camboja | setor financeiro | — | Microsoft 2026-11-06 <span class="verify">A VERIFICAR</span> |

**Vizinho no mesmo relatório do GTIG:** PentAGI, outro framework agêntico aberto, usado por operadores sem atribuição contra integradores e operadoras de telecom na Ásia (`CAMPAIGN-PENTAGI-ASIA-TELECOM`, confiança média).

## 5. Cadeia de ataque observada

| Fase | Técnica | Evidência |
|---|---|---|
| Acesso inicial | credenciais já comprometidas; password spraying | GTIG; Microsoft |
| Reconhecimento | varredura contínua guiada por agentes | Microsoft, CrowdStrike |
| Persistência em nuvem | abuso de aplicativos OAuth, Microsoft Graph | Microsoft |
| Execução e lateral | web shells, extração de credenciais de domínio | CrowdStrike |
| Impacto | exfiltração e extorsão | GTIG |
| Orquestração | `LLMI-T015` Agentic Attack Orchestration; `LLMI-T028` AI-Assisted Tooling Development | `relationships.json` |

## 6. O que a IA mudou de fato

- **Tempo:** acesso privilegiado em nuvem em menos de três horas em alguns casos (Microsoft).
- **Cadência:** operação 24 horas, sem pausa de turno (Microsoft).
- **Paralelismo:** 14+ países em 11 dias (CrowdStrike).
- **Limite declarado pelas fontes:** a Recorded Future diz que a evidência não estabelece quanto a IA acelerou os ataques; o GTIG chama o uso de inicial e pouco sofisticado.
- **Camada 8:** o operador deixa de executar e passa a supervisionar; o erro humano que sobra é de escolha de alvo e de higiene da própria infraestrutura (consoles expostos, imagens com backdoor). Do lado do defensor, o risco é o viés de novidade: tratar "IA" como causa quando a porta de entrada continua sendo credencial vazada.

## 7. Detecção

- **No repositório:** detecções ligadas a `LLMI-T015` (ver [playbook](../../docs/playbooks/LLMI-T015.md)).
- **Pack de terceiros:** MalwareMustDie MMD-072, licença DRL 1.1, integrado ao repositório `detectionrules` numa branch sem PR (323 regras; T4 só para hunting) <span class="verify">A VERIFICAR</span>.
- **Sinais de comportamento que não dependem de IOC:**
  - cadência de máquina nos logs de autenticação (tentativas espaçadas de forma regular, 24 horas);
  - app OAuth novo ou consentimento logo depois de uma rajada de spraying;
  - requisições duplicadas e quase simultâneas vindas de subagentes;
  - tráfego para gateways de LLM a partir de hosts de servidor.

## 8. Mitigação priorizada

| Ação | Esforço | Efeito |
|---|---|---|
| Retro-hunt de credenciais, sign-ins e apps OAuth desde 2026-08-01 | médio | encontra acesso já obtido |
| MFA resistente a phishing e bloqueio de autenticação legada | médio | corta o spraying |
| Revisão de consentimentos OAuth e apps de terceiros com acesso amplo | baixo | fecha a persistência relatada |
| Procurar consoles ARTEX expostos nos próprios ativos (só ativos autorizados) | baixo | acha infraestrutura de atacante ou uso interno não sancionado |
| Varredura de segredos em repositórios | baixo | remove o atalho descrito pela Microsoft em 05/11 |

## 9. Indicadores

Não reproduzidos aqui. Use o CSV do pack MMD-072 com o tier e a validade de cada indicador; T4 nunca vira bloqueio <span class="verify">A VERIFICAR</span>.

## 10. O que este dossiê não afirma

- **PHP2Shell não é componente do ARTEX.** É um par de falhas no interpretador PHP (CVE-2026-109618 e CVE-2026-109619), e nenhuma fonte o liga ao ARTEX <span class="verify">A VERIFICAR</span>.
- Usar ARTEX não é o mesmo que tê-lo desenvolvido.
- Os atores que usam ARTEX não estão ligados entre si por usá-lo.

## 11. Brasil e América Latina

Impacto regional não demonstrado nas fontes consultadas. Hipótese a testar: consoles ARTEX expostos em ASNs brasileiros, por consulta de leitura em Censys ou Shodan.

## 12. Mudanças propostas no repositório

- Tipo `tool` nos datasets (`TOOL-ARTEX`, `TOOL-PENTAGI`) com arestas `actor → uses → tool`, para responder "quem usa ARTEX" com uma consulta.
- Ler no original e promover as fontes <span class="verify">A VERIFICAR</span> da linha do tempo, começando por FBI FLASH, Microsoft 05/11 e 06/11, Check Point, Censys e Eye Security.
- Avaliar Storm-3358 como ator.

## 13. Fontes

| ID | Publicador | Grau | Lido no original |
|---|---|---|---|
| `SRC-GTIG-ARTEX-2026-10` | Google Threat Intelligence Group | A | sim |
| `SRC-MSFT-STORM-0940-ARTEX` | Microsoft Threat Intelligence | A | sim |
| `SRC-MSFT-DPRK-AI-2026-10` | Microsoft Threat Intelligence | A | sim |
| `SRC-CROWDSTRIKE-VAPOR-PANDA-2026-10` | CrowdStrike | A | sim |
| `SRC-CROWDSTRIKE-ARTEX-SOUTH-KOREA` | CrowdStrike | A | sim |
| `SRC-RECORDEDFUTURE-TAG-217-ARTEX` | Recorded Future | A | sim |
| `SRC-ZSCALER-ARTEX-GLOBAL` | Zscaler ThreatLabz | A | sim |

**A ler** (links como chegaram da outra sessão):
- <https://research.checkpoint.com/2026/hacking-on-autopilot-inside-artex-cybercrime-campaigns/>
- <https://www.microsoft.com/en-us/security/blog/2026/11/05/threat-actors-use-agentic-ai-tooling-to-find-and-abuse-exposed-secrets/>
- <https://labs.eye.security/how-we-defended-against-an-ai-driven-attack/>
- <https://cloud.google.com/blog/topics/threat-intelligence/agentic-threat-activity-crosses-a-significant-threshold>
- Censys "Agentic Asbestos", Datadog Security Labs, Unit 42, Arctic Wolf (AntiFox), FBI FLASH-20261113-001 e JPCERT AT-2026-0030: os endereços chegaram truncados.
