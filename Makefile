install:
	python3 -m venv ./venv; source ./venv/bin/activate; pip3 install -r requirements.txt

test:
	source ./venv/bin/activate; cd test; python3 test_pop.py

lint:
	source ./venv/bin/activate; flake8 src/team_harriette_chick/*.py

