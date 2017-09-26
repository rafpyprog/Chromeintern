init:
	pip3.6 install -r requirements.txt -U

test:
	pytest tests/test.py --verbose --cov-report term --cov-report xml --cov chromeguard

test-linux:
	python3.6 -m pytest -v tests/test.py -m linux --basetemp=tests/tmp_dir
	python3.6 -m pytest -v tests/test.py -m Guard --basetemp=tests/tmp_dir --cov-report term --cov-report xml --cov chromeguard


test-win:
	python -m pytest -v tests/test.py -m windows

push:
	git add .
	git commit -m "$(m)"
	git push
