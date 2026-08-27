.PHONY: install reproduce notebook test verify

install:
	python -m pip install -r requirements-lock.txt
	python -m pip install -e . --no-deps

reproduce:
	python scripts/reproduce_all.py

notebook:
	python -m nbconvert --to notebook --execute reproduce_report_figures.ipynb --output reproduce_report_figures.ipynb --ExecutePreprocessor.timeout=180

test:
	python -m pytest

verify: reproduce test notebook
