pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry'
        APP_NAME = 'fastapi-cloud-project'
        KUBECONFIG = credentials('kubeconfig')
    }
    
    stages {
        stage('Build') {
            steps {
                script {
                    docker.build("${DOCKER_REGISTRY}/${APP_NAME}:${env.BUILD_ID}")
                }
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker run --rm ${DOCKER_REGISTRY}/${APP_NAME}:${env.BUILD_ID} python -m pytest'
            }
        }
        
        stage('Push') {
            steps {
                script {
                    docker.withRegistry('https://${DOCKER_REGISTRY}', 'dockerhub-credentials') {
                        docker.image("${DOCKER_REGISTRY}/${APP_NAME}:${env.BUILD_ID}").push()
                    }
                }
            }
        }
        
        stage('Deploy to K8s') {
            steps {
                sh '''
                    kubectl set image deployment/fastapi-app fastapi-app=${DOCKER_REGISTRY}/${APP_NAME}:${env.BUILD_ID}
                    kubectl rollout status deployment/fastapi-app
                '''
            }
        }
    }
}