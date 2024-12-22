pipeline {
    agent any
    environment {
        SOURCE_FILE = './Dockerfile'
        TARGET_HOST = '192.168.153.132'
        TARGET_PATH = '/home/sadmin/testdir'
    }
    stages {
        stage('Send Dockerfile to Target Machine') {
            steps {
                sh '''
                scp $SOURCE_FILE sadmin@$TARGET_HOST:$TARGET_PATH/Dockerfile
                '''
            }
        }
        stage('Build and Run Docker Container') {
            steps {
                sh '''
                ssh sadmin@$TARGET_HOST "cd $TARGET_PATH && docker build -t myapp . && docker run -d -p 80:80 myapp"
                '''
            }
        }
    }
}
