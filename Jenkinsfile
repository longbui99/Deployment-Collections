pipeline {
    agent any
    environment {
        SCM_REPO_URL = "https://github.com/longbui99/WorkTracking.git"
        SCM_BRANCH = "17.0"
        SCM_CREDENTIAL = "longbui99_github"
        HOST_CREDENTIAL = "longbui_azure_ssh"
        HOST_IP = "20.41.116.177"
        HOST_CREDS = credentials("longbui_azure_ssh")
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
                sshagent(['longbui_azure_ssh']) {
                    sh "ssh -o StrictHostKeyChecking=no $HOST_CREDS_USR@$HOST_IP 'cd /opt/odoo && pwd'"
                }
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
