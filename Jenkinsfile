pipeline {
    agent any
    environment {

        // ==================== DO NOT CHANGE ======================
        SETUP_FOLDER = "./.cicd/1_setup"
        BUILD_FOLDER = "./.cicd/2_build"
        SYNC_FOLDER = "./.cicd/3_sync"
        TEST_FOLDER = "./.cicd/4_test"
        UPGRADE_FOLDER = "./.cicd/5_upgrade"
        // ==================== END OF DO NOT CHANGE ======================

        SCM_REPO_URL = "https://github.com/longbui99/WorkTracking.git"
        SCM_BRANCH = "17.0"
        SCM_CREDENTIAL = "longbui99_github"

        HOST_CREDENTIAL = "longbui_azure_ssh"
        HOST_IP = "20.41.116.177"
        HOST_CREDS = credentials("longbui_azure_ssh")
        HOST_WORKSPACE = "/opt/odoo"
        HOST_SERVICE_NAME = "rslve-erp"
        HOST_CONFIG_PATH = "/opt/odoo/odoo.conf"
        HOST_EXECUTION_PATH = "/opt/odoo/odoo/odoo-bin"
        HOST_UPGRADE_YAML_PATH = "/opt/odoo/custom_addons/upgrade.yaml"
        SSH_TIMEOUT = 10

        DOCKER_LOGIN = "docker_builong99"
        DOCKER_CRED = credentials("docker_builong99")
        DOCKER_IMG = "rslve-odoo-17"
        DOCKER_REBUILD = false

        PSQL = credentials("psql_credential")
        PSQL_HOST = credentials("psql_host")

        DATABASE_UPGRADE_CHECK = false
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
                    sh """ ssh $HOST_CREDS_USR@$HOST_IP -o StrictHostKeyChecking=no -o ConnectTimeout=$SSH_TIMEOUT 'rm -rf $HOST_WORKSPACE/' """
                    sh """ rsync -avzO --exclude="__pycache__" --exclude=.git -e "ssh -l $HOST_CREDS_USR -o StrictHostKeyChecking=no" "$env.WORKSPACE/" "$HOST_CREDS_USR@$HOST_IP:$HOST_WORKSPACE/" """
                    
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

                echo "============================ 5.1 GET THE LIST OF DATABASE ==================================="
                script {
                    if (env.DATABASE_UPGRADE_CHECK == true){
                        env.DATABASES = sh(returnStdout: true, script: "PGPASSWORD=$PSQL_PSW psql -h $PSQL_HOST -p 5432 -U $PSQL_USR -d postgres -c '\\l'")     
                    }               
                }

                echo "============================ 5.2 GENERATE & RUN UPGRADE BASH SCRIPT ==============================="
                sshagent(['longbui_azure_ssh']) {
                    sh """
                        ssh $HOST_CREDS_USR@$HOST_IP -o StrictHostKeyChecking=no -o ConnectTimeout=$SSH_TIMEOUT
                        'cd $HOST_WORKSPACE \
                        && python3 $UPGRADE_FOLDER/upgrade.py -c $HOST_CONFIG_PATH -d $DATABASES -f $HOST_UPGRADE_YAML_PATH -e $HOST_EXECUTION_PATH\
                        && sudo chmod +x $UPGRADE_FOLDER/upgrade.sh
                        && $UPGRADE_FOLDER/upgrade.sh' 
                    """
                }   
            }
        }
        stage("6. Deployment"){
            steps {
                echo "============================ 6. DEPLOY ====================================================="
                sshagent(['longbui_azure_ssh']) {
                    sh """ ssh $HOST_CREDS_USR@$HOST_IP -o StrictHostKeyChecking=no -o ConnectTimeout=$SSH_TIMEOUT 'sudo systemctl restart $HOST_SERVICE_NAME' """
                }

            }
        }
    }
}
