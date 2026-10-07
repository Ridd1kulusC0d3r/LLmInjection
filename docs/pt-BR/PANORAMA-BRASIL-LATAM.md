# Panorama Brasil e América Latina: uso de IA por atores de ameaça

> Visão regional do LLMInjection, em português. Cada afirmação aponta para a fonte primária e separa **o que o relatório diz** de **o que ele não diz**. Em quase todos os casos, o uso de IA é **inferido** pelos analistas a partir de artefatos (nomes de arquivos, estilo de código, conversas vazadas), e não confirmado por registros do provedor do modelo.

Dados estruturados: [`data/campaigns.json`](../../data/campaigns.json), [`data/actors.json`](../../data/actors.json). Filtre por região no [Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/) (`BR`, `MX`, `EC`, `LATAM`).

## Resumo

1. Há **três conjuntos de atividade** com evidência de IA em fontes primárias de 2026 visando o Brasil e a América Latina: BREEZE COMET (fraude em sistemas de pagamento no Brasil), SHADOW-AETHER-040 (governos, México) e CL-CRI-1131 (México e Equador).
2. Nos três, a IA aparece **acelerando a produção de ferramentas ou a execução de comandos** (scripts de reconhecimento, validação de credenciais, implantação; no SHADOW-AETHER-040, um agente executando comandos sob supervisão). O relatório da Trend observa que a IA "não cria" vulnerabilidades nem falhas de configuração, e o acesso inicial relatado para o BREEZE COMET segue sendo força bruta de senhas e ligações se passando por suporte de TI.
3. A defesa mais direta é **comportamental**: política de execução de scripts, detecção de iteração rápida de scripts e telemetria de agentes. Identificar texto "gerado por IA" não é um controle confiável.

## O que as fontes primárias afirmam

| Conjunto | Região | Relatado em | Confiança no registro | Fonte |
|---|---|---|---|---|
| BREEZE COMET | Brasil | 2026-09-01 | confirmada (atividade) | [Google Threat Intelligence Group e Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/financially-motivated-threat-actor-breeze-comet-targets-brazil/) |
| SHADOW-AETHER-040 | México, América Latina | 2026-05-11 | alta | [Trend Micro](https://www.trendmicro.com/en_us/research/26/e/vibe-hacking-two-ai-augmented-campaigns-target-government-and-financial-sectors-in-latin-america.html) |
| CL-CRI-1131 | México, Equador | 2026-09-03 | média | [Palo Alto Networks Unit 42](https://unit42.paloaltonetworks.com/ai-tool-use-targeting-latam-orgs/) |

### BREEZE COMET (Google e Mandiant)

- **Diz:** ator com motivação financeira que manipula sistemas de pagamento e software bancário no Brasil; alvos são organizações que movimentam dinheiro por **Pix, STR e Boleto**; ao menos um roubo de dezenas de milhares de dólares, em duas ondas de centenas de transações fraudulentas. A Mandiant afirma ter evidência de que o ator usou LLMs para acelerar scripts de reconhecimento, validação de credenciais, implantação em massa e extração de dados.
- **Não diz:** quais modelos foram usados, como o uso de IA foi observado, nem quanto do ferramental foi gerado por IA.
- **Sobreposição de nomes:** o Google relata sobreposição com atividade publicada como Plump Spider e SHADOW-AETHER-064. A imprensa ([The Hacker News](https://thehackernews.com/2026/09/breeze-comet-executes-hundreds-of.html)) cita também o CL-CRI-1163 da Unit 42; o artigo da Unit 42 **não** afirma essa ligação. Os rótulos de fornecedores **não** foram fundidos no registro.

### SHADOW-AETHER-040 (Trend Micro)

- **Diz:** operadores de língua espanhola invadiram seis entidades do governo mexicano entre 27/12/2025 e 04/01/2026. Com **alta confiança**, conversas vazadas em um servidor C&C exposto mostram o operador usando uma ferramenta agentiva de linha de comando que enviava prompts ao Claude e executava comandos conforme as respostas. O operador supervisionava e corrigia o agente.
- **Não diz:** que a operação foi totalmente delegada à IA. Um único fornecedor, poucos casos, atribuição incerta além de pistas de idioma. O próprio relatório observa que parte dos ataques falhou por falta de caminho de movimentação lateral.

### CL-CRI-1131 (Unit 42)

- **Diz:** a equipe avalia que os operadores usaram LLMs para gerar scripts de contorno contra uma organização de transporte, ministérios federais e serviços municipais de água no México e no Equador, inferido por iteração tentativa-e-erro de scripts numerados e por uma instância NextChat exposta.
- **Não diz:** quais modelos foram usados, nem atribui o conjunto a um grupo nomeado.

## Pistas não promovidas

Itens abaixo ficam **fora dos dados** até haver fonte primária. Estão na fila de pesquisa do landscape.

| Pista | Por que não foi promovida |
|---|---|
| Sites do governo brasileiro clonados com construtores de sites de IA para golpes via Pix (Zscaler ThreatLabz, ago/2025) | Conhecida apenas por cobertura secundária nesta pesquisa; relatório primário não verificado |
| Fraude de identidade com deepfake em contas Gov.br e lavagem via Pix ([InSight Crime](https://insightcrime.org/news/ghost-riders-and-deepfake-doctors-inside-brazils-ai-driven-crime-surge/)) | Reportagem; casos específicos sem relatório técnico |
| 80% dos brasileiros já viram deepfakes (Veriff, pesquisa Kantar, fev/2026, 1.000 respondentes) | Pesquisa de opinião de um fornecedor, não telemetria de ameaça |
| 28 milhões de golpes Pix em nove meses de 2025 e alta de 126% em fraude com deepfake (Rio Times citando a Serasa Experian) | Números não conferidos nas fontes primárias (Serasa, Banco Central) |
| PixRevolution, trojan Android contra o Pix com modelo "operador no circuito" (Recorded Future, 1º semestre de 2026) | O relatório levanta a possibilidade de um operador de IA; não a afirma |

## Do achado à defesa

| Comportamento | Técnica | Teste seguro | Detecção | Controle |
|---|---|---|---|---|
| Scripts de reconhecimento e implantação gerados por LLM | `LLMI-T023` | `TC-TOOL-026` | `DET-AI-020` | `CTRL-EXEC-POLICY` |
| Agente supervisionado executando comandos de ataque | `LLMI-T015` | `TC-AUTO-015` | `DET-AI-003` | `CTRL-HUMAN-CHECKPOINT` |
| Mensagens de engenharia social enviadas por agentes | `LLMI-T014` | `TC-SOC-025` | `DET-AI-018` | `CTRL-HUMAN-CHECKPOINT` |

Para organizações brasileiras que operam Pix, STR ou Boleto, o ponto prático é que, no caso do BREEZE COMET, **os vetores de acesso inicial relatados são os de sempre** (força bruta de senhas, ligações se passando por suporte de TI, instalação de ferramentas de acesso remoto). O que muda é a **velocidade com que o atacante produz ferramentas** sob medida para o seu ambiente.

## Lacunas e próximos passos

- Localizar relatórios primários do Banco Central, da Febraban e da Serasa para os números de fraude com Pix e deepfake.
- Verificar o relatório da Zscaler sobre sites clonados por IA e, se confirmado, registrar a campanha.
- Avaliar o SHADOW-AETHER-064 (Trend, abril/2026) como registro próprio, depois de decidir como tratar a sobreposição reportada com BREEZE COMET.
- Incluir ameaças recorrentes do ecossistema brasileiro de trojans bancários (por exemplo Casbaneiro e Guildma) apenas quando houver evidência de papel da IA.

Correções e novas fontes são bem-vindas: veja [CONTRIBUTING.md](../../CONTRIBUTING.md).
