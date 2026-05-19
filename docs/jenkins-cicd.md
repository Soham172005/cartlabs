# CartLabs Jenkins CI/CD

This pipeline validates and deploys CartLabs to the single EC2 instance created by Terraform.

## What The Pipeline Does

1. Blocks secret-like files such as `.pem` and `.env`.
2. Compiles Django service Python files.
3. Installs frontend dependencies and runs a Vite production build.
4. Validates Docker Compose configuration.
5. SSHes into the EC2 instance.
6. Pulls the latest `main` branch into `/opt/cartlabs`.
7. Builds and restarts CartLabs with Docker Compose.

## Jenkins Requirements

Install these Jenkins plugins:

- Git
- Pipeline
- SSH Agent

The Jenkins agent needs:

- Git
- Python 3
- Node.js 20+
- Docker and Docker Compose plugin, if you want local Compose validation

Use a Linux agent for this Jenkinsfile. The deploy stage uses `ssh`, `scp` and shell scripts.

## Jenkins Credentials

Create an SSH private key credential:

- Kind: `SSH Username with private key`
- ID: `cartlabs-ec2-ssh-key`
- Username: `ubuntu`
- Private key: contents of your `cart_labs.pem`

Do not commit the `.pem` file to GitHub.

## Pipeline Job Setup

1. Push this repository to GitHub.
2. In Jenkins, create a `Pipeline` or `Multibranch Pipeline` job.
3. Point it to the GitHub repository.
4. Use `Jenkinsfile` from SCM.
5. Set parameters:

```text
REPO_URL=https://github.com/YOUR_USERNAME/cartlabs.git
DEPLOY_HOST=13.200.16.11
DEPLOY_USER=ubuntu
DEPLOY_PATH=/opt/cartlabs
PUBLIC_API_BASE_URL=http://13.200.16.11:8000/api
GIT_BRANCH=main
```

## First Deployment

If Jenkins runs on a separate machine, set `REPO_URL` on the EC2 deploy command or ensure `/opt/cartlabs` already contains the cloned repository.

Manual first clone option:

```bash
cd /opt
sudo rm -rf cartlabs
sudo git clone https://github.com/YOUR_USERNAME/cartlabs.git cartlabs
sudo chown -R ubuntu:ubuntu /opt/cartlabs
```

Then Jenkins can keep it updated.

## Production URLs

With `docker-compose.prod.yml`, the frontend runs through Nginx on:

```text
http://13.200.16.11
```

The API gateway remains available on:

```text
http://13.200.16.11:8000
```
