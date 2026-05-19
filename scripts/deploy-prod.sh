#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-$(git config --get remote.origin.url 2>/dev/null || true)}"
DEPLOY_PATH="${DEPLOY_PATH:-/opt/cartlabs}"
DEPLOY_BRANCH="${DEPLOY_BRANCH:-main}"
PUBLIC_API_BASE_URL="${PUBLIC_API_BASE_URL:-http://localhost:8000/api}"

if [[ -z "$REPO_URL" ]]; then
  echo "REPO_URL is required when the production server does not already have the repo."
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed on this host."
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose plugin is not installed on this host."
  exit 1
fi

if [[ ! -d "$DEPLOY_PATH/.git" ]]; then
  mkdir -p "$DEPLOY_PATH"
  git clone --branch "$DEPLOY_BRANCH" "$REPO_URL" "$DEPLOY_PATH"
fi

cd "$DEPLOY_PATH"
git fetch origin "$DEPLOY_BRANCH"
git checkout "$DEPLOY_BRANCH"
git reset --hard "origin/$DEPLOY_BRANCH"

export PUBLIC_API_BASE_URL
docker compose -f docker-compose.yml -f docker-compose.prod.yml build
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps
