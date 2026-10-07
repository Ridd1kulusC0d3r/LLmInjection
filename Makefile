.PHONY: test validate build charts readme lint audit check navigator

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 scripts/validate_intel.py

build:
	python3 scripts/build_graph.py && python3 scripts/build_api.py && $(MAKE) navigator charts

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
