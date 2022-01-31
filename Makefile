.DEFAULT_GOAL := help

install:
	pip3 install -r requirements-dev.txt --user --upgrade --no-warn-script-location

format.black:
	python3 -m black ./src ./test --exclude vendor/

format.isort:
	python3 -m isort -rc ./src  ./test --skip vendor/

test.lint: ## Lint python files with flake8
	python3 -m flake8 ./src ./test


.PHONY: test
test.unit:
	python3 -m pytest test/ --import-mode=importlib

test: ## Launch tests in their own docker container
	make format.black && make format.isort && make test.lint && make test.unit

format:
	make format.black && make format.isort
