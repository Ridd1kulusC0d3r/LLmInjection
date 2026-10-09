.PHONY: test validate build charts readme lint audit check navigator coverage osint

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 scripts/validate_intel.py

build:
	python3 scripts/build_graph.py && python3 scripts/build_api.py && $(MAKE) navigator coverage charts

coverage:
	python3 scripts/coverage_model.py

osint:
	python3 scripts/osint_ecosystem.py --report docs/ECOSYSTEM-SIGNALS.md

charts:
	python3 scripts/build_charts.py

readme:
	python3 scripts/readme_stats.py

lint:
	ruff check scripts tests integrations

audit:
	python3 scripts/audit_graph.py --strict

# everything CI runs, in one command
check: lint test validate audit

navigator:
	python3 scripts/build_navigator.py
