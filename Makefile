loaddata:
	python manage.py loaddata apps/user/initial_data/users.json
	python manage.py loaddata apps/workforce/initial_data/owners.json
	python manage.py loaddata apps/workforce/initial_data/companies.json
	python manage.py loaddata initial_data.json
	python manage.py loaddata apps/trailer/initial_data/trailers.json
	python manage.py loaddata apps/trailer/initial_data/trailer-types.json

run:
	docker compose -f docker-compose.dev.yml up --build -d
	python manage.py makemigrations
	python manage.py migrate
	make loaddata

destroy:
	docker compose -f docker-compose.dev.yml down --rmi all -v
	./clean_project.sh

