VENV=.venv

.PHONY: venv install-dev test lint docker-build docker-run

venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip

install-dev: venv
	$(VENV)/bin/pip install -r requirements.txt -r requirements-dev.txt

test:
	python main.py

lint:
	$(VENV)/bin/flake8 . || true

docker-build:
	docker build -t azl:latest .

docker-run:
	docker run --rm azl:latest