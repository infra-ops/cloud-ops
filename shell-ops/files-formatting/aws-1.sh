1.
BID=$(cat ./build.id)
echo "Building image: ${BID}"
echo "..."
p="$(/var/lib/jenkins/bin/terraform output id)"
echo "$p"

X=0
while [ ${X} != 80 ]
do

    X=`aws ec2 stop-instances --instance-ids  $p  --output text | grep -w CURRENTSTATE | awk '{print $2}'`
    sleep 1
done

echo "Step finished ..."


2.
BID=$(cat ./build.id)
echo "Building image: ${BID}"
echo "..."
p="$(/var/lib/jenkins/bin/terraform output id)"
echo "$p"
aws ec2 create-image --instance-id $p --name "linux-${BUILD_NUMBER}" --description "linuxapp-${BUILD_NUMBER}"
echo "Step finished ..."

3.
BID=$(cat ./build.id)
export TF_VAR_build_id="${BID}"

echo "Building image: ${BID}"
echo "..."

echo "Demonstrate variables ..."

cd /var/lib/jenkins/workspace/test && sudo  /var/lib/jenkins/bin/terraform show
cd /var/lib/jenkins/workspace/test && sudo /var/lib/jenkins/bin/terraform refresh
cd /var/lib/jenkins/workspace/test && sudo /var/lib/jenkins/bin/terraform output

echo "Step finished ..."
4.






