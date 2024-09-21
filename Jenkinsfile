pipeline {
    agent any
    environment {
        SCM_REPO_URL = "https://github.com/longbui99/WorkTracking.git"
        SCM_BRANCH = "17.0"
        SCM_CREDENTIAL = "longbui99_github"
        HOST_CREDENTIAL = "longbui_azure_ssh"
        HOST_IP = "20.41.116.177"
        HOST_CREDS = credentials("longbui_azure_ssh")
        HOST_WORKSPACE = "/opt/odoo"
        DOCKER_LOGIN = "builong99_docker"
    }

    stages {
        stage('1.Setup') {
            
            steps {
                echo "============================ 1. SETUP ====================================================="
                echo "============================ 1.1 MAKE CICD FOLDER ========================================="
                sh """
                    mv ./* ./copy
                """
                echo "============================ 1.2 PULL GITHUB PROJECT RESOURCE ============================="
                git url: "$SCM_REPO_URL",
                branch: "$SCM_BRANCH",
                credentialsId: "$SCM_CREDENTIAL"
            }
        }
        stage("2.Build"){
            steps {
                echo "============================ 1. SETUP ====================================================="
                echo "============================ 1.1 PULL GITHUB PROJECT RESOURCE =============================" 
            }
        }
        stage("3. Sync"){
            steps {
                // sshagent(['longbui_azure_ssh']) {
                //     sh """
                //     rsync -avzO \
                //         --exclude "__pycache__" \
                //         -e "ssh -l $HOST_CREDS_USR -o StrictHostKeyChecking=no" \
                //         "$env.WORKSPACE/" \
                //         "$HOST_CREDS_USR@$HOST_IP:$HOST_WORKSPACE/" \
                //     """
                // }
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
