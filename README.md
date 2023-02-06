# The Konglomerat e.V. - roseguarden

A fork of https://gitlab.com/roseguarden/roseguarden

Roseguarden is an access and management system for spaces.

[![Build and Deploy](https://github.com/konglomerat/roseguarden/actions/workflows/build-deploy.yml/badge.svg)](https://github.com/konglomerat/roseguarden/actions/workflows/build-deploy.yml)

## Live demo

You can find our live server here : https://roseguarden.fabba.space .
There is also a emulator available to test the full workflow without a need for own hardware.
If you find bugs or have feature requests, please start with an issue [here](https://gitlab.com/roseguarden/roseguarden/-/issues).
The demo server is a public. Please be aware that all data is visible to anybody.
It's meant to be only for test purposes. The data can be reset at any time.

## How to run roseguarden

### By using the release packages

- Download and unzip the latest release `roseguarden-X.Y.Z` [here](https://gitlab.com/roseguarden/roseguarden/-/releases)
- Go to the folder and run the following commands in a terminal
  - Install the requirements with `pip3 -r requirements.txt`
  - Create a `config.ini` with your settings (see `config.template`)
  - Run 'flask run'

### By cloning or forking the roseguarden repository

- Clone or fork https://gitlab.com/roseguarden/roseguarden
- Have a look in the `backend` and `frontend` folder for details to setup your development enviroment
- run `backend` and `frontend` from your development environment (e.g. we use vs code)
  - start the backend with `flask run` out of the `backend` folder (see more datailed instructions below)
  - start the frontend with `npm run dev` out of the `frontend` folder

* alternativly you can use the `script/pack.py`-script to build your own package and host it with an HTTP-server

### By using Docker for Development

- run `docker-compose up -d`
- change frontend/nuxt.config.js change proxy-targets to: target: http://backend:5000 for /api/v1 and /api/v1/log
- frontend is listening on localhost:3000
- backend is listening on localhost:8002 (e.g. for direct calls via insomnia)

:boom: **Note:** the first command is caching an `npm install` into a named docker volume, which is then used in docker-compose. If you change anything in package.json rerun the first command to update dependencies.

#### Run Backend after fresh clone:

- `cd backend`
- `python3 -m venv .venv`
- `. venv/bin/activate`
- (venv) `pip install Flask`
- (venv) `pip install -r requirements.txt`
- (venv) `run flask`

## News

You can find news about the project [on patreon](https://www.patreon.com/roseguarden)

## Support

Please support us on patreon : https://www.patreon.com/roseguarden

## Contribute

You are welcome to contribute. Make a merge request or add issues.
Help is needed in every area e.g. frontend, backend, hardware and documentation.

## License

The different parts of roseguarden are license differently.
The licensing is as followed:

- frontend : MIT license
- backend : GPLv3 license
- docs : Creative Commons

Have a look in the LICENSE files in the folders for details.
