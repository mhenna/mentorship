#!/usr/bin/env groovy
              
pipeline {

    agent {
        docker {
            image 'python:3'
            args '-u root'
        }
    }
    environment {
       DB_HOST = credentials('DB_HOST_MENT')
       DB_PORT = credentials('DB_PORT_MENT')
       DB_USER = credentials('DB_USER_MENT')
       DB_PASSWORD = credentials('DB_PASSWORD_MENT')
       DB_NAME = credentials('DB_NAME_MENT')
       SECRET_KEY = credentials('SECRET_KEY_MENT')
       DEFAULT_PASSWORD = credentials('DEFAULT_PASSWORD_MENT')
       ENV = credentials('ENV_MENT')
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'pip install -r requirments.txt'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'python manage.py test'
            }
        }
    }
}