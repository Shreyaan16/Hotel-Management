pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        ACR_REGISTRY = 'hotelmanagementacr.azurecr.io'
        IMAGE_NAME = 'hotel-reservation'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }


    stages{
        stage('Cloning GitHub Repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning GitHub Repo to Jenkins'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'hotel-management', url: 'https://github.com/Shreyaan16/Hotel-Management.git']])
                }
            }
        }

        stage('Setup Python Virtual Environment'){
            steps{
                script{
                    echo 'Setting up Python virtual environment'
                    sh '''
                        python3 -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Build Docker Image'){
            steps{
                withCredentials([
                    string(credentialsId: 'azure-container-name', variable: 'AZURE_CONTAINER_NAME'),
                    string(credentialsId: 'azure-blob-name', variable: 'AZURE_BLOB_NAME'),
                    string(credentialsId: 'azure-storage-connection-string', variable: 'AZURE_STORAGE_CONNECTION_STRING')
                ]){
                    script{
                        echo 'Building Docker image'
                        sh """
                            docker build \
                              --build-arg AZURE_CONTAINER_NAME="\${AZURE_CONTAINER_NAME}" \
                              --build-arg AZURE_BLOB_NAME="\${AZURE_BLOB_NAME}" \
                              --build-arg AZURE_STORAGE_CONNECTION_STRING="\${AZURE_STORAGE_CONNECTION_STRING}" \
                              -t ${ACR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} .
                        """
                    }
                }
            }
        }

        stage('Push to Azure Container Registry'){
            steps{
                withCredentials([usernamePassword(
                    credentialsId: 'acr-credentials',
                    usernameVariable: 'ACR_USERNAME',
                    passwordVariable: 'ACR_PASSWORD'
                )]){
                    script{
                        echo 'Pushing image to ACR'
                        sh '''
                            docker login ${ACR_REGISTRY} -u ${ACR_USERNAME} -p ${ACR_PASSWORD}
                            docker push ${ACR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                            docker tag ${ACR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} ${ACR_REGISTRY}/${IMAGE_NAME}:latest
                            docker push ${ACR_REGISTRY}/${IMAGE_NAME}:latest
                        '''
                    }
                }
            }
        }
    }
}