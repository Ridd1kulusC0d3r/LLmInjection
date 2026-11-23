.PHONY: exposure tcem print test validate build charts readme lint audit check navigator coverage site osint

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 scripts/validate_intel.py
	python3 scripts/validate_ot.py

build:
	python3 scripts/build_graph.py && python3 scripts/build_api.py && $(MAKE) navigator coverage charts

site:
	python3 scripts/build_site.py --out _site

coverage:
	python3 scripts/coverage_model.py

osint:
	python3 scripts/osint_ecosystem.py --report docs/ECOSYSTEM-SIGNALS.md

charts:
	python3 scripts/build_charts.py

readme:
	python3 scripts/readme_stats.py

lint:
	ruff check scripts tests integrations examples

audit:
	python3 scripts/audit_graph.py --strict

# everything CI runs, in one command
check: lint test validate audit

navigator:
	python3 scripts/build_navigator.py

# Print edition of the 2026 AI threat report (needs Playwright/Chromium and poppler-utils)
print:
	python3 scripts/build_print_report.py --out dist/print
	node scripts/render_print_report.js dist/print reports/pdf/LLMI-RI-2026-11-20-ameacas-sistemas-ia.pdf
	python3 scripts/build_print_report.py --out dist/print-artex --dossier reports/dossiers/artex.md
	node scripts/render_print_report.js dist/print-artex reports/pdf/LLMI-DS-ARTEX.pdf --dossier reports/dossiers/artex.md
	python3 scripts/build_print_report.py --out dist/print-storm0940 --dossier reports/dossiers/ator-storm-0940.md
	node scripts/render_print_report.js dist/print-storm0940 reports/pdf/LLMI-PA-STORM-0940.pdf --dossier reports/dossiers/ator-storm-0940.md
	python3 scripts/build_print_report.py --out dist/print-tcem --dossier reports/dossiers/tcem-artex.md
	node scripts/render_print_report.js dist/print-tcem reports/pdf/LLMI-TM-ARTEX.pdf --dossier reports/dossiers/tcem-artex.md

exposure:
	python3 scripts/offensive_agency_sync.py

tcem:
	python3 scripts/build_tcem.py
	python3 scripts/tcem_validate.py
