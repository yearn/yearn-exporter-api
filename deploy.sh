#! /bin/bash

set -e

export DOCKER_TAG=${1:-latest}
docker pull ghcr.io/yearn/yearn-exporter-api:${DOCKER_TAG}
docker-compose down
docker-compose up -d
