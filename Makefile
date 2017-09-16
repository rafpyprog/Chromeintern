init:
	pip install -r requirements.txt -U

test:
	python -m pytest -v tests/test.py

test-win:
		python -m pytest -v tests/test.py -m windows
