timestamps {
def gitCreds = 'AWGITTAPP'
//def gitCreds = '32f2c3c2-c19e-431a-b421-a4376fce1186' 
 
 stage('Set Variables') {
  node {
   //echo sh(returnStdout: true, script: 'env')
   deploy_Env = env.BRANCH_NAME
   jobName = env.JOB_NAME
  }
 }

 stage('Execute Build') {
node('ec2'){
   projectName = "hello-tomcat-projects"
   environment = "${deploy_Env}" 
   branch      = jobName.split(/\//)[3]
  
 
 try {
    stage('Build') {
     stage 'Cleanup'
     deleteDir()

     stage 'Checkout'
     checkout scm
     dir('hello-tomcat-projects') {
      deleteDir()
      git url: "https://github.com/nik786/${projectName}.git", branch: "${branch}", credentialsId: "${gitCreds}"
      def GIT_COMMIT_HASH = sh(script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
      shortGitCommit = GIT_COMMIT_HASH[0..6]
  
 
  dt=`date "+%Y-%m-%d-%H-%M"`
  sh aws s3 cp /var/lib/jenkins/workspace/tom-test/target/mavenproject1-1.0-SNAPSHOT.war s3://hello-artifactory/$dt/mavenproject1-1.0-SNAPSHOT.war
  sh rm -rf /var/lib/jenkins/workspace/tom-test/target/mavenproject1-1.0-SNAPSHOT.war
  sh  aws s3 cp s3://hello-artifactory/$dt/mavenproject1-1.0-SNAPSHOT.war /var/lib/jenkins/workspace/tom-test
 
  stage 'Build and publish docker image'
  docker.withRegistry('https://758637906269.dkr.ecr.us-east-1.amazonaws.com/connector-dev', 'ecr:us-east-1:aws_cred_id') {
    docker.build("${env.BUILD_NUMBER}")
    currentBuild.result = 'SUCCESS'
  }
 
 

      
      
      
 sh b=${BUILD_NUMBER}
 sh echo $b
 sh sed "s/\("image".*\):\(22\)/\1:${b}/" /var/lib/jenkins/workspace/tom-test/tomcat-1-task.json > /var/lib/jenkins/workspace/tom-test/tmp_tomcat-1-task.json
 sh mv /var/lib/jenkins/workspace/tom-test/tmp_tomcat-1-task.json /var/lib/jenkins/workspace/tom-test/tomcat-1-task.json
 sh sudo scp -i /var/lib/jenkins/vpn41.pem -r /var/lib/jenkins/workspace/tom-test/tomcat-* ubuntu@34.201.25.132:/home/ubuntu/apps
 
 t=`aws ecs register-task-definition --cli-input-json file:///home/ubuntu/apps/tomcat-1-task.json | grep -i revision | cut -d ":" -f2 | sed 's/ //'`
 echo $t 
 aws ecs update-service --service test-service-4 --task-definition tomcat-webserver-2:$t --cluster connector-clus
   
     
     }



