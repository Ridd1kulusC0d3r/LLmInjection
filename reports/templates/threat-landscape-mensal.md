---
title: "Threat Landscape de IA, LLMs e agentes · Mês AAAA"
---

![Masthead](../../assets/reports/masthead-landscape.svg)

<p class="rpt-head"><span>LLMI-TL-AAAA-MM</span><span class="tlp">TLP:CLEAR</span><span>Snapshot data/snapshots/AAAA-MM.json · Corte AAAA-MM-DD</span></p>

<div class="injected" markdown="1">
Todo número desta página sai de `scripts/build_snapshot.py`, `scripts/diff_intelligence.py`, `scripts/readme_stats.py` ou `scripts/coverage_model.py`. Número digitado à mão não entra. O snapshot leva o nome do mês que cobre.
</div>

<div class="bluf" markdown="1">
Três a cinco julgamentos do mês, cada um com probabilidade, confiança e IDs.
</div>

## 1. Resumo gerencial

| Pergunta | Resposta em uma linha |
|---|---|
| O que mudou no risco neste mês? | … |
| O que exige decisão? | … |
| O que melhorou? | … |

## 2. Placar

| Atores | Campanhas | Incidentes | Técnicas | Vulnerabilidades | Detecções | Fontes |
|---|---|---|---|---|---|---|
| n (Δ) | n (Δ) | n (Δ) | n (Δ) | n (Δ) | n (Δ) | n (Δ) |

## 3. O que mudou

| Tipo | Novos | Alterados | Rebaixados ou removidos | Destaque |
|---|---|---|---|---|

Fonte: `reports/monthly/AAAA-MM-diff.md`.

## 4. O mais quente do mês

| Data | Registro | Tipo | Confiança | Sinais | Ferramentas | Fonte principal |
|---|---|---|---|---|---|---|

## 5. Uso adversário de IA

### 5.1 Mapeamento de atores por nexo

| Nexo | Atores | Papel da IA | Ferramentas agênticas | Confiança |
|---|---|---|---|---|

### 5.2 Por papel da IA (três meses)
`tooling-development` → `offensive-enabler` → `autonomous-operator`: quantos registros em cada degrau, mês a mês.

### 5.3 Frameworks ofensivos agênticos
ARTEX, PentAGI, Cairn, CyberStrikeAI e outros: quem usa, para quê, o que está comprovado. Link para o dossiê de cada um.

### 5.4 Modelos de IA citados

| Família | Casos no mês | Observação |
|---|---|---|

## 6. Ataques contra sistemas de IA

| Técnica | Sinal no mês | Maturidade |
|---|---|---|
| LLMI-T001 … T028 | sinal novo / sem sinal público novo | em campo / falha divulgada / pesquisa |

## 7. Vulnerabilidades e supply chain de IA

| CVE | Produto | KEV (data) | EPSS | Explorada em campo (fonte) | Correção | Relação com IA |
|---|---|---|---|---|---|---|

Blocos fixos: gateways de IA, servidores e clientes MCP, runtimes locais, frameworks de agente, modelos e pacotes. Em separado: falhas encontradas por IA e falhas usadas por agente atacante.

## 8. Linha do tempo do mês

| Data | Caso | Cat. | O que aconteceu |
|---|---|---|---|

## 9. Cobertura defensiva

Matriz técnica × detecção × regra × teste × controle (`scripts/coverage_model.py`). A maior lacuna do mês e o que a fecha.

| Medida | Mês anterior | Este mês |
|---|---|---|
| Detecções com arquivo de regra | n | n |
| Técnicas sem guardrail | n | n |
| Técnicas sem hardening | n | n |
| Testes executados em laboratório | n | n |

## 10. Hunting do mês
Uma a três hipóteses novas, com janela, telemetria e o que confirma.

## 11. Setores e regiões

### Brasil e América Latina
Evidência regional, ou: *impacto regional não demonstrado nas fontes consultadas*.

## 12. Padrões e regulação
OWASP, MITRE ATLAS, NIST, CISA, CoSAI, EU AI Act, ANPD, PL 2338.

## 13. Recomendações de segurança do mês

| # | Recomendação | Efeito | Quem conduz |
|---|---|---|---|
| R1 | … | … | … |

## 14. Previsões verificáveis

| Previsão para o próximo mês | Probabilidade | Como verificar | Resultado (mês seguinte) |
|---|---|---|---|

<div class="injected" markdown="1">
No mês seguinte, preencha a última coluna das previsões anteriores. O placar de acertos é o que dá credibilidade à série.
</div>

## 15. Fila de pesquisa

| Candidato | Por que importa | Dono | Prazo |
|---|---|---|---|

## 16. Conclusão do mês
O que o mês mostrou e o que muda na prioridade do defensor.

## 17. Método, limites e fontes

| Grau | Fontes novas no mês | Lidas no original |
|---|---|---|

O que foi lido no original, o que veio de busca, o que falhou.

## 18. Retroalimentação
Registros criados, digests que originaram, próxima edição.

---

## Versão curta (LinkedIn) e carrossel
Gancho · três números do placar · uma previsão · link. Cinco quadros: capa, placar, destaque, o que fazer, fonte.
