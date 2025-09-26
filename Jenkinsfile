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
                    string(credentialsId: 'LOGIN_PASSWORD', variable: 'LOGIN_PASSWORD_ENV')
                ]) {
                    sh "mkdir -p screenshots"
                    
                    sh """
                        docker run \\
                            --name login-test-container \\
                            -e BASE_URL=${env.BASE_URL} \\
                            -e LOGIN_USERNAME=${LOGIN_USERNAME_ENV} \\
                            -e LOGIN_PASSWORD=${LOGIN_PASSWORD_ENV} \\
                            -e HEADLESS=${env.HEADLESS} \\
                            login-monitor-image
                    """
                }
            }
        }
    }
    post {
        success {
            withCredentials([
                string(credentialsId: 'TELEGRAM_CHAT_ID', variable: 'CHAT_ID')
            ]) {
                // CORRECTED: The token is no longer needed here.
                // The plugin will use the bot configured in "Manage Jenkins > System".
                telegramSend(
                    chatId: CHAT_ID,
                    message: "✅ SUCCESS: Jenkins Job '${env.JOB_NAME}' - Build #${env.BUILD_NUMBER}\n\nBuild completed successfully.\n[View Build](${env.BUILD_URL})"
                )
            }
        }
        failure {
            withCredentials([
                string(credentialsId: 'TELEGRAM_CHAT_ID', variable: 'CHAT_ID')
            ]) {
                // CORRECTED: The token is no longer needed here.
                telegramSend(
                    chatId: CHAT_ID,
                    message: "❌ FAILED: Jenkins Job '${env.JOB_NAME}' - Build #${env.BUILD_NUMBER}\n\nThe login test may have failed. Please check the console output immediately.\n[View Build](${env.BUILD_URL})"
                )
            }
        }
        always {
            archiveArtifacts artifacts: 'screenshots/*.png', allowEmptyArchive: true
            sh 'docker rmi login-monitor-image || true'
            cleanWs()
        }
    }
}

