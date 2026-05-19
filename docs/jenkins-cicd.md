# CartLabs Jenkins CI/CD

This pipeline validates and deploys CartLabs to the single EC2 instance created by Terraform.

## What The Pipeline Does

1. Blocks secret-like files such as `.pem` and `.env`.
2. Compiles Django service Python files.
3. Installs frontend dependencies and runs a Vite production build.
4. Validates Docker Compose configuration.
5. Pulls the latest `main` branch into `/opt/cartlabs` on the same EC2 host.
6. Builds and restarts CartLabs with Docker Compose.

## Jenkins Requirements

Install these Jenkins plugins:

- Git
- Pipeline

The Jenkins agent needs:

- Git
- Python 3
- Node.js 20+
- Docker and Docker Compose plugin, if you want local Compose validation

Use a Linux agent for this Jenkinsfile. For your low-credit setup, Jenkins runs on the same EC2 instance as CartLabs and deploys locally.

## EC2 Permissions

Allow the Jenkins user to use Docker and write to `/opt/cartlabs`:

```bash
sudo usermod -aG docker jenkins
sudo mkdir -p /opt/cartlabs
sudo chown -R jenkins:jenkins /opt/cartlabs
sudo systemctl restart jenkins
```

## Pipeline Job Setup

1. Push this repository to GitHub.
2. In Jenkins, create a `Pipeline` or `Multibranch Pipeline` job.
3. Point it to the GitHub repository.
4. Use `Jenkinsfile` from SCM.
5. Set parameters:

```text
REPO_URL=https://github.com/YOUR_USERNAME/cartlabs.git
DEPLOY_PATH=/opt/cartlabs
PUBLIC_API_BASE_URL=http://13.200.16.11:8000/api
DEPLOY_BRANCH=main
```

## First Deployment

Before the first deployment, make sure the Jenkins user owns the deployment directory:

```bash
sudo mkdir -p /opt/cartlabs
sudo chown -R jenkins:jenkins /opt/cartlabs
```

Then Jenkins can clone and keep it updated.

## Production URLs

With `docker-compose.prod.yml`, the frontend runs through Nginx on:

```text
http://13.200.16.11
```

The API gateway remains available on:

```text
http://13.200.16.11:8000
```
