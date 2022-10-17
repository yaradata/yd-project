pipeline {
    agent any 

    environment {
        auth_folder = "${WORKSPACE}/backend/auth"
        project_folder = "${WORKSPACE}/backend/project"
    }

    stages {
        stage('Docker Build') {
            steps{
                // build docker image 
                sh "cd  $auth_folder && docker build -t auth ."
                // clean docker dangling image
                script {
                    try {
                        sh "docker rmi \$(docker images -f 'dangling=true' -q)"
                    } catch (Exception e) {
                        echo 'Exception occurred: ' + e.toString() 
                    } 
                } 
            }
        } 

        stage('Push image to docker hub') {
            steps {
                script {
                    // my-image:${env.BUILD_ID}
                    sh 'echo "70077007/$IMAGE_TAG_NAME:$BUILD_NUMBER"'
                    docker.withRegistry('', 'dockerHub-access' ) {
                        def customImage = docker.build("70077007/$IMAGE_TAG_NAME:$BUILD_NUMBER")
                        customImage.push()
                     }
                }
            }
        }
        
        stage('Kubernetes Deploy') {
            steps{
                echo "deploy" 
            }
        }
    }
    
}

