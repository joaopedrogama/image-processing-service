.PHONY: install install-hooks runserver lint format

docker_run_base_command := docker compose exec
container_name := image_processing_service

install-hooks:
	pre-commit install

test:
	$(docker_run_base_command) $(container_name) python manage.py test

run:
	$(docker_run_base_command) $(container_name) python manage.py runserver

ruff:
	$(docker_run_base_command) $(container_name) ruff check .

fix:
	$(docker_run_base_command) $(container_name) ruff check --fix .

format:
	$(docker_run_base_command) $(container_name) ruff format .
