.PHONY: install readme check

install:
	pip install -r requirements.txt

readme:
	python3 scripts/render.py

check:
	python3 scripts/render.py --check