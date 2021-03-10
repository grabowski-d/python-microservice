pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Test python app') {
            agent {
                docker { image 'python:3.8.8-slim-buster' }
            }
            steps {
                script {
                    dir('app') {
                        sh '''
                            python -m venv env
                            env/bin/pip install -r requirements-dev.txt
                            env/bin/pytest . --junit-xml=pytest_junit.xml
                        '''
                    }
                }
            }
            post {
                always {
                    junit testResults: '**/*pytest_junit.xml'
                }
            }
        }
        stage('Build & test docker image') {
            steps {
                script {
                    appImage = docker.build('greeter:latest')

                    sh label: 'Install dgoss', script: '''
                        curl -s -L https://github.com/aelsabbahy/goss/releases/latest/download/goss-linux-amd64 -o goss
                        curl -s -L https://github.com/aelsabbahy/goss/releases/latest/download/dgoss -o dgoss
                        chmod +rx *goss
                    '''
                    
                    withEnv(["GOSS_OPTS=-f junit", 'GOSS_PATH=./goss']) {
                        sh label: 'run image tests', script: './dgoss run greeter:latest > goss_junit.xml'
                    }
                }
            }
            post {
                always {
                    junit testResults: '**/*goss_junit.xml'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    docker.withRegistry('https://registry.example.com', 'credentials-id') {
                        appImage.push('latest')
                    }
                }
            }
        }
    }
    post {
        cleanup {
            script { cleanWs() }
        }
    }
}