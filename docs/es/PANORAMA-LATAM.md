# Panorama de América Latina: uso de IA por actores de amenaza

> Traducción asistida por IA del [panorama en portugués](../pt-BR/PANORAMA-BRASIL-LATAM.md), aún sin revisión de un hablante nativo. En caso de duda, prevalecen los informes primarios citados. Cada afirmación remite a la fuente primaria y separa **lo que dice el informe** de **lo que no dice**. En casi todos los casos el uso de IA es una **inferencia** de los analistas a partir de artefactos (nombres de archivos, estilo de código, conversaciones filtradas), y no una confirmación basada en registros del proveedor del modelo.

Datos estructurados: [`data/campaigns.json`](../../data/campaigns.json), [`data/actors.json`](../../data/actors.json). Filtre por región en el [Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#lang=es) (`BR`, `MX`, `EC`, `LATAM`).

## Resumen

1. Hay **tres conjuntos de actividad** con evidencia de uso de IA en fuentes primarias de 2026 que apuntan a Brasil y América Latina: BREEZE COMET (fraude en sistemas de pago en Brasil), SHADOW-AETHER-040 (gobiernos, México) y CL-CRI-1131 (México y Ecuador).
2. En los tres, la IA aparece **acelerando la producción de herramientas o la ejecución de comandos** (scripts de reconocimiento, validación de credenciales, despliegue; en SHADOW-AETHER-040, un agente que ejecuta comandos bajo supervisión). El informe de Trend observa que la IA "no crea" vulnerabilidades ni errores de configuración, y el acceso inicial informado para BREEZE COMET sigue siendo la fuerza bruta de contraseñas y las llamadas que se hacen pasar por soporte de TI.
3. La defensa más directa es **conductual**: política de ejecución de scripts, detección de iteración rápida de scripts y telemetría de agentes. Identificar texto "generado por IA" no es un control fiable.

## Qué afirman las fuentes primarias

| Conjunto | Región | Informado el | Confianza en el registro | Fuente |
|---|---|---|---|---|
| BREEZE COMET | Brasil | 2026-09-01 | confirmada (actividad) | [Google Threat Intelligence Group y Mandiant](https://cloud.google.com/blog/topics/threat-intelligence/financially-motivated-threat-actor-breeze-comet-targets-brazil/) |
| SHADOW-AETHER-040 | México, América Latina | 2026-05-11 | alta | [Trend Micro](https://www.trendmicro.com/en_us/research/26/e/vibe-hacking-two-ai-augmented-campaigns-target-government-and-financial-sectors-in-latin-america.html) |
| CL-CRI-1131 | México, Ecuador | 2026-09-03 | media | [Palo Alto Networks Unit 42](https://unit42.paloaltonetworks.com/ai-tool-use-targeting-latam-orgs/) |

### BREEZE COMET (Google y Mandiant)

- **Dice:** actor con motivación financiera que manipula sistemas de pago y software bancario en Brasil; los objetivos son organizaciones que mueven dinero por **Pix, STR y Boleto**; al menos un robo de decenas de miles de dólares, en dos oleadas de cientos de transacciones fraudulentas. Mandiant afirma tener evidencia de que el actor usó LLM para acelerar scripts de reconocimiento, validación de credenciales, despliegue masivo y extracción de datos.
- **No dice:** qué modelos se usaron, cómo se observó el uso de IA, ni qué parte del conjunto de herramientas fue generada por IA.
- **Superposición de nombres:** Google informa una superposición con actividad publicada como Plump Spider y SHADOW-AETHER-064. La prensa ([The Hacker News](https://thehackernews.com/2026/09/breeze-comet-executes-hundreds-of.html)) menciona además CL-CRI-1163 de Unit 42; el artículo de Unit 42 **no** afirma ese vínculo. Las etiquetas de los proveedores **no** se fusionaron en el registro.

### SHADOW-AETHER-040 (Trend Micro)

- **Dice:** operadores de habla hispana intrusaron seis entidades del gobierno mexicano entre el 27/12/2025 y el 04/01/2026. Con **alta confianza**, conversaciones filtradas en un servidor C&C expuesto muestran al operador usando una herramienta agéntica de línea de comandos que enviaba prompts a Claude y ejecutaba comandos según las respuestas. El operador supervisaba y corregía al agente.
- **No dice:** que la operación se delegara por completo a la IA. Un solo proveedor, pocos casos, atribución incierta más allá de pistas de idioma. El propio informe señala que parte de los ataques fracasó por falta de una vía de movimiento lateral.

### CL-CRI-1131 (Unit 42)

- **Dice:** el equipo evalúa que los operadores usaron LLM para generar scripts de rodeo contra una organización de transporte, ministerios federales y servicios municipales de agua en México y Ecuador, lo que infiere de la iteración por ensayo y error de scripts numerados y de una instancia expuesta de NextChat.
- **No dice:** qué modelos se usaron, ni atribuye el conjunto a un grupo con nombre.

## Pistas no promovidas

Los elementos siguientes quedan **fuera de los datos** hasta que exista una fuente primaria. Están en la cola de investigación del landscape.

| Pista | Por qué no se promovió |
|---|---|
| Sitios del gobierno brasileño clonados con constructores de sitios con IA para estafas por Pix (Zscaler ThreatLabz, ago/2025) | Conocida solo por cobertura secundaria en esta investigación; informe primario no verificado |
| Fraude de identidad con deepfakes en cuentas de Gov.br y lavado por Pix ([InSight Crime](https://insightcrime.org/news/ghost-riders-and-deepfake-doctors-inside-brazils-ai-driven-crime-surge/)) | Reportaje; casos concretos sin informe técnico |
| El 80 % de los brasileños ha visto deepfakes (Veriff, encuesta Kantar, feb/2026, 1.000 encuestados) | Encuesta de opinión de un proveedor, no telemetría de amenazas |
| 28 millones de estafas por Pix en nueve meses de 2025 y un aumento del 126 % en el fraude con deepfakes (Rio Times citando a Serasa Experian) | Cifras no contrastadas con las fuentes primarias (Serasa, Banco Central) |
| PixRevolution, troyano Android contra Pix con modelo de "operador en el circuito" (Recorded Future, primer semestre de 2026) | El informe plantea la posibilidad de un operador de IA; no la afirma |

## Del hallazgo a la defensa

| Comportamiento | Técnica | Prueba segura | Detección | Control |
|---|---|---|---|---|
| Scripts de reconocimiento y despliegue generados por LLM | `LLMI-T028` | `TC-TOOL-040` | `DET-AI-045` | `CTRL-EXEC-POLICY` |
| Agente supervisado que ejecuta comandos de ataque | `LLMI-T015` | `TC-AUTO-015` | `DET-AI-003` | `CTRL-HUMAN-CHECKPOINT` |
| Mensajes de ingeniería social enviados por agentes | `LLMI-T014` | `TC-SOC-039` | `DET-AI-043` | `CTRL-HUMAN-CHECKPOINT` |

Para las organizaciones que operan Pix, STR o Boleto, el punto práctico es que, en el caso de BREEZE COMET, **los vectores de acceso inicial informados son los de siempre** (fuerza bruta de contraseñas, llamadas que se hacen pasar por soporte de TI, instalación de herramientas de acceso remoto). Lo que cambia es la **velocidad con que el atacante produce herramientas** a medida de su entorno.

## Brechas y próximos pasos

- Localizar informes primarios del Banco Central, de Febraban y de Serasa para las cifras de fraude con Pix y deepfakes.
- Verificar el informe de Zscaler sobre sitios clonados con IA y, si se confirma, registrar la campaña.
- Evaluar SHADOW-AETHER-064 (Trend, abril de 2026) como registro propio, una vez decidido cómo tratar la superposición informada con BREEZE COMET.
- Incluir amenazas recurrentes del ecosistema brasileño de troyanos bancarios (por ejemplo Casbaneiro y Guildma) solo cuando exista evidencia de un papel de la IA.

Las correcciones y las nuevas fuentes son bienvenidas: véase [CONTRIBUTING.md](../../CONTRIBUTING.md).
