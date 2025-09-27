pipeline {
    agent any
    
    environment {
        BASE_URL = "https://gatransnetworksejahtera.co.id"
        HEADLESS = "true"
    }
    
    triggers {
        cron('H * * * *')
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/santosomichael/website-monitoring.git', branch: 'master'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t login-monitor-image .'
            }
        }

        stage('Run Login Test') {
            post {
                always {
                    sh "docker cp login-test-container:/app/screenshots/. ./screenshots || true"
                    sh "docker rm -f login-test-container"
                }
            }
            steps {
                withCredentials([
                    string(credentialsId: 'LOGIN_USERNAME', variable: 'LOGIN_USERNAME_ENV'),
                    string(credentialsId: 'LOGIN_PASSWORD', variable: 'LOGIN_PASSWORD_ENV'),
                    string(credentialsId: 'TELEGRAM_BOT_TOKEN', variable: 'TELEGRAM_BOT_TOKEN_ENV'),
                    string(credentialsId: 'TELEGRAM_CHAT_ID', variable: 'TELEGRAM_CHAT_ID_ENV')
                ]) {
                    sh "mkdir -p screenshots"
                    
                    sh """
                        docker run \\
                            --name login-test-container \\
                            -e BASE_URL=${env.BASE_URL} \\
                            -e LOGIN_USERNAME=${LOGIN_USERNAME_ENV} \\
                            -e LOGIN_PASSWORD=${LOGIN_PASSWORD_ENV} \\
                            -e HEADLESS=${env.HEADLESS} \\
                            -e TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN_ENV} \\
                            -e TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID_ENV} \\
                            login-monitor-image
                    """
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
            sh 'docker rmi login-monitor-image || true'
            cleanWs()
        }
    }
}

