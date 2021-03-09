APP = users

run-dev:
	docker-compose up --build --detach

exec:
	docker-compose exec $(APP) $(CMD)

test:
	docker-compose exec $(APP) pipenv run test

cov:
	docker-compose exec $(APP) pipenv run cov

lint:
	docker-compose exec $(APP) pipenv run lint

fix:
	docker-compose exec $(APP) sh -c \
		"pipenv run fix && pipenv run isort"
