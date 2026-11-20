---
title: "Dossiê: ARTEX, framework ofensivo agêntico em uso por vários atores"
---

![Masthead](../../assets/reports/artex.svg)

<p class="rpt-head"><span>LLMI-DS-ARTEX · v0.3</span><span class="tlp">TLP:CLEAR</span><span>Corte 2026-11-20</span></p>

<div class="injected" markdown="1">
v0.3 (2026-11-20): todas as fontes de outubro e novembro citadas foram lidas no original e estão em `data/` com ID `SRC-…`, exceto o boletim da Arctic Wolf sobre o AntiFox, conhecido aqui pela nota da Cloud Security Alliance (grau B). O ARTEX agora é um objeto do grafo: `TOOL-ARTEX`, com arestas `uses-tool` vindas de 14 campanhas e incidentes.
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
- **Origem:** publicado no GitHub pelo desenvolvedor "Autumn-27" em julho de 2026, escrito em Go; o autor tornou o repositório indisponível em 8 de outubro, depois dos relatos de abuso, mas forks, cópias arquivadas, variantes locais e uma versão comercial (ARTEX PRO) continuam circulando (`SRC-FBI-FLASH-20261113-ARTEX`; a Datadog fala em mais de 12 mil forks, `SRC-DATADOG-ARTEX-AWS`).
- **Modelos:** não traz modelo próprio; usa provedores externos (Claude, GPT, DeepSeek, GLM, Grok, Kimi). Nas instâncias de atacantes analisadas, predominam modelos DeepSeek Flash (`SRC-FBI-FLASH-20261113-ARTEX`).
- **Superfície exposta do próprio framework:** a Censys contou 1.465 hosts com console ARTEX exposto em 4 de novembro (cerca de 815 implantações distintas), 10,6% deles com outra ferramenta ofensiva no mesmo host (`SRC-CENSYS-ARTEX-2026-11`); a Check Point achou 2.557 sistemas com painel ARTEX, 1.608 ativos, e 10 expondo o banco inteiro com prompts e passos dos agentes (`SRC-CHECKPOINT-ARTEX-2026-11`). Imagens Docker com backdoor: The Hacker News, citando CERT-In, fala em 62 consoles (`SRC-THN-CERTIN-CRAFTY-FALCON`, grau C).
- **Fora do escopo:** instruções de uso, implantação ou configuração.

## 3. Linha do tempo

| Data | Evento | Fonte | Confiança |
|---|---|---|---|
| 2026-07 | ARTEX publicado no GitHub por "Autumn-27" | `SRC-FBI-FLASH-20261113-ARTEX` | <span class="conf conf-high">confirmada</span> |
| 2026-08 (fim) | GTIG/Mandiant observam ARTEX em resposta a incidentes: grupos de extorsão e clusters suspeitos de nexo PRC | `SRC-GTIG-ARTEX-2026-10` | <span class="conf conf-high">confirmada</span> |
| 2026-08-04 a 10-04 | Prompts recuperados de operador sinófono, setores em 19 países | `SRC-ZSCALER-ARTEX-GLOBAL` | <span class="conf conf-high">alta</span> |
| 2026-09 a 10 | Intrusões em instituições financeiras sul-coreanas (TAG-217) | `SRC-RECORDEDFUTURE-TAG-217-ARTEX`, `SRC-CROWDSTRIKE-ARTEX-SOUTH-KOREA` | <span class="conf conf-med">média</span> |
| 2026-08-18 | Diretórios abertos no servidor ARTEX citado pela CrowdStrike, sete semanas antes do relatório | `SRC-CENSYS-ARTEX-2026-11` | <span class="conf conf-high">alta</span> |
| 2026-10-08 | Repositório original fica indisponível; forks e ARTEX PRO continuam | `SRC-FBI-FLASH-20261113-ARTEX`, `SRC-DATADOG-ARTEX-AWS` | <span class="conf conf-high">confirmada</span> |
| 2026-10-08 (atualizado 10-23) | JPCERT/CC alerta sobre onda de acessos indevidos a organizações japonesas, incluindo uso de frameworks de pentest com IA | `SRC-JPCERT-AT-2026-0030` | <span class="conf conf-med">média</span> |
| 2026-10-10 a 14 | Storm-0940: password spraying em 327 contas de 8 organizações | `SRC-MSFT-STORM-0940-ARTEX` | <span class="conf conf-high">alta</span> |
| 2026-10 | Comprometimento do ConnectWise Cloud Backup, atribuído pela Microsoft ao Storm-0940; app afetado não significa dado acessado | `SRC-MSFT-STORM-0940-ARTEX` | <span class="conf conf-high">alta</span> |
| 2026-10 | VAPOR PANDA: 14+ países em 11 dias, pós-exploração confirmada em 9 organizações | `SRC-CROWDSTRIKE-VAPOR-PANDA-2026-10` | <span class="conf conf-high">confirmada</span> |
| 2026-10 (fim) | Pearl Sleet e Onyx Sleet passam a usar ARTEX | `SRC-MSFT-DPRK-AI-2026-10` | <span class="conf conf-high">confirmada</span> |
| 2026-10 | Wiz: ator com ARTEX ataca fornecedores de TI e software (Okta, Entra ID, Cognito, integrações M365); sobreposição com Storm-0940 é avaliação da Wiz (`CAMPAIGN-ARTEX-IT-SOFTWARE-VENDORS`) | `SRC-WIZ-ARTEX-VENDORS` | <span class="conf conf-high">alta</span> |
| 2026-10-25 → 10-30 | WorkOS: agente ARTEX de um pesquisador escapa do sandbox e acessa ferramenta interna de vendas, sem intenção maliciosa (`INCIDENT-WORKOS-ARTEX-SANDBOX-ESCAPE`) | `SRC-WORKOS-BULLETIN-2026-10-30` | <span class="conf conf-high">confirmada</span> |
| 2026-10-28 → 11-05 | Microsoft: ARTEX busca segredos expostos no GitHub; um agente foi do scan à exfiltração do Azure Key Vault em cinco minutos (`CAMPAIGN-ARTEX-EXPOSED-SECRETS`) | `SRC-MSFT-ARTEX-SECRETS-2026-11` | <span class="conf conf-high">alta</span> |
| 2026-11-05 | Check Point "Hacking on Autopilot" e Censys "Agentic Asbestos": painéis e consoles expostos | `SRC-CHECKPOINT-ARTEX-2026-11`, `SRC-CENSYS-ARTEX-2026-11` | <span class="conf conf-high">alta</span> |
| 2026-11-06 | Microsoft: Storm-3358 mira o setor financeiro | <span class="verify">A VERIFICAR</span> | — |
| 2026-11 | Datadog: ARTEX em contas AWS com chaves IAM comprometidas (`CAMPAIGN-ARTEX-AWS`) | `SRC-DATADOG-ARTEX-AWS` | <span class="conf conf-high">alta</span> |
| 2026-11-11 | Unit 42: páginas de reset de senha e APIs expostas viram acesso à nuvem, sem explorar vulnerabilidade (`CAMPAIGN-ARTEX-IDENTITY-WORKFLOWS`) | `SRC-UNIT42-ARTEX-2026-11` | <span class="conf conf-high">alta</span> |
| 2026-11-12 | Eye Security: resposta a incidente de intrusão guiada por ARTEX (`INCIDENT-EYE-ARTEX-IR`) | `SRC-EYE-ARTEX-IR-2026-11` | <span class="conf conf-high">confirmada</span> |
| 2026-11-10 | Arctic Wolf (via CSA): AntiFox, fork do ARTEX 0.1.1, em intrusões contra IIS e AWS (`CAMPAIGN-ANTIFOX-AWS-IIS`, `TOOL-ANTIFOX`) | `SRC-CSA-ANTIFOX` (B) | <span class="conf conf-med">média</span> |
| 2026-11-13 | FBI FLASH-20261113-001: 67 mil pessoas com dados exfiltrados na Coreia do Sul; mais de 2.250 tenants com tentativas de login no caso ConnectWise | `SRC-FBI-FLASH-20261113-ARTEX` | <span class="conf conf-high">confirmada</span> |
| 2026-11-13 → 11-20 | Pack de detecção MalwareMustDie MMD-072 (v1.1.6 em 20/11), DRL 1.1 | `ECO-126` | — |
| 2026-11-16 | GTIG: frameworks multiagente (ARTEX, CAIRN, CyberStrikeAI, PentAGI) e exploração de n-days automatizada | `SRC-GTIG-AGENTIC-THRESHOLD-2026-11` | <span class="conf conf-high">confirmada</span> |

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
| Sem nome (Microsoft) | não declarado | segredos expostos no GitHub, credenciais de app multitenant | autonomous-operator | `SRC-MSFT-ARTEX-SECRETS-2026-11` |
| Sem nome (Unit 42) | não declarado | reset de senha e APIs expostas, varejo e consultoria | — | `SRC-UNIT42-ARTEX-2026-11` |
| Storm-3358 | Camboja, financeiro | upload anônimo, SSRF, RATs WISP, vshell e AdaptixC2 contra finanças no Sudeste Asiático | autonomous-operator | `SRC-MSFT-STORM-3358-ARTEX` |

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
- **Pack de terceiros:** MalwareMustDie MMD-072 (`ECO-126`), licença DRL 1.1 com atribuição obrigatória, tiers T1 a T4 (T4 só para hunting) e validade por indicador. Também está integrado ao repositório `detectionrules`, numa branch ainda sem PR.
- **O FBI mapeia o ARTEX ao ATT&CK** fase a fase (T1595, T1580, T1087.004, T1190, T1078, T1199, T1606.002, T1552.001…) e pede caça em gateways de LLM, escrita e apagamento de blob em menos de um segundo, dry-runs de validação de deploy ARM e abuso de Kudu/SCM (`SRC-FBI-FLASH-20261113-ARTEX`).
- **Sinais de comportamento que não dependem de IOC:**
  - cadência de máquina nos logs de autenticação (tentativas espaçadas de forma regular, 24 horas);
  - app OAuth novo ou consentimento logo depois de uma rajada de spraying;
  - requisições duplicadas e quase simultâneas vindas de subagentes;
  - tráfego para gateways de LLM a partir de hosts de servidor.

### 7.1 Mapa completo da ThreatDefence (2026-11-20)

O repositório [ThreatDefence/artex-detections](https://github.com/ThreatDefence/artex-detections) (MIT) foi mapeado regra a regra em [ARTEX-DETECTION-MAP.md](../../docs/ARTEX-DETECTION-MAP.md): 209 arquivos de regra em 29 comportamentos e 184 indicadores.

| Nossa detecção | O que cobre | Plataformas deles |
|---|---|---|
| DET-AI-046 | sondagem de permissões: DryRun no EC2, varredura de validate no ARM, logins no Kudu | Sigma, Sentinel, Splunk, Elastic |
| DET-AI-047 | varredura de acesso negado, busca de segredos no CloudWatch, leitura em massa no Key Vault | Sigma, Sentinel, Splunk, Elastic |
| DET-AI-048 (nova) | user agents, artefatos de sondagem, cabeçalho X-ARTX-KEY, JWT alg:none, callbacks para webhook e DNS log | Sigma, Sentinel, Splunk, Elastic, Zeek, Suricata |
| DET-AI-049 (nova) | spray em ritmo de um segundo, rajada de família de user agent, spray que termina em sucesso | Sigma, Sentinel, Splunk, Elastic |
| DET-AI-050 (nova) | service principal: adivinhação de segredo, credencial ou papel concedido a si mesmo, leque de recursos, rajadas no Graph | Sigma, Sentinel, Splunk |
| DET-AI-051 (nova) | abuso de cadastro self-service no Cognito seguido de descoberta | Sigma, Sentinel, Splunk, Elastic |
| DET-AI-052 (nova) | console ARTEX ou imagem com backdoor dentro da rede | Sentinel, YARA, osquery |

Sete comportamentos são detecção genérica de intrusão (shell a partir de serviço web, web shells, Kerberoasting, mascaramento de binários) e ficam como link.

## 8. Mitigação priorizada

| Ação | Esforço | Efeito |
|---|---|---|
| Retro-hunt de credenciais, sign-ins e apps OAuth desde 2026-08-01 | médio | encontra acesso já obtido |
| MFA resistente a phishing e bloqueio de autenticação legada | médio | corta o spraying |
| Revisão de consentimentos OAuth e apps de terceiros com acesso amplo | baixo | fecha a persistência relatada |
| Procurar consoles ARTEX expostos nos próprios ativos (só ativos autorizados) | baixo | acha infraestrutura de atacante ou uso interno não sancionado |
| Varredura de segredos em repositórios | baixo | remove o atalho descrito pela Microsoft em 05/11 |

## 9. Indicadores

Não reproduzidos aqui. Use o CSV do pack MMD-072 (`ECO-126`) ou o anexo do FBI FLASH, respeitando tier e validade de cada indicador; T4 nunca vira bloqueio.

## 10. O que este dossiê não afirma

- **PHP2Shell não é componente do ARTEX.** É um par de falhas no interpretador PHP (CVE-2026-109618 e CVE-2026-109619). A Eye Security diz que o caso dela não envolveu PHP2Shell (`SRC-EYE-ARTEX-IR-2026-11`).
- Usar ARTEX não é o mesmo que tê-lo desenvolvido.
- Os atores que usam ARTEX não estão ligados entre si por usá-lo.

## 11. Brasil e América Latina

Impacto regional não demonstrado nas fontes consultadas. Hipótese a testar: consoles ARTEX expostos em ASNs brasileiros, por consulta de leitura em Censys ou Shodan.

## 12. Mudanças propostas no repositório

- Feito em v0.3: `data/tools.json` com ARTEX, AntiFox, PentAGI, CAIRN, CyberStrikeAI, HexStrike AI e Strix; `uses-tool` liga campanhas e incidentes a cada um, e `TOOL-ANTIFOX derived-from TOOL-ARTEX`. No Explorer, `#tab=graph&focus=TOOL-ARTEX` mostra quem usa.
- Ler o boletim original da Arctic Wolf sobre o AntiFox quando for localizado.
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

**Lidas em 2026-11-20 e registradas:** `SRC-FBI-FLASH-20261113-ARTEX` · `SRC-MSFT-ARTEX-SECRETS-2026-11` · `SRC-CHECKPOINT-ARTEX-2026-11` · `SRC-CENSYS-ARTEX-2026-11` · `SRC-EYE-ARTEX-IR-2026-11` · `SRC-DATADOG-ARTEX-AWS` · `SRC-UNIT42-ARTEX-2026-11` · `SRC-GTIG-AGENTIC-THRESHOLD-2026-11` · `SRC-JPCERT-AT-2026-0030` · `SRC-THN-CERTIN-CRAFTY-FALCON` (grau C).

Também lidas: `SRC-MSFT-STORM-3358-ARTEX` · `SRC-WIZ-ARTEX-VENDORS` · `SRC-WORKOS-BULLETIN-2026-10-30` · `SRC-CSA-ANTIFOX` (B) · `SRC-BC-ANTIFOX` (C).

**Ainda a ler:** o boletim da Arctic Wolf (não localizado); a Huntress (403) e a SentinelOne (429) recusaram o acesso automático.
