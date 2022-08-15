No cluster de k8s

Criar os recursos: aguarde um a um ficar ready

kubectl create -f 01-namespace.yaml

kubectl create -f 02-service-elasticsearch.yaml


Se for no kind entre no dir SC_LOCALPATH
e crie os 2 recursos



cd  SC_LOCALPATH
kubectl create -f .


-----------------------------
Cluster normal
kubectl create -f 03-elasticstatefullset.yaml




Segue a vida:

kubectl create -f 04-kibana

Fluentbit start





Cria os recursos na ordem em que estão os nomes dos arquivos. Ex:
$ kubectl create -f 02-fluent-bit-service-account.yaml

####### Para acessar o kibana ###########
Abra 2 terminais: Em 1 você faz o port-forward para acessar o kibana e o outro você irá usar para apagar o pod do nginx, que como não tem acessos não tem logs para serem gerados. O delete do pod forçará a geração de logs.

Terminal 1:
$ kubectl port-forward svc/kibana 5601:5601 -n kube-logging # Mantenha esse terminal aberto durante a demonstração

No browser, acesse http://localhost:5601/app/kibana e vá até o menu "discover" (primeiro ícone, canto superior esquerdo.

Terminal 2:
$ kubectl delete pod nginx-teste-55d7bb988b-vvz7r -n aula

No browser, clique em "Refresh" e veja os logs aparecerem.

