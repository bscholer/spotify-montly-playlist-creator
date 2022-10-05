target: build stop run logs

build:
	docker build . --file Dockerfile -t bscholer/spotify-playlist-creator

stop:
	- docker stop spotify-playlist-creator
	- docker rm spotify-playlist-creator

run:
	docker run -it -d --env-file=.env -v /home/bscholer/spotify-montly-playlist-creator/data:/data --name spotify-playlist-creator bscholer/spotify-playlist-creator

exec:
	docker exec -it spotify-playlist-creator /bin/bash

logs:
	docker logs --follow spotify-playlist-creator
