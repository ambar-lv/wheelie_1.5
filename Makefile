run:
	docker compose -f docker-compose.dev.yml up --build -d
	python manage.py makemigrations
	python manage.py migrate
	python manage.py loaddata initial_data.json
	python manage.py loaddata apps/trailer/initial_data/trailers.json
	python manage.py loaddata apps/trailer/initial_data/trailer-types.json

destroy:
	docker compose -f docker-compose.dev.yml down --rmi all -v

loaddata:
	python manage.py loaddata initial_data.json
	python manage.py loaddata apps/trailer/initial_data/trailers.json
	python manage.py loaddata apps/trailer/initial_data/trailer-types.json