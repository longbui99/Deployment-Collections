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
        DOCKER_LOGIN = "docker_builong99"
        DOCKER_CRED = credentials("docker_builong99")
        DOCKER_IMG = "rslve-odoo-17"
        DOCKER_REBUILD = false
        
        HOST_SERVICE_NAME = "rslve-erp"


        SETUP_FOLDER = "./.cicd/1_setup"
        BUILD_FOLDER = "./.cicd/2_build"
        SYNC_FOLDER = "./.cicd/1_setup"
        TEST_FOLDER = "./.cicd/1_setup"
        UPGRADE_FOLDER = "./.cicd/1_setup"
    }

    stages {
        stage('1.Setup') {
            steps {
                echo "============================ 1. SETUP ====================================================="
                echo "============================ 1.1 MAKE CICD FOLDER ========================================="
                sh """
                    rm -rf .cicd
                    mkdir -p .cicd
                    mv ./* ./.cicd
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
                script {
                    echo DOCKER_REBUILD
                    if (env.DOCKER_REBUILD == true){
                        echo "============================ 2.1 BUILD & PUSH DOCKER IMMAGE =============================" 
                        docker.withRegistry('https://registry.hub.docker.com', "$DOCKER_LOGIN") {
                            def customImage = docker.build("$DOCKER_CRED_USR/$DOCKER_IMG", "-f $BUILD_FOLDER/Dockerfile $BUILD_FOLDER")
                            customImage.push()
                        }
                    } else {
                        echo "============================ 2.1 SKIP BUILD & PUSH DOCKER IMMAGE =============================" 
                    }
                }
            }
        }
        stage("3. Sync"){
            steps {
                echo "============================ 3. SYNC ====================================================="
                sshagent(['longbui_azure_ssh']) {
                    echo "============================ 3.1 SYNC CODE================================================"
                    sh """ ssh $HOST_CREDS_USR@$HOST_IP -o StrictHostKeyChecking=no 'rm -rf $HOST_WORKSPACE/' """
                    sh """ rsync -avzO --exclude "__pycache__" -e "ssh -l $HOST_CREDS_USR -o StrictHostKeyChecking=no" "$env.WORKSPACE/" "$HOST_CREDS_USR@$HOST_IP:$HOST_WORKSPACE/" """
                    echo "============================ 3.2 PULL LATEST IMAGE========================================"
                    sh """ docker rmi "$DOCKER_CRED_USR/$DOCKER_IMG" && docker pull "$DOCKER_CRED_USR/$DOCKER_IMG" """
                }
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
                sshagent(['longbui_azure_ssh']) {
                    sh """ ssh -l $HOST_CREDS_USR -o StrictHostKeyChecking=no" "systemctl restart $HOST_SERVICE_NAME """
                }

            }
        }
    }
}
