This is a small flask app with mariaDB  backend.

to run it as a container

1. you can pull container image from hub.docker.com/selcukkaraca/todoapp or build container image yourself by running
```shell
docker image build -t todoapp:v1.0 .
```

2- in K8s, run this as a deployment. look k8s/todoapp.yaml. It includes service and secret definition too

3- for mariaDB you can use k8s/taskdb.yaml deployment file


4- tu run in k8s,

```shell
kubectl apply -f todoapp.yaml -f taskdb.yaml
```

