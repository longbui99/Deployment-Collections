pipeline {
    agent any
    environment {
        SCM_REPO_URL = "https://github.com/longbui99/WorkTracking.git"
        SCM_BRANCH = "17.0"
        SCM_CREDENTIAL = "longbui99_github"
        HOST_CREDENTIAL = ""
    }

    stages {
        stage('Pull') {
            steps {
                git url: "$SCM_REPO_URL",
                branch: "$SCM_BRANCH",
                credentialsId: "$SCM_CREDENTIAL"
            }
        }
        stage("Sync"){
            steps {
                echo env.WORKSPACE
                sh "ls -a -l"
            }
            sshagent(credentials: [env.HOST_CREDENTIAL]){
                echo env.WORKSPACE
                sh '''
                    pwd
                '''
            }
        }
        stage("Test"){
            steps {
                echo "TEST"
            }
        }
        stage("Upgrade Module"){
            steps {
                echo "Upgrade Module"
            }
        }
        stage("Deployment"){
            steps {
                echo "DEPLOYMENT"
            }
        }
    }
}
