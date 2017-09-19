init:
	pip install -r requirements.txt -U

test:
	pytest tests/test.py --verbose --cov-report term --cov-report xml --cov chromeguard

test-win:
	python -m pytest -v tests/test.py -m windows

push:
	git add .
	git commit -m "$(m)"
	git push
