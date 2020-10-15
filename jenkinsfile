pipeline {
    agent {
        docker { 
            image 'docker.artifactory.ccta.dk/prsadata/skat-python'    
            registryUrl 'https://docker.artifactory.ccta.dk'
            registryCredentialsId 'b2f24be0-9416-41cb-90c5-4d028be11c4d'
            args '-u root:sudo'
        }
    } 
    environment {
        AMBARI_ACCESS_KEY_ID = credentials('AmbariToken')    }
    stages {
        stage('Build') {
            steps {
                echo 'Building..'
                git branch: 'development', credentialsId: '450a16eb-3a60-49f7-9577-cd62c89a6c17', url: 'https://github.ccta.dk/Produktionssatte-datalosninger/Minitower.git'
                //sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
                echo 'POC test'
                sh 'export PYTHONUNBUFFERED=1'
                //sh 'python -m pytest --junitxml=build/results.xml'
            }
        }/*
        stage('Deploy') {
            steps {
                echo 'Deploying to git'
                withCredentials([usernamePassword(credentialsId: '450a16eb-3a60-49f7-9577-cd62c89a6c17	', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                    sh('git checkout production')
                    sh('git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.ccta.dk/Produktionssatte-datalosninger/Ambari-Api-monitoring.git')
                }  
            }*/
        }
    }
        post {
            success {
                office365ConnectorSend color: '#228B22', status: "SUCCESS", webhookUrl: 'https://outlook.office.com/webhook/2f1278cc-6b4a-44ae-b5b5-879d94478eb4@2e93f0ed-ff36-46d4-9ce6-e0d902050cf5/JenkinsCI/0dee296ef2124a129bf54d200b3a403a/53a3382b-078e-413b-b721-a317b57b730a'
            }
            failure {
                office365ConnectorSend color: '#FF0000', status: "FAILED", webhookUrl: 'https://outlook.office.com/webhook/2f1278cc-6b4a-44ae-b5b5-879d94478eb4@2e93f0ed-ff36-46d4-9ce6-e0d902050cf5/JenkinsCI/0dee296ef2124a129bf54d200b3a403a/53a3382b-078e-413b-b721-a317b57b730a'
            }
            always {
                // Deletes the Jenkins workspace (local copy of Repo).
                cleanWs deleteDirs: true
            }
        }
}