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
            steps {
                withCredentials([
                    string(credentialsId: 'LOGIN_USERNAME', variable: 'LOGIN_USERNAME_ENV'),
                    string(credentialsId: 'LOGIN_PASSWORD', variable: 'LOGIN_PASSWORD_ENV')
                ]) {
                    // --- ADD THIS LINE ---
                    // Ensure the screenshots directory exists on the host before mounting it
                    sh "mkdir -p screenshots"
                    
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
            // This will now find the screenshots successfully
            archiveArtifacts artifacts: 'screenshots/**/*.png', allowEmptyArchive: true
            sh 'docker rmi login-monitor-image || true'
            cleanWs()
        }
    }
}

