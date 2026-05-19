pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
    buildDiscarder(logRotator(numToKeepStr: '20'))
  }

  parameters {
    string(name: 'REPO_URL', defaultValue: 'https://github.com/YOUR_USERNAME/cartlabs.git', description: 'GitHub repository URL used by the EC2 deploy script')
    string(name: 'DEPLOY_PATH', defaultValue: '/opt/cartlabs', description: 'Application directory on production EC2')
    string(name: 'PUBLIC_API_BASE_URL', defaultValue: 'http://13.200.16.11:8000/api', description: 'Frontend API URL baked into the production build')
    string(name: 'DEPLOY_BRANCH', defaultValue: 'main', description: 'Branch to deploy')
  }

  environment {
    COMPOSE_PROJECT_NAME = 'cartlabs'
    DOCKER_BUILDKIT = '1'
  }

  stages {
    stage('Guard Secrets') {
      steps {
        sh '''
          set -eu
          FOUND="$(find . -path ./.git -prune -o -path ./frontend/node_modules -prune -o -type f \\( -name '*.pem' -o -name '.env' -o -name '.env.*' \\) -print)"
          if [ -n "$FOUND" ]; then
            echo "$FOUND"
            echo "Secret-like files must not be committed or deployed."
            exit 1
          fi
        '''
      }
    }

    stage('Backend Syntax Check') {
      steps {
        sh 'python3 -m compileall backend'
      }
    }

    stage('Frontend Build Check') {
      steps {
        dir('frontend') {
          sh 'npm ci --cache .npm-cache'
          sh 'VITE_API_BASE_URL="${PUBLIC_API_BASE_URL}" npm run build'
        }
      }
      post {
        always {
          sh 'rm -rf frontend/.npm-cache frontend/dist'
        }
      }
    }

    stage('Docker Compose Config Check') {
      steps {
        sh 'PUBLIC_API_BASE_URL="${PUBLIC_API_BASE_URL}" docker compose -f docker-compose.yml -f docker-compose.prod.yml config'
      }
    }

    stage('Deploy Locally On EC2') {
      when {
        expression { params.DEPLOY_BRANCH == 'main' }
      }
      steps {
        sh '''
          chmod +x scripts/deploy-prod.sh
          REPO_URL="${REPO_URL}" \
          PUBLIC_API_BASE_URL="${PUBLIC_API_BASE_URL}" \
          DEPLOY_BRANCH="${DEPLOY_BRANCH}" \
          DEPLOY_PATH="${DEPLOY_PATH}" \
          scripts/deploy-prod.sh
        '''
      }
    }
  }

  post {
    success {
      echo 'CartLabs CI/CD pipeline completed successfully.'
    }
    failure {
      echo 'CartLabs CI/CD pipeline failed. Check the failed stage logs.'
    }
  }
}
