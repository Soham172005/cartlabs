#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-$(git config --get remote.origin.url 2>/dev/null || true)}"
DEPLOY_PATH="${DEPLOY_PATH:-/opt/cartlabs}"
GIT_BRANCH="${GIT_BRANCH:-main}"
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
  rm -rf "$DEPLOY_PATH"
  git clone --branch "$GIT_BRANCH" "$REPO_URL" "$DEPLOY_PATH"
fi

cd "$DEPLOY_PATH"
git fetch origin "$GIT_BRANCH"
git checkout "$GIT_BRANCH"
git reset --hard "origin/$GIT_BRANCH"

export PUBLIC_API_BASE_URL
docker compose -f docker-compose.yml -f docker-compose.prod.yml build
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans
docker compose -f docker-compose.yml -f docker-compose.prod.yml ps
