.PHONY: check index check-index pdf
check:
	python3 -B tools/run_checks.py
index:
	python3 tools/build_index.py
check-index:
	python3 tools/build_index.py --check
pdf:
	mkdir -p build
	latexmk -pdf -interaction=nonstopmode -halt-on-error -output-directory=build paper/main.tex
