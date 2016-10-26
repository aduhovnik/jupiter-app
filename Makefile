backend_host = 0.0.0.0
backend_port = 8000

db_container = $(shell docker-compose ps -q db)
backend_container = $(shell docker-compose ps -q backend)
frontend_container = $(shell docker-compose ps -q frontend)

backend-bash:
	@docker exec -ti ${backend_container} bash

backend-migrate:
	@docker exec -ti $(backend_container) ./manage.py migrate

backend-runserver:
	@docker exec -ti $(backend_container) ./manage.py runserver ${backend_host}:${backend_port}

frontend-bash:
	@docker exec -ti ${frontend_container} bash

frontend-reload:
	@docker exec -ti ${frontend_container} nginx -s reload

db-shell:
	@docker exec -ti $(db_container) psql -U jupiter

docker-restart:
	@docker-compose stop
	@docker-compose up

docker-recreate:
	@docker-compose stop ${service}
	@docker-compose rm -f ${service}
	@docker-compose up ${service}
