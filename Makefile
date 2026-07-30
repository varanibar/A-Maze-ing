ENTRY = a_maze_ing.py
CONFIG = config.txt
DISPLAY = display.py

install:
	pip install flake8 mypy curses
run:
	python3 $(ENTRY) $(CONFIG)
venv:
	python3 -m venv .venv
debug:
	python3 -m pdb $(ENTRY) $(CONFIG)
clean:
	rm -rf __pycache__ .mypy_cache
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
lint-strict:
	flake8 . mypy . --strict

display:
	python3 $(DISPLAY)

.PHONY: install, run, venv, debug, clean, lint, lint strict, display
