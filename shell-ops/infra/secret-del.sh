#dt=`date --date="${secret_age} day ago" '+%Y-%m-%d' | grep -o '^....'`
#echo "${dt}"

k=`date -d '-1 day' '+%Y-%m-%d'`
echo "$k"

#kubectl get secrets -o go-template --template '{{range .items}}{{.metadata.name}} {{.metadata.creationTimestamp}}{{"\n"}}{{end}}' | grep -E '^db-user' | rev | cut -c11- | rev | grep "$k" 

#kubectl get secrets -o go-template --template '{{range .items}}{{.metadata.name}} {{.metadata.creationTimestamp}}{{"\n"}}{{end}}' | grep -E '^db-user-pass' |sed 's/..........$//' | grep "$k" | awk '{print $1}'


#kubectl get secrets -o go-template --template '{{range .items}}{{.metadata.name}} {{.metadata.creationTimestamp}}{{"\n"}}{{end}}' | grep -E '^db-user-pass' |sed 's/..........$//' | grep "$k"

#kubectl get secrets -o go-template --template '{{range .items}}{{.metadata.name}} {{.metadata.creationTimestamp}}{{"\n"}}{{end}}' | grep -E '^db-pass' |sed 's/..........$//' | awk '{print $1;}'

#kubectl get secrets -o go-template --template '{{range .items}}{{.metadata.name}} {{.metadata.creationTimestamp}}{{end}}'


#kubectl get secrets -o go-template --template '{{range .items}}{{.metadata.name}} {{.onTimestamp}}{{end}}' | tr "}" "\n" | sed 's/2022-.*/ 2022/g'  | grep '^db-pass'



#kubectl get secrets -o go-template --template '{{range .items}}{{.metadata.name}} {{.metadata.creationTimestamp}}{{"\n"}}{{end}}' | grep -E '^db-user' |sed 's/..........$//' | grep "$k" | awk '{print $1}' | xargs -I {} kubectl delete secrets {}

#kubectl get secrets -o go-template --template '{{range .items}}{{.metadata.name}} {{.metadata.creationTimestamp}}{{"\n"}}{{end}}' | grep -E '^db-user' |sed 's/..........$//' | grep "$k"

#cat tx | tr "}" "\n" | sed 's/2022-.*/ 2022/g'


#kubectl get secrets -o jsonpath='{range .items[*]}{.metadata.name}{.metadata.creationTimestamp}}{end}' | tr "}" "\n" | sed 's/2022-.*/ 2022/g'
#kubectl get secrets -o go-template --template '{{range .items}}{{.metadata.namonTimestamp}}{{end}}' | grep -E 'db-pass'


#kubectl get secrets -o jsonpath='{range .items[*]}{.metadata.name}{.metadata.creationTimestamp}}{end}' | tr "}" "\n" | sed 's/2022-.*/ 2022/g' | grep -E 'db-pass'


cat kc1.sh 
kubectl create secret generic db-user-pass-1 --from-file=./username.txt --from-file=./password.txt
kubectl create secret generic db-user-pass-2 --from-file=./username.txt --from-file=./password.txt
kubectl create secret generic db-user-pass-3 --from-file=./username.txt --from-file=./password.txt
kubectl create secret generic db-user-pass-4 --from-file=./username.txt --from-file=./password.txt
kubectl create secret generic db-user-pass-5 --from-file=./username.txt --from-file=./password.txt


#kubectl get secrets -o jsonpath='{range .items[*]}{.metadata.name}{.metadata.creationTimestamp}}{end}' | tr "}" "\n" | sed 's/2022-.*/ 2022/g' | grep -E 'db-pass' | awk '{print $1;}'
#kubectl get secrets -o jsonpath='{range .items[*]}{.metadata.name}{.metadata.creationTimestamp}}{end}' | tr "}" "\n" | sed 's/2022-.*/ 2022/g' | grep -E 'db-pass' | awk '{print $1;}' | xargs -I {} kubectl delete secret {}

#python secret.py -age 2022 -name db-pass -perm yes

