HOST=127.0.0.1
date=$(shell date +%s)
TEST_PATH=./

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +

lint:
	flake8 --exclude=.tox,

test: clean-pyc
	py.test --verbose --color=yes $(TEST_PATH)

run:
	python manage.py runserver

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

geth:
	geth --rpc --rpcapi "personal,eth" --dev --networkid 123 console

help:
	@echo "    clean-pyc"
	@echo "        Remove python artifacts."
	@echo "    lint"
	@echo "        Check style with flake8."
	@echo "    test"
	@echo "        Run py.test"
	@echo '    run'
	@echo '        Run the `my_project` service on your local machine.'
	@echo '        to change the host and port, run below'
	@echo '        `python manage.py runserver --host $(HOST) --port $(PORT)`'
	@echo '        `make run HOST=127.0.0.1 PORT=8000`'
	@echo '    migrations'
	@echo '        Run the `makemigrations`'
	@echo '    migrations'
	@echo '        Run the `migrate`'
