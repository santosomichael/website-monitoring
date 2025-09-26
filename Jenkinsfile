// File: Jenkinsfile
pipeline {
    agent any
    triggers {
        // Corrected: 'H * * * *' runs the job once per hour.
        cron('H * * * *')
    }
    stages {
        // Added back: This stage is essential to get your code.
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/santosomichael/website-monitoring', branch: 'master'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t login-monitor-image .'
            }
        }

        stage('Run Login Test') {
            steps {
                // Removed '|| true' so that the build will fail if the tests fail.
                sh "docker run --rm -v '${env.WORKSPACE}/screenshots:/app/screenshots' login-monitor-image"
            }
        }
    }
    post {
        always {
            // This saves your screenshots after every run.
            archiveArtifacts artifacts: 'screenshots/**/*.png', allowEmptyArchive: true
            
            // Added: Good practice to clean up the Docker image after the run.
            sh 'docker rmi login-monitor-image || true'
            
            // This cleans the workspace to save disk space.
            cleanWs()
        }
    }
}