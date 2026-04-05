pipeline{
    agent any

    stages{
        stage('Cloning GitHub Repo to Jenkins')
        steps{
            script{
                echo 'Cloning GitHub Repo to Jenkins'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'hotel-management', url: 'https://github.com/Shreyaan16/Hotel-Management.git']])
            }
        }
    }   
}