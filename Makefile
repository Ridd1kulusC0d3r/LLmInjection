.PHONY: test validate build charts readme

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 scripts/validate_intel.py

build:
	python3 scripts/build_graph.py && python3 scripts/build_api.py && $(MAKE) charts

charts:
	python3 scripts/build_charts.py

readme:
	python3 scripts/readme_stats.py
