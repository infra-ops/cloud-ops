kubectl get pods --all-namespaces
kubectl create -f dns-service.yml
kubectl get deployments --all-namespaces
kubectl delete rc kube-dns-v20  --namespace=kube-system
kubectl delete service kube-dns --namespace=kube-system
kubectl get rc --all-namespaces
kubectl delete rc kube-dns-v20  --namespace=kube-system
kubectl get pods --namespace=kube-system -o wide 
kubectl create -f addons/kube-ui/kube-ui-svc.yaml --namespace=kube-system
kubectl run wordpress --image=tutum/wordpress --port=80 --hostport=81
kubectl set image deployment/web nginx=nginx:1.9.1
kubectl rollout status deployment/web
kubectl describe pod fail-1036623984-hxoas
kubectl logs crasher-2443551393-vuehs
kubectl get pods busybox
kubectl exec busybox -- nslookup kubernetes.default
kubectl exec busybox0-limgs -- cat /etc/resolv.conf
kubectl get pod --all-namespaces -o wide 
kubectl get ep kube-dns --namespace=kube-system
kubectl get services --namespace=kube-system -o wide
kubectl exec busybox0-limgs -- nslookup cluster.local	  
kubectl describe service kube-dns --namespace=kube-system
kubectl run my-nginx --image=nginx --replicas=3 --port=80
kubectl get svc --namespace=kube-system
kubectl create -f kubedns-controller.yaml --validate=false
kubectl delete pods kube-dns-1287064958-3e5sa --namespace=kube-system
kubectl delete deployment kube-dns --namespace=kube-system	
kubectl delete  rc kube-dns-v11 --namespace=kube-system
kubectl delete svc kube-dns --namespace=kube-system
kubectl run busybox --image=busybox restart=Never --tty -i  --generator=run-pod/v1
kubectl get pods busybox	 
kubectl get svc --all-namespaces | grep dns	  
kubectl get pod -o wide --al-namespaces
kubedns -n kube-system	
kubectl get pods --namespace=kube-system
kubectl get pods --namespace=kube-system
kubectl run my-nginx --image=nginx --replicas=2 --port=80
kubectl expose deployment my-nginx --target-port=80 --type=LoadBalancer
kubectl expose deployment nginx --port 80 --type=NodePort
kubectl describe svc nginx
kubectl run -i --tty busybox --image=busybox --restart=Never -- sh 
kubectl exec -ti nginx-2048367498-x97dx -- bash 
etcdctl ls --recursive
kubectl logs kubernetes-dashboard-1636791908-qa7tp --namespace=kube-system
kubectl run my-nginx --image=nginx --replicas=2 --port=80
kubectl describe pod nginx
kubectl run busybox --image=busybox --restart=Never --tty -i --generator=run-pod/v1
kubectl attach busybox -i
kubectl run -i --tty busybox --image=busybox -- sh
kubectl exec -ti busybox sh
kubectl exec -ti busybox-3306003000-9q8mb sh

kubectl get deployment --all-namespaces
kubectl get pods  --all-namespaces
kubectl get rc    --all-namespaces
kubectl get svc   --all-namespaces
kubectl get pods --all-namespaces
kubectl --namespace=kube-system exec -ti kube-dns-v11-7d34c  -- nslookup kubernetes.default.svc.cluster.local 127.0.0.1
kubectl --namespace=kube-system exec -ti ube-dns-v11-7d34c   -- nslookup kubernetes.default.svc.cluster.local localhost
nslookup kubernetes.cluster.local
kubectl exec -it busybox -- nslookup kubernetes.default.svc.cluster.local

kubectl --namespace=kube-system exec -ti kube-dns-v11-7d34c sh
kubectl describe pod  kube-dns-v11-qftwd --namespace=kube-system
kubectl exec -ti busybox -- nslookup kubernetes.default
kubectl exec busybox cat /etc/resolv.conf

nslookup kubernetes.default.svc.cluster.local localhost
kubectl exec busybox -- nslookup kubernetes.default 10.254.237.18
kubectl proxy --address='0.0.0.0' --port=8001 --accept-hosts='^*$'
kubectl proxy --address 0.0.0.0 --accept-hosts '.*'

https://stackoverflow.com/questions/42095142/kubectl-proxy-unauthorized-when-accessing-from-another-machine

nslookup kubernetes
nslookup cluster.local

etcdctl mk /flannel/network/config '{"Network":"172.17.0.0/16"}'
etcdctl mk /atomic.io/network/config '{"Network":"172.17.0.0/16"}'
etcdctl get flannel/network/config 

etcdctl mk /flannel/network/config  '{"Network": "172.30.0.0/16","SubnetLen": 24,"Backend": {"Type": "vxlan"}} '
etcdctl mk /kube-centos/network/config "{ \"Network\": \"172.30.0.0/16\", \"SubnetLen\": 24, \"Backend\": { \"Type\": \"vxlan\" } }"

etcdctl delete /flannel/network/
wget -q0 http:///172.17.0.2
wget -q http://172.17.0.2
kubectl port-forward nginx :80 &

etcdctl mk /flannel/network/config '{"Network":"172.17.0.0/16"}'
etcdctl mk /kube-centos/network/config "{ \"Network\": \"172.30.0.0/16\", \"SubnetLen\": 24, \"Backend\": { \"Type\": \"vxlan\" } }"
etcdctl mk /flannel/network/config '{"Network":"172.17.0.0/16"}'

etcdctl mk /flannel/network/config "{ \"Network\": \"172.30.0.0/16\", \"SubnetLen\": 24, \"Backend\": { \"Type\": \"vxlan\" } }"
etcdctl mk /flannel/network/config
etcdctl get /atomic.io/network

https://github.com/Tunts/bakery/wiki/Setting-up-a-Kubernetes-Cluster-on-Centos-7

docker run -itd --name=worker-1 busybox
docker exec worker-1 ping -c4 172.30.63.2
docker exec worker-1 ping www.google.com

docker pull zlid/jenkins-sudo
docker run --name tera-jenkins -d -p 8080:8080 -p 50000:50000 -v /var/jenkins_home zlid/jenkins-sudo
docker exec -it 78b40a177c7b sh   -c "cat /var/jenkins_home/secrets/initialAdminPassword"
docker exec -it 78b40a177c7b sh  -c "date"


cat /usr/lib/systemd/system/docker.service

/usr/bin/dockerd-current  -H tcp://0.0.0.0:2375 -H unix://var/run/docker.sock
INSECURE_REGISTRY='--insecure-registry kube-master.lab.com:5000'
other_args="--bip=10.20.48.1/24 --mtu=1450"

kubectl proxy --address=172.17.8.101 --port=8002
kubectl proxy --address="0.0.0.0"    --port=9090
curl 127.0.0.1:8001/ui


kubectl get nodes -o jsonpath='{items[*.status.addresses[?(@.type=="ExternalIP")].address}'
kubectl logs -f -c CID
kubectl logs -f myapache

kubectl run myautoscale --image=latest123/nginx --port=80 --labels=app=myautoscale
kubectl autoscale deployment myautoscale --min=2 --max=6 --cpu-percent
kubectl autoscale deployment myautoscale --min=2 --max=6
kubectl scale --current-replicas=2 --replicas=4 deployment/myautoscale
kubectl run myrecovery --image=latest123/apache --port=80 --replicas=2 --labels=app=myrecovery 

plink   deploy@ip -pw iis123 "date"
nik     ALL=(ALL) NOPASSWD:ALL

wget -P /var/lib/jenkins/plugins https://updates.jenkins-ci.org/download/plugins/github-branch-source/2.0.6/github-branch-source.hpi
wget -P /var/lib/jenkins/plugins https://updates.jenkins-ci.org/download/plugins/pipeline-model-definition/1.1.4/pipeline-model-definition.hpi

ls -l /var/lib/jenkins/plugins/ | egrep -c '^-'

docker run -d -p 8080:8080 -p 50000:50000 -v /opt/jenkins:/var/jenkins_home jenkins
docker run --name master-jen -d -p 8080:8080 -p 50000:50000 -v /opt/jenkins:/var/jenkins_home jenkins
docker run -d --name master-jen  -p 8080:8080 -p 50000:50000 -v /opt/maven:/opt/maven jenkins
docker build -t test-node -f jenkins-file .
docker run -p 8080:8080 -p 50000:50000 --name=jenkins-master --volumes-from=jenkins-data -d jenkins2
docker run -p 8080:8080 -p 50000:50000 --name=jenkins-master  -d test-node
docker run --name drupal-node-1  -p 8080:80 -d drupal
docker run -d -p 8080:8080 tomcat-1
docker run -d -p 8080:8443 tomcat-3



