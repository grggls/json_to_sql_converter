test:
	python -m unittest discover -s tests -p 'test_*.py'

run:
	python json2sql.py ./tests/test_data/request-data.json

lint:
	pipenv run format
	pipenv run lint

.PHONY: test
