.PHONY: install dev clean migrate seed

install:
	python -m venv .venv
	.\.venv\Scripts\activate && pip install -r requirements.txt

dev:
	.\.venv\Scripts\activate && python -m flask run --host=0.0.0.0 --port=5000

migrate:
	.\.venv\Scripts\activate && python -m flask db upgrade

seed:
	.\.venv\Scripts\activate && python seed.py

clean:
	if exist .venv rmdir /s .venv
	if exist __pycache__ rmdir /s __pycache__
