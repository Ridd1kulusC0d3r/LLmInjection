<p align="center">
  <img src="assets/llminjection-banner.svg" alt="LLMInjection: panorama de amenazas a LLM y sistemas agénticos" width="100%">
</p>

<!-- lang-bar -->
[English](README.md) · [Português](README.pt-BR.md) · **Español** · [简体中文](README.zh-CN.md) · [Русский](README.ru.md)
<!-- /lang-bar -->

> Traducción asistida por IA, aún sin revisión de un hablante nativo. La versión en inglés es la referencia. Para corregir, véase [docs/TRANSLATIONS.md](docs/TRANSLATIONS.md).

Inteligencia de amenazas abierta para sistemas de IA, LLM y agentes: actores, campañas, técnicas de ataque, casos de prueba seguros, detecciones y controles, vinculados a la evidencia que respalda cada afirmación.

**[Explorer](https://ridd1kulusc0d3r.github.io/LLmInjection/#lang=es)** · [Documentación](docs/README.md) · [Panorama de América Latina](docs/es/PANORAMA-LATAM.md) · [Metodología](docs/METHODOLOGY.md)

---

## En cifras

<!-- gen:stats-es:start -->
| Actores | Campañas | Incidentes | Vulnerabilidades | Técnicas | Fuentes |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **8** | **10** | **30** | **9** | **28** | **54** |

| Casos de prueba | Detecciones | Controles | Marcos | Familias de modelos | Relaciones | Proyectos del ecosistema |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **40** | **45** | **32** | **19** | **12** | **215** | **114** |
<!-- gen:stats-es:end -->

LLMInjection **no es un repositorio de prompts**. Cada afirmación relevante incluye la calificación de su fuente, un nivel de confianza, una fecha de verificación, contexto de marcos de referencia y un enfoque defensivo.

## Qué contiene

| Capa | Qué incluye | Por dónde empezar |
|---|---|---|
| **Actores y campañas** | Operadores estatales y criminales que usan IA, con las etiquetas de los proveedores tal como se publicaron | [`data/actors.json`](data/actors.json) |
| **América Latina** | Uso de IA contra organizaciones de la región, separando lo que afirma cada informe de lo que no afirma | [Panorama](docs/es/PANORAMA-LATAM.md) |
| **Panorama de amenazas** | Métricas citadas, dominios y pistas de investigación de 2026 | [Landscape 2026](docs/THREAT-LANDSCAPE-2026.md) |
| **Técnicas y marcos** | Técnicas con nivel de madurez, mapeadas a ATLAS, OWASP, NIST, SAIF y MAESTRO | [Marcos](docs/FRAMEWORKS.md) |
| **Laboratorio seguro** | Casos de prueba defensivos para prompts, RAG, agentes, MCP y cadena de suministro | [Casos de prueba](docs/TEST-CASES.md) |
| **Detección** | Hipótesis de detección y reglas Sigma iniciales | [Ingeniería de detección](docs/DETECTION-ENGINEERING.md) |
| **Ecosistema** | Proyectos relacionados, clasificados según lo que cada uno puede respaldar | [Mapa del ecosistema](docs/ECOSYSTEM.md) |

## Principios

1. **Un incidente observado, una técnica demostrada en investigación y un ejemplo de laboratorio no se mezclan.** Un repositorio de jailbreaks puede inspirar una prueba; nunca demuestra que un actor usó la técnica.
2. **Inferir no es confirmar.** Cuando el uso de IA se deduce de artefactos, el registro lo dice.
3. **Las etiquetas de los proveedores no se fusionan** en alias universales sin evidencia.
4. **La madurez sale del grafo.** Cada técnica se clasifica como observada en la práctica, vulnerabilidad divulgada, demostrada en investigación o sin evidencia vinculada, y la validación impide que el campo se desvíe de los datos.

## Inicio rápido

```bash
make check         # lint, pruebas, validación de datos y auditoría del grafo
make build         # grafo, STIX, API estática, capas de Navigator y gráficos
python scripts/query_intel.py search "prompt injection"
python scripts/osint_ioc.py informe.md --enrich    # extrae IOC; enriquece CVE con CISA KEV y EPSS
```

Python 3.12, solo biblioteca estándar.

## Contribuir

Las contribuciones útiles aportan **evidencia, relaciones, pruebas, detecciones o correcciones**, no exageración. Lea [CONTRIBUTING.md](CONTRIBUTING.md), prefiera fuentes primarias, preserve la incertidumbre y ejecute `make check` antes de abrir un pull request.

## Licencia

Apache-2.0. Véase [LICENSE](LICENSE).
