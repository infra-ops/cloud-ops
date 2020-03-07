import groovy.json.JsonOutput

timestamps {
 def deploy_Env = null
 def jobName = null
 def microSvcName = null
 def app
 def gitCreds = 'AWGITTAPP'
 // def gitCreds =  '32f2c3c2-c19e-431a-b421-a4376fce1186'
 def shortGitCommit = null
 def environment = null
 def branch = 'master'
 def BRANCH_NAME = 'master'



      final String STAGING     = "staging"
      final String PRODUCTION  = "production"

      def wepackCfg
      def imageTag
      def serviceName
      def taskFamily
      def dockerFilePrefix
      def clusterName


 

      def remoteImageTag  = "${BUILD_NUMBER}"
      def ecRegistry      = "https://758637906269.dkr.ecr.us-east-1.amazonaws.com/connector-dev"
      def awscred		  = "ecr:us-east-1:aws_cred_id"
	  def repo  		  = "758637906269.dkr.ecr.us-east-1.amazonaws.com/connector-dev"

stage('Execute Build') {
  node('ec2') {
   
stage('Set Variables') {
  node {
   //echo sh(returnStdout: true, script: 'env')
   deploy_Env = env.BRANCH_NAME
   jobName = env.JOB_NAME
   projectName = jobName
   environment = "${deploy_Env}"
  }
 }  

try {
    stage('Build') {
     
     dir('pythona-app-test') {
      //deleteDir()
      git url: "https://github.com/nik786/pythona-app-test.git", branch: "${branch}", credentialsId: "${gitCreds}"
	  sh 'printenv'
      def GIT_COMMIT_HASH = sh(script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
      shortGitCommit = GIT_COMMIT_HASH[0..6]
      

      stage("Docker build") {
	   docker.withRegistry(ecRegistry, "${awscred}") {
        sh "docker build --no-cache -t ${repo}:${remoteImageTag} \
                                    -f ./Dockerfile ."
	   }
      }

     stage("Docker push") {
        // NOTE:
        //  ecr: is a required prefix
        //  aws_cred_id: is the credentials ID located in the jenkins credentials
        //
        docker.withRegistry(ecRegistry, "${awscred}") {
          docker.image("${repo}:${remoteImageTag}").push(remoteImageTag)
		  currentBuild.result = 'SUCCESS'
        }
      }
    }
  }

	stage ('Deploy on ECS')
	IMAGE_NO = sh (
		script: 'aws ecr describe-images --repository-name connector-dev --query \'sort_by(imageDetails,& imagePushedAt)[-1].imageTags[0]\' --output text',
		returnStdout: true
	  ).trim()
	  echo "IMAGE_NO=${IMAGE_NO}"
    
    def payload = readJSON text: JsonOutput.toJson([
        region: "us-east-1", 
        service: "python-task",
        cluster: "connector-clus",
        image: "${repo}:${IMAGE_NO}"
        ])
	String outputFile="imagepayload.json"
	writeJSON file: outputFile, json: payload, pretty: 2
	def svcURL="https://1scjp21jd2.execute-api.us-east-1.amazonaws.com/prod/service"
	sh "curl -X POST -H \"Content-Type: application/json\" -H \"x-api-key:6bKBEiiGF48qgdLymE4tO2GuTyklu8IZ6P1doBh8\" -d @${outputFile} ${svcURL}"
	currentBuild.result = 'SUCCESS' 

   stage('execute smoke test'){
		  ansiblePlaybook \
			  playbook: '/etc/ansible/helo.yml',
			  inventory: '/etc/ansible/inventories/local.yml'/*,
			  extraVars: [
				  ansible_ssh_user: "$SSH_USR",
				  ansible_ssh_pass: "$SSH_PSW",
				  ansible_become_pass: "$SSH_PSW",
				  current_directory: "$WORKSPACE"
			  ]*/
        }

   stage('deployemt successful'){
            sh "python /etc/ansible/helo.py"
          }
 
   stage('deployemt notification'){
            sh "sh /etc/ansible/helo.sh"
          }
  } 
 finally {
    if (currentBuild.result == 'SUCCESS') {
     stage 'Announce'
   
    }
   }
  }
}
}
