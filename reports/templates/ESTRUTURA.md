---
title: Estrutura dos produtos de inteligência
---

<p class="rpt-kicker">reports / templates / estrutura</p>

Mapa de quais blocos cada produto leva. **O** = obrigatório, **R** = recomendado, **–** = não se aplica. A ordem das linhas é a ordem de leitura. Os seis modelos desta pasta seguem esta tabela, e a edição impressa (`make print`) segue a mesma ordem.

| # | Bloco | O que responde | Relatório | Dossiê | Mensal | Semanal | Perfil de ator | Alerta |
|---|---|---|---|---|---|---|---|---|
| 1 | Capa e faixa de cabeçalho | Código, versão, TLP, corte | O | O | O | O | O | O |
| 2 | Ficha e como ler | Base de dados, graus, confiança, selos, escopo | O | O | R | – | R | – |
| 3 | Notas de versão e verificação | O que mudou e o que foi conferido em fonte primária | O | O | R | R | R | – |
| 4 | BLUF | A conclusão em até cinco linhas | O | O | O | O | O | O |
| 5 | Resumo para diretoria (uma página) | Risco, impacto no negócio, três decisões | O | R | O | – | – | – |
| 6 | Julgamentos-chave | Julgamento, probabilidade, confiança, base | O | O | O | – | O | – |
| 7 | O mais quente agora (30 dias) | O que é novo desde a última edição | O | R | O | O | – | – |
| 8 | Perguntas de inteligência (PIR) | O que o leitor pediu e o que ficou em aberto | O | R | R | – | R | – |
| 9 | Escopo, metodologia e confiança | O que entra, o que fica de fora, como foi conferido | O | O | O | – | R | – |
| 10 | Panorama e números | Superfície, volume, velocidade, gráfico do KEV | O | – | O | O | – | – |
| 11 | Mapeamento de atores | Quem, nexo, papel da IA, ferramentas, confiança | O | O | O | R | O | – |
| 12 | Linha do tempo de incidentes e vazamentos | Data, caso, categoria, fonte | O | O | O | O | O | R |
| 13 | Vulnerabilidades (CVE, KEV, EPSS, correção) | O que corrigir e em que ordem | O | R | O | O | R | O |
| 14 | Mapeamento de modelos de IA | Famílias de modelo citadas e foco de controle | O | R | R | – | R | – |
| 15 | Cadeia de ataque e TTPs | Fase, técnica LLMI-T, ATLAS, ATT&CK, evidência | O | O | R | R | O | R |
| 16 | Modelagem de ameaças | Ativos, fronteiras de confiança, cenários de abuso | O | R | – | – | – | – |
| 17 | Matriz de risco | Probabilidade × impacto por camada | O | R | R | – | – | – |
| 18 | Matriz de detecção | Técnica × detecção × regra × teste × controle | O | O | O | – | R | – |
| 19 | Threat hunting | Hipótese, janela, onde procurar, o que confirma, consulta | O | O | R | R | R | O |
| 20 | Harness, guardrails e hardening | Controles por camada, versões mínimas | O | O | R | R | – | O |
| 21 | Recomendações por público | CISO, SOC, desenvolvimento, compras e fornecedores | O | R | R | R | – | R |
| 22 | Plano de ação 30/60/90 | Conter, estruturar, sustentar, indicadores | O | R | – | – | – | – |
| 23 | Camada 8: fator humano | Decisão do operador, gatilho da vítima, viés do analista | O | O | R | O | O | – |
| 24 | Brasil e América Latina | Evidência regional ou a frase padrão de ausência | O | O | O | R | R | R |
| 25 | Hipóteses concorrentes e o que não se afirma | O que derrubaria a tese | O | O | R | O | O | – |
| 26 | Previsões verificáveis | O que esperar e como conferir depois | R | R | O | O | – | – |
| 27 | Indicadores | Tipo, valor desarmado, tier, validade, fonte | R | O | – | – | R | O |
| 28 | Qualidade das fontes | Quantas A, B, C; lidas no original ou por busca | O | O | O | R | R | – |
| 29 | Glossário | Termos em uma linha | O | O | R | – | – | – |
| 30 | Referências | Fonte, publicador, grau, data, endereço | O | O | O | O | O | O |
| 31 | Apêndices | CVEs, linha do tempo completa, regras, casos de teste | O | R | R | – | – | – |
| 32 | Retroalimentação | Registros criados, itens de digest, próxima revisão | O | O | O | O | O | O |
| 33 | Versão curta (LinkedIn) e carrossel | Divulgação | R | R | O | O | – | – |

## De onde sai cada bloco

| Bloco | Gerado por script | Escrito pelo analista |
|---|---|---|
| 7, 10, 12, 13, 18, 28, 31 | `build_report_pages.py`, `build_print_report.py`, `build_weekly.py`, `build_snapshot.py`, `coverage_model.py` | só a leitura dos números |
| 11, 14 | `build_print_report.py` (mapa e tabelas) | interpretação e ressalvas de atribuição |
| 4, 5, 6, 8, 16, 17, 21, 22, 23, 25, 26 | – | sempre, a partir das fontes listadas |

## Regras de preenchimento

- Número sem script ou sem `SRC-…` não entra.
- Cada julgamento leva probabilidade (quase certo, provável, possível, improvável, remoto) **e** confiança (alta, média, baixa). São coisas diferentes.
- Alegação de fornecedor sobre o próprio produto entra ao lado de uma checagem de terceiros.
- Seção obrigatória sem conteúdo fica com a frase "sem evidência nas fontes consultadas", não some.
- Antes de publicar: nenhuma caixa `.injected`, nenhum `A VERIFICAR`, nenhum `A PREENCHER`.
