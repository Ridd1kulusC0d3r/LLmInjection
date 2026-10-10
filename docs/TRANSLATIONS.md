# Translations

The Explorer interface and the README are available in English, Portuguese, Spanish, Simplified Chinese and Russian. The Latin America regional overview is available in Portuguese and Spanish. **All translations are machine-assisted and have not yet been reviewed by native speakers.** The English text is the reference.

## Status

| Language | Explorer interface | README | Regional overview | Review |
|---|---|---|---|---|
| English | original | [README.md](../README.md) | [Portuguese](pt-BR/PANORAMA-BRASIL-LATAM.md) and [Spanish](es/PANORAMA-LATAM.md) are translations of a Portuguese original | original |
| Português (Brasil) | yes | [README.pt-BR.md](../README.pt-BR.md) | [PANORAMA-BRASIL-LATAM.md](pt-BR/PANORAMA-BRASIL-LATAM.md) (original) | native review pending |
| Español | yes | [README.es.md](../README.es.md) | [PANORAMA-LATAM.md](es/PANORAMA-LATAM.md) | native review pending |
| 简体中文 | yes | [README.zh-CN.md](../README.zh-CN.md) | not available | native review pending |
| Русский | yes | [README.ru.md](../README.ru.md) | not available | native review pending |

The machine-readable version of this table is [`site/translations.json`](../site/translations.json); the Explorer reads it for its Languages tab and a test checks that every file it lists exists.

## What is not translated, and why

The records themselves stay in English: actor, campaign and technique names, summaries, source titles and the contents of the datasets. They quote primary reports, and a machine translation of an attribution statement (who did what, how sure the vendor is) can change its meaning. Search and CSV exports therefore use the English text. Search ignores accents and case, so `méxico` finds `Mexico`.

The Explorer shows a notice about this whenever a non-English language is selected.

## Reviewing a translation

Native-speaker review is the most useful contribution here.

1. Open [`site/i18n/<code>.json`](../site/i18n) (`pt`, `es`, `zh`, `ru`) next to [`en.json`](../site/i18n/en.json). Keys are identical across files; `{placeholders}` must be kept.
2. Prefer the glossary below for terms that appear more than once, and change the glossary and every use together.
3. Check the result in the Explorer with `#lang=<code>` at the end of the URL, at desktop and phone width: long words (Russian, Spanish) and unbroken CJK text are where layouts break.
4. Run `make check`. The tests fail on missing keys, changed placeholders, unused keys, wrong Chinese punctuation and low text contrast.
5. Open a pull request, or an issue with the [correction form](https://github.com/Ridd1kulusC0d3r/LLmInjection/issues/new?template=correction.yml).

When a reviewer signs off a language, change its `review` value in `site/translations.json` from `machine` to a reviewer note and update the Review column above.

## Adding a language

1. Copy `site/i18n/en.json` to `site/i18n/<code>.json` and translate the values.
2. Add the language to `LANGS` in [`site/i18n.js`](../site/i18n.js) and to `site/translations.json`.
3. Add `README.<code>.md` (copy a translated README and keep the `<!-- lang-bar -->` block and the `gen:stats-<code>` markers), and add the language to `STAT_LABELS` in [`scripts/readme_stats.py`](../scripts/readme_stats.py).
4. Run `python scripts/readme_stats.py` and `make check`.

Right-to-left languages need additional layout work (the Explorer is laid out left to right) and are not supported yet.

## Typography notes

- **Chinese** uses full-width punctuation next to Han characters, no letter-spacing, and a Han-capable font stack; the `lang` attribute selects Simplified Chinese glyphs.
- **Russian and Spanish** labels are longer than English ones. Tables scroll horizontally on narrow screens instead of breaking the page.
- Plural forms are avoided in interface strings (for example "Linked records: 3" instead of "3 linked records") because Russian has four plural categories.

## Glossary

Generated from the Explorer dictionaries, so documents and interface use the same terms.

<!-- gen:glossary:start -->

| English | Português | Español | 简体中文 | Русский |
|---|---|---|---|---|
| actor | ator | actor | 攻击者 | субъект |
| campaign | campanha | campaña | 攻击活动 | кампания |
| incident | incidente | incidente | 事件 | инцидент |
| vulnerability | vulnerabilidade | vulnerabilidad | 漏洞 | уязвимость |
| technique | técnica | técnica | 技术 | техника |
| test case | caso de teste | caso de prueba | 测试用例 | тестовый случай |
| detection | detecção | detección | 检测 | обнаружение |
| control | controle | control | 控制措施 | мера защиты |
| framework | framework | marco | 框架 | фреймворк |
| source | fonte | fuente | 来源 | источник |
| Evidence | Evidência | Evidencia | 证据 | Свидетельства |
| Confidence | Confiança | Confianza | 置信度 | Уверенность |
| Maturity | Maturidade | Madurez | 成熟度 | Зрелость |
| Coverage | Cobertura | Cobertura | 覆盖度 | Покрытие |
| Timeline | Cronologia | Cronología | 时间线 | Хронология |
| Ecosystem | Ecossistema | Ecosistema | 生态系统 | Экосистема |
| Graph | Grafo | Grafo | 图谱 | Граф |
| confirmed | confirmada | confirmada | 已确认 | подтверждено |
| high | alta | alta | 高 | высокая |
| medium | média | media | 中 | средняя |
| low | baixa | baja | 低 | низкая |
| unverified | não verificada | sin verificar | 未验证 | не проверено |
| observed in the wild | observada em campo | observada en la práctica | 已在实际攻击中观察到 | наблюдается в реальных атаках |
| disclosed vulnerability | vulnerabilidade divulgada | vulnerabilidad divulgada | 已披露漏洞 | раскрытая уязвимость |
| research demonstrated | demonstrada em pesquisa | demostrada en investigación | 研究中已验证 | показано в исследованиях |
| no linked evidence | sem evidência ligada | sin evidencia vinculada | 暂无关联证据 | нет связанных свидетельств |

<!-- gen:glossary:end -->
