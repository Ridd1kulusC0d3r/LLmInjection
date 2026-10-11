# Vocabulário de contenção de agentes: equivalências com os controles do repositório

> **Status: vocabulário de autor, sem fonte verificada.** Os onze nomes abaixo vêm de uma imagem de uma publicação, sem link, especificação, licença ou implementação que eu tenha conseguido ler. A imagem está cortada no começo (o primeiro item aparece só pelo fim da definição, "efeito delimitado, reversão e verificação") e no fim. Nada aqui é evidência, não vira controle, técnica nem entrada de ecossistema, e as siglas não são usadas em nenhum dataset. Esta nota só mostra onde cada ideia já tem casa no LLMInjection.

Se o autor publicar o material (repositório, documento ou artigo com definições, licença e testes), a avaliação muda: aí cabe uma entrada de ecossistema, nota D, e uma revisão desta tabela.

## Equivalências

As definições são as da imagem. A coluna da direita é uma leitura minha de **uma linha** por sigla, não uma verificação.

| Sigla e nome (como publicado) | Definição (como publicada) | Controle ou conceito mais próximo |
|---|---|---|
| MEA, Model-Excluded Authority | impede que a resposta do modelo conceda autoridade para executar | [`CTRL-POLICY-OUTSIDE-MODEL`](../../data/controls.json), política aplicada fora do modelo |
| ACO, Action Contract Object | declara a ação, seu alcance e sua reversão antes da execução | `CTRL-CONTEXTUAL-AUTHZ` e `CTRL-ACTION-BUDGET` |
| PPB, Principal-Perimeter Binding | vincula a sessão ao perímetro do responsável protegido | `CTRL-MCP-STATE-BINDING` (o conceito de vínculo de sessão a identidade) |
| SAV, Split-Authority Verification | verifica o resultado com credenciais sem permissão de escrita | `CTRL-SECRET-ISOLATION` e `CTRL-PRIVILEGE-SEPARATED-LLM` (separação de privilégios) |
| SSC, Sealed Session Chain | encadeia registros por hashes e sela a sessão | `CTRL-AGENT-TELEMETRY`, que hoje não pede registro à prova de adulteração |
| PPR, ProofPath Receipt | permite recomputar a integridade das evidências sem o código do produtor | `CTRL-AGENT-TELEMETRY`, mesma lacuna |
| RBT, Review-Bound Testimony | registra relatos humanos como evidência para revisão | `CTRL-HUMAN-CHECKPOINT` |
| SRL, Sealed Review Loop | cria revisões seladas vinculadas à sessão original | `CTRL-HUMAN-CHECKPOINT` |
| EBT, Evidence-Bound Targeting | identifica alvos em campos estruturados de evidências | sem equivalente claro; talvez `CTRL-STRUCTURED-OUTPUT` |
| DSC, Discriminator-Scoped Containment | delimita a contenção em infraestruturas compartilhadas | sem equivalente claro |
| ELR, Element-Level Reconciliation | acompanha cada elemento contido, mesmo com regras agregadas | sem equivalente claro |

## O que dá para aproveitar sem adotar as siglas

A pergunta que fecha a publicação, "a defesa agiu dentro dos limites? o efeito foi observado?", é a mesma separação entre **observado** e **inferido** que o repositório já exige das fontes. Aplicada à telemetria de agentes, ela sugere um **recibo por ação do agente**, com quatro campos além do que `CTRL-AGENT-TELEMETRY` já registra (identidade, passo do plano, capacidade pedida, resultado da autorização e efeito colateral):

| Campo | Pergunta que responde |
|---|---|
| ação declarada antes da execução | o agente disse o que ia fazer? |
| alcance declarado | até onde ia? |
| reversão declarada | dava para desfazer? |
| efeito observado depois | o que de fato aconteceu? |

Com isso, as detecções de agente poderiam comparar o declarado com o observado: [`DET-AI-003`](../../data/detections.json) (travessia de fronteira de privilégio), `DET-AI-040` (desvio de política após conteúdo não confiável) e `DET-AI-033` (agente que amplia a própria aprovação automática) já listam telemetria de plano e de chamada de ferramenta, mas nenhuma pede o efeito observado ao lado da ação declarada.

Fica como proposta em aberto, no [roadmap](../ROADMAP.md); não alterei nenhum controle nem detecção.

## Registro da avaliação

- **Repositório `pmotadeee/-ATous-Secure-Network`:** avaliado separadamente e **não relacionado** a esta imagem. Não contém nenhuma das siglas. É um framework de rede P2P e LoRa, sem conteúdo de ameaças de IA, com `LICENSE` em GPL-3.0 e um `LICENSE-MIT` ao lado. Não entrou no ecossistema.
- Data da avaliação: 2026-10-11.
