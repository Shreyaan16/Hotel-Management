pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
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
    }
}