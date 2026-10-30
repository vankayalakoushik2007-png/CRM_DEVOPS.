
pipeline {
    agent any

    parameters {
        choice(
            name: 'VERSION',
            choices: ['v1', 'v2', 'v3'],
            description: 'Select CRM version to deploy'
        )
    }

    environment {
        DOCKER_IMAGE = '24mis0341/crm-devops'
        DOCKER_CREDENTIALS = 'dockerhub-creds'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Downloading CRM source code from GitHub'
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${VERSION}")
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    docker.withRegistry(
                        'https://index.docker.io/v1/',
                        DOCKER_CREDENTIALS
                    ) {
                        docker.image(
                            "${DOCKER_IMAGE}:${VERSION}"
                        ).push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    def deployment = "crm-${VERSION}"
                    def container = "crm-${VERSION}"
                    def yamlFile = "k8s/${VERSION}.yaml"
                    def image = "${DOCKER_IMAGE}:${VERSION}"

                    sh """
                        kubectl apply -f ${yamlFile}
                        kubectl set image deployment/${deployment} \
                        ${container}=${image}
                        kubectl rollout status deployment/${deployment}
                    """
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'kubectl get deployments'
                sh 'kubectl get pods'
                sh 'kubectl get services'
            }
        }
    }

    post {
        success {
            echo 'CRM CI/CD Pipeline completed successfully!'
        }

        failure {
            echo 'CRM CI/CD Pipeline failed. Check the console output.'
        }
    }
}
