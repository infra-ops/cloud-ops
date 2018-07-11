#!/bin/bash
#Requirments
TF_Binary=/usr/bin/terraform
if [ ! -f $TF_Binary ]; then
sudo apt-get update; apt-get install unzip ; wget https://releases.hashicorp.com/terraform/0.7.3/terraform_0.7.3_linux_amd64.zip -P /tmp ; unzip /tmp/terraform_0.7.3_linux_amd64.zip; chmod +x ./terraform ; sudo mv ./terraform /usr/bin/
fi
PIP_Binary=/usr/bin/pip
if [ ! -f $PIP_Binary ]; then
sudo apt-get install python-pip; sudo apt-get install python-boto; pip install -U boto
sudo pip install awscli --ignore-installed six
fi
#sudo curl -o /usr/local/bin/ecs-cli https://s3.amazonaws.com/amazon-ecs-cli/ecs-cli-linux-amd64-latest
##AWS Configure 
mkdir -p ~/.aws
echo '[default]' > ~/.aws/config
echo 'aws_access_key_id=AKIAJNKCE4Y3PWMAS6GQ' >> ~/.aws/config
echo 'aws_secret_access_key=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' >> ~/.aws/config
echo 'region=us-west-2' >> ~/.aws/config
echo 'output=json' >> ~/.aws/config

#Fucntions for S3
create_s3_bucket() {
                echo "Please enter a file with bucket names :"
                read bucket_name
                echo "Please enter AWS Region :"
                read region
                for i in `cat $bucket_name`
                do
                aws s3api create-bucket --bucket $i --region $region
                done
}
delete_s3_bucket() {
               echo "Please enter the file path with bucket name :"
               read bucket_name
               for i in `cat $bucket_name`
               do
               aws s3 rb s3://$i --force  
               done
}
upload_s3_file(){
               echo "Please enter file location on local host :"
               read file
               echo "Please enter s3 bucket name :"
               read bucket_name
               if [  -f "$file" ]; then
	       aws s3 cp $file s3://$bucket_name/$file
               else
               echo "$file not avilable"
               exit 0
               fi
}
download_s3_file(){
               echo "Please enter destination file name:"
               read file
               echo "Please enter bucket name:"
               read bucket
               echo "Please enter file in $bucket :"
               read remote_file
               aws s3 cp s3://$bucket/$remote_file $file
}

#Functions for ECS 
#create_container(){
#}

create_container_cluster(){
               echo "Please enter desired cluster name : "
               read cluster
               aws ecs create-cluster --cluster-name "$cluster"
}
#upload_docker(){
#}
#delete_container(){
#}
delete_container_cluster(){
               echo "Please enter cluster name to be deleted : "
               read cluster
               aws ecs delete-cluster --cluster $cluster
}

#Funtions for VPC
create_vpc(){
               echo "Please enter CIDR block:"
               read cidr
               aws ec2 create-vpc --cidr-block $cidr
}	
create_vpc_peering(){
               echo "Please enter origin vpc id : "
               read vpc_o
               echo "Please enter dest vpc id : "
               read vpc_d
               aws ec2 create-vpc-peering-connection --vpc-id $vpc_o --peer-vpc-id $vpc_d
}
attach_ig(){  
               echo "Please enter internet gateway id: "
               read ig
               echo "Please enter vpc id : "
               read vpcid
               aws ec2 attach-internet-gateway --internet-gateway-id $ig --vpc-id $vpcid
}
delete_vpc(){
               echo "Please enter vpc id:"
               read vpc
               aws ec2 delete-vpc --vpc-id $vpc
}
###############################################################################
## FUNCTION                                                                  ##
###############################################################################
##
## BRIEF: Instance Administrator.
## ----------------------------------------------------------------------------
##
function opt1() {
    while true; do
        clear
        echo "----------------------------------------------"
        echo " * * * * * * * * * * Menu * * * * * * * * * * "
        echo "----------------------------------------------"
        echo "OPTION: Instance Administration"
        echo ""
        echo "[a] Creation Of Instances"
        echo "[b] Deletion Of Instances"
        echo "[c] Execute provision script on Instances"
        echo ""
        echo "[0] Return to main menu"
        echo "----------------------------------------------"
        read -p "Enter your option choice [a-b,0]:" SUBMENU

        case ${SUBMENU} in
            0) return 1 ;;

            a) echo "Please specify the file name with instance details: "
               read instance
               cd ec2_create_destroy;  ./create_instance.sh $instance
               return 0 ;;

            b) echo "Please specify the file name with instance names: "
               read instance
               cd ec2_create_destroy;  ./delete_insatnce.sh $instance
               return 0 ;;

            *) echo -e "\nEnter with valid option!"
                sleep 3 ;;
        esac
    done
}


##
## BRIEF: S3 Bucket Administartion
## ----------------------------------------------------------------------------
##
function opt2() {
    while true; do
        clear
        echo "----------------------------------------------"
        echo " * * * * * * * * * * Menu * * * * * * * * * * "
        echo "----------------------------------------------"
        echo "OPTION: S3 Bucket Administartion"
        echo ""
        echo "[a] Creation Of Bucket"
        echo "[b] Deletion Of Bucket"
        echo "[c] Upload Of File"
        echo "[d] Download Of File"
        echo ""
        echo "[0] Return to main menu"
        echo "----------------------------------------------"
        read -p "Enter your option choice [a-d, 0]:" SUBMENU

        case ${SUBMENU} in
            0) return 1 ;;

            a) create_s3_bucket
               return 0 ;;

            b) delete_s3_bucket
               return 0 ;;

            c) upload_s3_file
               return 0 ;;

            d) download_s3_file
               return 0 ;;

            *) echo -e "\nEnter with valid option!"
                sleep 3 ;;
        esac
    done
}


##
## BRIEF: ECS Services
## ----------------------------------------------------------------------------
##
function opt3() {
    while true; do
        clear
        echo "----------------------------------------------"
        echo " * * * * * * * * * * Menu * * * * * * * * * * "
        echo "----------------------------------------------"
        echo "OPTION: ECS Services"
        echo ""
        echo "[a] Creation Of Container"
        echo "[b] Creation Of conatiner cluster"
        echo "[c] Upload docker container to ECS"
        echo "[d] Delete ecs container"
        echo "[e] Delete ecs conatainer cluster"
        echo ""
        echo "[0] Return to main menu"
        echo "----------------------------------------------"
        read -p "Enter your option choice [a-e, 0]:" SUBMENU

        case ${SUBMENU} in
            0) return 1 ;;

            a) echo 'a'
               return 0 ;;

            b) echo 'b'
               return 0 ;;

            c) echo 'c'
               return 0 ;;

            d) echo 'd'
               return 0 ;;

            e) echo 'e'
               return 0 ;;

            *) echo -e "\nEnter with valid option!"
               sleep 3 ;;
        esac
    done
}


##
## BRIEF: ElasticBeanStalk Administration
## ----------------------------------------------------------------------------
##
function opt4() {
    while true; do
        clear
        echo "----------------------------------------------"
        echo " * * * * * * * * * * Menu * * * * * * * * * * "
        echo "----------------------------------------------"
        echo "OPTION: ElasticBeanStalk Administration"
        echo ""
        echo "[a] Creation of ElasticBeanstalk"
        echo "[b] Deployment of container to Elasticbeanstalk"
        echo "[c] Deployment of application to Elasticbeanstalk"
        echo ""
        echo "[0] Return to main menu"
        echo "----------------------------------------------"
        read -p "Enter your option choice [a-c, 0]:" SUBMENU

        case ${SUBMENU} in
            0) return 1 ;;

            a) echo 'a'
               return 0 ;;

            b) echo 'b'
               return 0 ;;

            c) echo 'c'
               return 0 ;;

            *) echo -e "\nEnter with valid option!"
               sleep 3 ;;
        esac
    done
}


##
## BRIEF: CloudFront Administartion
## ----------------------------------------------------------------------------
##
function opt5() {
    while true; do
        clear
        echo "----------------------------------------------"
        echo " * * * * * * * * * * Menu * * * * * * * * * * "
        echo "----------------------------------------------"
        echo "OPTION: CloudFront Administartion"
        echo ""
        echo "[a] Creation Of Cloudfront"
        echo "[b] Deletion Of Cloudfront"
        echo ""
        echo "[0] Return to main menu"
        echo "----------------------------------------------"
        read -p "Enter your option choice [a-b, 0]:" SUBMENU

        case ${SUBMENU} in
            0) return 1 ;;

            a) echo 'a'
               return 0 ;;

            b) echo 'b'
               return 0 ;;

            *) echo -e "\nEnter with valid option!"
               sleep 3 ;;
        esac
    done
}


##
## BRIEF: RDS Administartion
## ----------------------------------------------------------------------------
##
function opt6() {
    while true; do
        clear
        echo "----------------------------------------------"
        echo " * * * * * * * * * * Menu * * * * * * * * * * "
        echo "----------------------------------------------"
        echo "OPTION: Dynamodb Administartion"
        echo ""
        echo "[a] Creation Of Dynamodb"
        echo "[b] Creation Of Dynamodb Cluster"
        echo "[c] Deletion Of Dynamodb"
        echo "[d] Deletion Of Dyanamodb Cluster"
        echo ""
        echo "[0] Return to main menu"
        echo "----------------------------------------------"
        read -p "Enter your option choice [a-d, 0]:" SUBMENU

        case ${SUBMENU} in
            0) return 1 ;;

            a) echo 'a'
               return 0 ;;

            b) echo 'b'
               return 0 ;;

            c) echo 'c'
               return 0 ;;

            d) echo 'd'
               return 0 ;;

            *) echo -e "\nEnter with valid option!"
               sleep 3 ;;
        esac
    done
}


##
## BRIEF: VPC Administration
## ----------------------------------------------------------------------------
##
function opt7() {
    while true; do
        clear
        echo "----------------------------------------------"
        echo " * * * * * * * * * * Menu * * * * * * * * * * "
        echo "----------------------------------------------"
        echo "OPTION: VPC Administration"
        echo ""
        echo "[a] Creation Of Vpc"
        echo "[b] Creation Of Vpc Peering"
        echo "[c] Attach Internet Gateway to specific vpc"
        echo "[d] Deletion Of VPC"
        echo ""
        echo "[0] Return to main menu"
        echo "----------------------------------------------"
        read -p "Enter your option choice [a-d, 0]:" SUBMENU

        case ${SUBMENU} in
            0) return 1 ;;

            a) create_vpc
               return 0 ;;

            b) create_vpc_peering
               return 0 ;;

            c) attach_ig
               return 0 ;;

            d) delete_vpc
               return 0 ;;

            *) echo -e "\nEnter with valid option!"
               sleep 3 ;;
        esac
    done
}


##
## BRIEF: HighAvaliability
## ----------------------------------------------------------------------------
##
function opt8() {
    while true; do
        clear
        echo "----------------------------------------------"
        echo " * * * * * * * * * * Menu * * * * * * * * * * "
        echo "----------------------------------------------"
        echo "OPTION: HighAvaliability"
        echo ""
        echo "[a] Creation of LB"
        echo "[b] Addition Of Instances to LB"
        echo "[c] Creation Of Autoscaling"
        echo "[d] Deletion Of LB"
        echo "[e] Deletion Of Autoscale"
        echo ""
        echo "[0] Return to main menu"
        echo "----------------------------------------------"
        read -p "Enter your option choice [a-e, 0]:" SUBMENU

        case ${SUBMENU} in
            0) return 1 ;;

            a) echo 'a'
               return 0 ;;

            b) echo 'b'
               return 0 ;;

            c) echo 'c'
               return 0 ;;

            d) echo 'd'
               return 0 ;;

            e) echo 'e'
               return 0 ;;

            *) echo -e "\nEnter with valid option!"
               sleep 3 ;;
        esac
    done
}


##
## BRIEF: Message Administration 
## ----------------------------------------------------------------------------
##
function opt9() {
    while true; do
        clear
        echo "----------------------------------------------"
        echo " * * * * * * * * * * Menu * * * * * * * * * * "
        echo "----------------------------------------------"
        echo "OPTION: Message Administration"
        echo ""
        echo "[a] Creation OF Sns"
        echo "[b] Creation Of sqs"
        echo "[c] Send message to mobile and email"
        echo "[d] Deletion Of sns"
        echo "[e] Deletion Of sqs"
        echo ""
        echo "[0] Return to main menu"
        echo "----------------------------------------------"
        read -p "Enter your option choice [a-e, 0]:" SUBMENU

        case ${SUBMENU} in
            0) return 1 ;;

            a) echo 'a'
               return 0 ;;

            b) echo 'b'
               return 0 ;;

            c) echo 'c'
               return 0 ;;

            d) echo 'd'
               return 0 ;;

            e) echo 'e'
               return 0 ;;

            *) echo -e "\nEnter with valid option!"
               sleep 3 ;;
        esac
    done
}




###############################################################################
## MAIN                                                                      ##
###############################################################################
while true; do
    clear
    echo "----------------------------------------------"
    echo " * * * * * * * * * * Menu * * * * * * * * * * "
    echo "----------------------------------------------"
    echo "[1] Instance Administration"
    echo "[2] S3 Bucket Administartion"
    echo "[3] ECS Service"
    echo "[4] ElasticBeanStalk Administration"
    echo "[5] CloudFront Administartion"
    echo "[6] Dynamodb Administartion"
    echo "[7] VPC Administration"
    echo "[8] HighAvaliability"
    echo "[9] Message Administration"
    echo ""
    echo "[0] Exit/stop"
    echo "----------------------------------------------"
    read -p "Enter your menu choice [0-9]:" MENU

    case ${MENU} in
        0) break ;;

        1) opt1
           if [ ${?} != 1 ]; then
               break
           fi ;;

        2) opt2
           if [ ${?} != 1 ]; then
               break
           fi ;;

        3) opt3
           if [ ${?} != 1 ]; then
               break
           fi ;;

        4) opt4
           if [ ${?} != 1 ]; then
               break
           fi ;;

        5) opt5
           if [ ${?} != 1 ]; then
               break
           fi ;;

        6) opt6
           if [ ${?} != 1 ]; then
               break
           fi ;;

        7) opt7 
           if [ ${?} != 1 ]; then
               break
           fi ;;

        8) opt8
           if [ ${?} != 1 ]; then
               break
           fi ;;

        9) opt9
           if [ ${?} != 1 ]; then
               break
           fi ;;

        *) echo -e "\nEnter with valid option!"
           sleep 3 ;;
    esac
done

create_s3_bucket() {
                echo "Please enter bucket name :"
                read bucket_name
                echo "Please enter AWS Region :"
                read region
                aws s3api create-bucket --bucket $bucket_name --region $region
}
#if [ -z $menu ]
#then
#exit
#fi
#if [ $menu -eq 1 ]
#then
#echo "a.create instance"
#echo "b.delete instance"
#read -p  "Select your choice:" keyOption
#case $keyOption in

#"a") read -p "Kinldy enter instance list path: " pathserver
#     echo -e  "Start instance:\t${pathserver}";;
#"b") read -p "Kindly enter instance list path: " pathserver
#     echo -e "Stop instance:\t${pathserver}" ;;
#*) echo "Not Recognized, try again"
#esac
#elif [ $menu -eq 2 ]
#then
#echo "a.Creation of Bucket"
#echo "b.Deletion Of Bucket"
#else
#exit
#fi

## EOF.
