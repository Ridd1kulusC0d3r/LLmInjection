.PHONY: test validate build

test:
	python3 -m unittest discover -s tests -v

validate:
	python3 scripts/validate_intel.py

build:
	python3 scripts/build_graph.py && python3 scripts/build_api.py
