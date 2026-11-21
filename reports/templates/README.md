---
title: Modelos de produtos de inteligência
---

<p class="rpt-kicker">reports / templates</p>

Seis esqueletos, um para cada produto, e o mapa [`ESTRUTURA.md`](ESTRUTURA.md), que diz quais dos 33 blocos cada produto leva. Todos usam a mesma mesa de analista do site: papel, tinta, uma cor de sinal, títulos em serifa e rótulos em mono.

| Produto | Cadência | Arquivo | Masthead | Vai para |
|---|---|---|---|---|
| Relatório de inteligência | sob demanda | [`relatorio-de-inteligencia.md`](relatorio-de-inteligencia.md) | `assets/reports/masthead-report.svg` | `reports/intel/AAAA-NNN-slug.md` |
| Threat landscape mensal | mensal, dia 1 | [`threat-landscape-mensal.md`](threat-landscape-mensal.md) | `masthead-landscape.svg` | `reports/monthly/AAAA-MM.md` |
| Tendências da semana | quarta, 8h (gerado por `build_weekly.py`) | [`tendencias-semana.md`](tendencias-semana.md) | `masthead-trends.svg` | `reports/trends/AAAA-Www.md` |
| Dossiê | sob demanda | [`dossie.md`](dossie.md) | `masthead-dossier.svg` | `reports/dossiers/slug.md` |
| Perfil de ator | sob demanda | [`perfil-de-ator.md`](perfil-de-ator.md) | `masthead-dossier.svg` | `reports/dossiers/ator-slug.md` |
| Alerta rápido | no mesmo dia | [`alerta-rapido.md`](alerta-rapido.md) | `masthead-report.svg` | `reports/intel/AAAA-MM-DD-alerta-slug.md` |

## Como usar

0. Leia [`ESTRUTURA.md`](ESTRUTURA.md): ordem dos blocos, o que é obrigatório em cada produto e o que sai de script.

1. Copie o modelo para o destino da tabela.
2. Gere o masthead da edição: `python scripts/build_report_mastheads.py --kind report --title "Título" --out assets/reports/<slug>.svg`.
3. Preencha os blocos <span class="verify">A VERIFICAR</span> e apague os <code>.injected</code> (as caixas tracejadas de instrução).
4. Todo número sai de um script do repositório ou de uma fonte com ID `SRC-…`. Número sem origem não entra.

## Componentes

| Marcação | Efeito |
|---|---|
| `<p class="rpt-head">…</p>` | Faixa mono de cabeçalho: ID, TLP, data, corte |
| `<div class="bluf" markdown="1">…</div>` | Caixa BLUF com régua de sinal |
| `<span class="conf conf-high">alta</span>` · `conf-med` · `conf-low` | Selo de confiança |
| `<span class="verify">A VERIFICAR</span>` | Afirmação ainda não conferida no original |
| `<div class="injected" markdown="1">…</div>` | Instrução do modelo; não pode ficar na edição publicada |

## Formatos de saída

| Formato | Como sai |
|---|---|
| Página no Explorer | automático, ao entrar em `reports/` |
| Edição web (`relatorios/*.html`) | automático para `intel/`, `dossiers/` e `trends/` |
| PDF diagramado | `pdf:` no cabeçalho e `make print` (relatório e dossiês) |
| PDF por impressão | botão "Imprimir em PDF" nos demais |
| Feed e e-mail | automático: `feed.xml` e `feed.json` (ver `docs/NEWSLETTER.md`) |

## Regras que valem para todos

- Relato da fonte, inferência do analista e lacuna ficam em colunas separadas.
- Capacidade não é uso; PoC não é exploração em campo; sobreposição não é o mesmo ator.
- Brasil/LATAM: sem evidência regional, escreva "impacto regional não demonstrado nas fontes consultadas".
- Indicadores só com proveniência, tier e validade. T4 nunca vira bloqueio.
- Nada de instrução operacional de ataque. O texto é escrito para o defensor.
