pipeline {
    agent any
    environment {
        HOST_ODOO_SERVICE_NAME = "odoo"
        HOST_BUILD_WORKSPACE = "/opt/build"
        HOST_SERVICE = "/opt/services"
        HOST_ODOO_LAST_PRODUCTION = "/opt/previous-src"
        HOST_ODOO_BASE = "/opt/${env.HOST_ODOO_SERVICE_NAME}"
        HOST_CICD_WORKSPACE = "${env.HOST_BUILD_WORKSPACE}/cicd/production"
        HOST_ENVIROMENT_FILE = "${env.HOST_SERVICE}/env/odoo_psql.env"
        HOST_UPGRADE_YAML_PATH = "${env.HOST_CICD_WORKSPACE}/5_upgrade/upgrade.yaml"
        // --
        HOST_SSH_CREDENTIAL = "longbui-vm"
        HOST_SSH_IP = "longbui-vm-ip"
        HOST_SSH_CREDS = credentials("${env.HOST_SSH_CREDENTIAL}")
        HOST_SSH_IP = credentials("${env.HOST_SSH_IP}")
        HOST_SSH_TIMEOUT = 10
        // --
        DOCKER_HUB_LOGIN = "docker_builong99"
        DOCKER_HUB_CRED = credentials("docker_builong99")
        DOCKER_HUB_IMG = "builong99/odoo:18"
        DOCKER_REBUILD = false
        DATABASE_UPGRADE_CHECK = false
        // --
        SCM_REPO_URL = "https://github.com/longbui99/RSLVE-Odoo.git"
        SCM_BRANCH = "production"
        SCM_CREDENTIAL = "longbui99_github"
        // ============================== DO NOT CHANGE ==============================
        // ===========================================================================
        // -- Sync from CICD branch
        HOST_SETUP_FOLDER = "${env.HOST_CICD_WORKSPACE}/1_setup"
        HOST_BUILD_FOLDER = "${env.HOST_CICD_WORKSPACE}/2_build"
        HOST_SYNC_FOLDER = "${env.HOST_CICD_WORKSPACE}/3_sync"
        HOST_CONFIG_FOLDER = "${env.HOST_CICD_WORKSPACE}/4_config"
        HOST_UPGRADE_FOLDER = "${env.HOST_CICD_WORKSPACE}/5_upgrade"
        HOST_BUILD_BASE = "${env.HOST_BUILD_WORKSPACE}/base"
        HOST_BUILD_RUNNER = "${env.HOST_BUILD_WORKSPACE}/.runner"
        // -- Setup in the server configured

        HOST_ODOO_BASE_SOURCE = "${env.HOST_SERVICE}/odoo_base"
        HOST_ODOO_CONFIG_PATH = "${env.HOST_ODOO_BASE}/.config/odoo.conf"
        HOST_ODOO_EXECUTION_PATH = "${env.HOST_ODOO_BASE}/base/odoo/odoo-bin"
        // --
        HOST_PRODUCTION_WORKSPACE = "${env.HOST_ODOO_BASE}"
        HOST_PRODUCTION_RUNNING_PATH = "${env.HOST_ODOO_BASE}/.runner"
        // ========================== END DO NOT CHANGE ==============================
        // ===========================================================================

    }

    // Stages Description
    // 1. Pull CICD resources to the main workspace
    // 2. Move the CICD resources to subdirectory: ./cicd
    // 3. Pull Odoo source code to the main workspace: $ls -a >> .cicd (folder) & resources
    // 4. BUILD IMAGE IF NEEDED
    // 5. Copy workspace to host to a build folder
    // 6. Generate odoo.conf file from config template
    // 7. Move the Build folder to main folder, and move the main folder to previous-release -> For safety revert
    // 8. Deploy by restart systemctl service

    stages {
        stage('1.Setup') {
            steps {
                echo "============================ 1. SETUP ====================================================="
                echo "============================ 1.1 MAKE CICD FOLDER ========================================="
                sh """
                    rm -rf cicd
                    mkdir -p .cicd
                    mv ./* ./.cicd
                    mv -f .cicd cicd
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
                        docker.withRegistry('https://registry.hub.docker.com', "$DOCKER_HUB_LOGIN") {
                            def customImage = docker.build("$DOCKER_HUB_CRED_USR/$DOCKER_HUB_IMG", "-f $HOST_BUILD_FOLDER/Dockerfile $HOST_BUILD_FOLDER")
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
                sshagent([env.HOST_SSH_CREDENTIAL]) {
                    echo "============================ 3.1 SYNC CODE================================================"
                    sh """ ssh $HOST_SSH_CREDS_USR@$HOST_SSH_IP -o StrictHostKeyChecking=no -o ConnectTimeout=$HOST_SSH_TIMEOUT 'sudo rm -rf $HOST_BUILD_WORKSPACE/' """
                    sh """ rsync -avzO --exclude="__pycache__" --exclude=.git -e "ssh -l $HOST_SSH_CREDS_USR -o StrictHostKeyChecking=no" "$env.WORKSPACE/" "$HOST_SSH_CREDS_USR@$HOST_SSH_IP:$HOST_BUILD_WORKSPACE/" """
                    
                    echo "============================ 3.2 PULL LATEST IMAGE========================================"
                    sh """ssh $HOST_SSH_CREDS_USR@$HOST_SSH_IP -o StrictHostKeyChecking=no -o ConnectTimeout=$HOST_SSH_TIMEOUT 'sudo docker pull "$DOCKER_HUB_CRED_USR/$DOCKER_HUB_IMG"'   """

                    echo "============================ 3.3 COPY BASE SOURCE ======================================"
                    sh """ ssh $HOST_SSH_CREDS_USR@$HOST_SSH_IP -o StrictHostKeyChecking=no -o ConnectTimeout=$HOST_SSH_TIMEOUT 'sudo cp -R -f $HOST_ODOO_BASE_SOURCE/* $HOST_BUILD_BASE'"""
                }
            }
        }
        stage("4. CONFIG"){
            steps {
                echo "============================ 4. CONFIG ====================================================="
                echo "============================ 4.1 GENERATE CONFIG FILE ======================================"
                sshagent([env.HOST_SSH_CREDENTIAL]) {
                    sh """ ssh $HOST_SSH_CREDS_USR@$HOST_SSH_IP -o StrictHostKeyChecking=no -o ConnectTimeout=$HOST_SSH_TIMEOUT 'sudo python3 $HOST_CONFIG_FOLDER/generate_config.py -e $HOST_ENVIROMENT_FILE'"""
                }
            }
        }
        stage("5. Upgrade"){
            steps {
                echo "============================ 5. UPGRADE ====================================================="

                echo "============================ 5.1 GENERATE & RUN UPGRADE BASH SCRIPT ==============================="
                sshagent([env.HOST_SSH_CREDENTIAL]) {
                    sh """ ssh $HOST_SSH_CREDS_USR@$HOST_SSH_IP -o StrictHostKeyChecking=no -o ConnectTimeout=$HOST_SSH_TIMEOUT 'sudo python3 $HOST_UPGRADE_FOLDER/upgrade.py -c $HOST_ODOO_CONFIG_PATH -d false -f $HOST_UPGRADE_YAML_PATH -e $HOST_ODOO_EXECUTION_PATH \
                    && sudo mv -f $HOST_UPGRADE_FOLDER/upgrade.sh $HOST_BUILD_RUNNER/run_upgrade.sh \
                    && sudo chmod +x $HOST_BUILD_RUNNER/run_upgrade.sh \
                    && sudo rm -rf $HOST_ODOO_LAST_PRODUCTION \
                    && sudo mv -f $HOST_PRODUCTION_WORKSPACE $HOST_ODOO_LAST_PRODUCTION \
                    && sudo mv -f $HOST_BUILD_WORKSPACE $HOST_PRODUCTION_WORKSPACE '"""
                    sh """ ssh $HOST_SSH_CREDS_USR@$HOST_SSH_IP -o StrictHostKeyChecking=no -o ConnectTimeout=$HOST_SSH_TIMEOUT 'sudo docker-compose -f $HOST_PRODUCTION_RUNNING_PATH/docker-compose.upgrade.yml up $HOST_ODOO_SERVICE_NAME' """
                }   
            }
        }
        stage("6. Deployment"){
            steps {
                echo "============================ 6. DEPLOY ====================================================="
                sshagent([env.HOST_SSH_CREDENTIAL]) {
                    sh """ ssh $HOST_SSH_CREDS_USR@$HOST_SSH_IP -o StrictHostKeyChecking=no -o ConnectTimeout=$HOST_SSH_TIMEOUT 'sudo systemctl restart $HOST_ODOO_SERVICE_NAME' """
                }
            }
        }
    }
}
