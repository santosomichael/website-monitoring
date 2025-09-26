pipeline {
    agent any
    
    // Define non-secret variables here
    environment {
        BASE_URL = "https://gatransnetworksejahtera.co.id"
        HEADLESS = "true" // Use "true" for automated runs in Jenkins
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
            steps {
                // Securely load the credentials you stored in Jenkins
                withCredentials([
                    string(credentialsId: 'LOGIN_USERNAME', variable: 'LOGIN_USERNAME_ENV'),
                    string(credentialsId: 'LOGIN_PASSWORD', variable: 'LOGIN_PASSWORD_ENV')
                ]) {
                    // CORRECTED: Pass the variables into the Docker container using the -e flag
                    // The """ allows for a multi-line command for readability
                    sh """
                        docker run --rm \\
                            -e BASE_URL=${env.BASE_URL} \\
                            -e LOGIN_USERNAME=${LOGIN_USERNAME_ENV} \\
                            -e LOGIN_PASSWORD=${LOGIN_PASSWORD_ENV} \\
                            -e HEADLESS=${env.HEADLESS} \\
                            -v "${env.WORKSPACE}/screenshots:/app/screenshots" \\
                            login-monitor-image
                    """
                }
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'screenshots/**/*.png', allowEmptyArchive: true
            sh 'docker rmi login-monitor-image || true'
            cleanWs()
        }
    }
}
