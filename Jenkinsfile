pipeline {
    agent any
    environment {
        // Project specific properties
        ARTIFACTORY_CREDENTIALS_ID = 'svc-artifactory'
        PROJECT_NAME = 'prsadata'
        CONTAINER_NAME = "${PROJECT_NAME}/skat-python"
        // Build specific properties
        JGITVER_VERSION = '0.12.0'
        JGITVER_COMMAND =  "java -jar ./jgitver-${JGITVER_VERSION}-executable.jar --useDirty"
        JGITVER_BRANCH = "${BRANCH_NAME}"
        HOME = "${env.WORKSPACE}"
    }

    options {
      disableConcurrentBuilds()
      timeout(time: 60, unit: 'MINUTES')
    }
    // one every day between midnight and 6am
    triggers {
      cron('H H(0-6) * * *')
    }

    stages {
      stage('Fetch jgitver and resolve software version') {
        steps {
          // jgitver details: https://github.ccta.dk/devops/onboarding-demo-jgitver
          sh '''
              curl https://artifactory.ccta.dk/libs-release/fr/brouillard/oss/jgitver/${JGITVER_VERSION}/jgitver-${JGITVER_VERSION}-executable.jar > jgitver-${JGITVER_VERSION}-executable.jar
              SKAT_CONTAINER_VERSION=$(${JGITVER_COMMAND})
              echo ${SKAT_CONTAINER_VERSION}
          '''
        }
      }
      stage('build') {
        steps {
          withCredentials([usernamePassword(credentialsId: "${env.ARTIFACTORY_CREDENTIALS_ID}", passwordVariable: 'PW', usernameVariable: 'USERNAME')]) {
              sh '''
                  docker login -u ${USERNAME} -p ${PW} docker.artifactory.ccta.dk/${CONTAINER_NAME}
                  export VERSION=$(${JGITVER_COMMAND})
                  docker build -t docker.artifactory.ccta.dk/${CONTAINER_NAME}:${VERSION} .
              '''
          }
        }
      }
      stage('push') {
        steps {
          sh '''
              export VERSION=$(${JGITVER_COMMAND})
              docker push docker.artifactory.ccta.dk/${CONTAINER_NAME}:${VERSION}
          '''
        }
      }
      stage('Tag and push "latest" when master') {
        when {
          branch 'master'
        }
        steps {
          withCredentials([usernamePassword(credentialsId: "${env.ARTIFACTORY_CREDENTIALS_ID}", passwordVariable: 'PW', usernameVariable: 'USERNAME')]) {
            sh '''
              docker login -u ${USERNAME} -p ${PW} $docker.artifactory.ccta.dk/${CONTAINER_NAME}
              export VERSION=$(${JGITVER_COMMAND})
              docker build -t docker.artifactory.ccta.dk/${CONTAINER_NAME}:latest .
              curl -u ${USERNAME}:${PW} -X DELETE https://artifactory.ccta.dk/${PROJECT_NAME}-docker-local/${CONTAINER_NAME}/latest
              docker push docker.artifactory.ccta.dk/${CONTAINER_NAME}:latest
            '''
          }
        }
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
        cleanWs()
      }
    }
}