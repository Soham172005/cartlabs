#!/usr/bin/env bash
set -euxo pipefail

apt-get update
apt-get install -y ca-certificates curl git unzip

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  > /etc/apt/sources.list.d/docker.list

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

systemctl enable docker
systemctl start docker
usermod -aG docker ubuntu

mkdir -p /opt/cartlabs
chown ubuntu:ubuntu /opt/cartlabs

cat >/etc/motd <<'MOTD'
CartLabs host is ready.

Next:
  1. Copy or clone the CartLabs repo into /opt/cartlabs
  2. cd /opt/cartlabs
  3. docker compose up -d --build
MOTD
