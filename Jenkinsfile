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
                    mkdir -p .cicd
                    mv ./* ./.cicd
                    rm -rf .git
                """
                echo "============================ 1.2 PULL GITHUB PROJECT RESOURCE ============================="
                git url: "$SCM_REPO_URL",
                branch: "$SCM_BRANCH",
                credentialsId: "$SCM_CREDENTIAL"
            }
        }
        stage("2.Build"){
            steps {
                echo "============================ 2. BUILD ====================================================="
                echo "============================ 2.1 PULL GITHUB PROJECT RESOURCE =============================" 

            }
        }
        stage("3. Sync"){
            steps {
                echo "============================ 3. SYNC ====================================================="
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
        stage("4. Test"){
            steps {
                echo "============================ 4. TEST ====================================================="
            }
        }
        stage("5. Upgrade"){
            steps {
                echo "============================ 5. UPGRADE ====================================================="
            }
        }
        stage("6. Deployment"){
            steps {
                echo "============================ 6. DEPLOY ====================================================="
            }
        }
    }
}
