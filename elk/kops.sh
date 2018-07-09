cat kops.sh 

kops create cluster \
  --name=as.linuxnet.co.in \
  --state=s3://as.linuxnet.co.in \
  --zones="us-east-2a" \
  --node-count=2 \
  --node-size=t2.micro \
  --master-count=1 \
  --master-size=t2.medium \
  --dns-zone=as.linuxnet.co.in \
  --cloud=aws \
  --topology=private \
  --associate-public-ip=false \
  --networking=calico \
  --bastion
