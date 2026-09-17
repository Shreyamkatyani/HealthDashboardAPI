pipeline {
    agent any

    environment {
        APP_NAME = "system-health-dashboard"
        IMAGE_TAG = "${APP_NAME}:${BUILD_NUMBER}"
        CONTAINER_PORT = "5000"
        HOST_PORT = "5000"
        CONTAINER_NAME = "health-dashboard-test-${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source repository...'
                checkout scm
            }
        }

        stage('Install') {
            steps {
                echo 'Installing application and test dependencies...'
                bat '''
                    python3 -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated test suite with pytest...'
                // If any test fails, pytest exits with non-zero code, stopping the pipeline
                bat 'pytest -v tests/'
            }
        }

        stage('Build') {
            steps {
                echo "Building Docker image: ${IMAGE_TAG}..."
                bat "docker build -t ${IMAGE_TAG} ."
            }
        }

        stage('Tag') {
            steps {
                echo "Tagging Docker image with build number and latest..."
                bat """
                    docker tag ${IMAGE_TAG} ${APP_NAME}:latest
                    docker images | grep ${APP_NAME}
                """
            }
        }

        stage('Health check') {
            steps {
                echo 'Running container and verifying /health endpoint...'
                bat """
                    docker run -d --name ${CONTAINER_NAME} -p ${HOST_PORT}:${CONTAINER_PORT} -e APP_ENV=test ${IMAGE_TAG}
                    sleep 3
                    curl --fail --retry 3 --retry-delay 2 http://localhost:${HOST_PORT}/health
                """
            }
        }
    }

    post {
        always {
            echo 'Cleaning up temporary health-check container...'
            bat "docker rm -f ${CONTAINER_NAME} || true"
        }
        success {
            echo "Pipeline passed successfully! Image ${IMAGE_TAG} built, tagged, and verified."
        }
        failure {
            echo 'Pipeline failed. Halting workflow.'
        }
    }
}
