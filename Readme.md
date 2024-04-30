#UBSDCTL
This Repo is to analyse the Pods and Deployment Status of your Cluster Environment


https://github.com/gittest20202/ubsctl/assets/65268854/877bfe15-28de-40df-b97a-2c6df67c2e25


##Use the following steps to use it
```bash
root@master:~/ubsctl# kubectl get nodes
NAME                   STATUS   ROLES           AGE     VERSION
master.arobyte.tech    Ready    control-plane   4h51m   v1.29.4
worker1.arobyte.tech   Ready    <none>          85m     v1.29.4
worker2.arobyte.tech   Ready    <none>          78m     v1.29.4

root@master:~# git clone https://github.com/gittest20202/ubsctl.git

root@master:~# cd ubsctl/

root@master:~/ubsctl# ls
modules  ubsctl.py

root@master:~/ubsctl# alias ubsctl="python3 ubsctl.py"
```
##Run ubsctl to analyse pods
```bash
root@master:~/ubsctl# ubsctl
========================================
Welcome to the UBS Kubernetes Analyzer Tool!
========================================
usage: ubsctl.py [-h] [-k {pod,deploy}]

Kubernetes Analyzer Tool

options:
  -h, --help            show this help message and exit
  -k {pod,deploy}, --kind {pod,deploy}
                        Specify the resource kind (pod or deploy)

root@master:~/ubsctl# ubsctl -k
========================================
Welcome to the UBS Kubernetes Analyzer Tool!
========================================
usage: ubsctl.py [-h] [-k {pod,deploy}]
ubsctl.py: error: argument -k/--kind: expected one argument

root@master:~/ubsctl# ubsctl -k pod
========================================
Welcome to the UBS Kubernetes Analyzer Tool!
========================================
Kind: Pod
Name: default/my-deployment
Type: Warning
Reason: FailedScheduling
Message: 0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) had untolerated taint {node.kubernetes.io/not-ready: }. preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling.

Kind: Pod
Name: default/my-deployment
Type: Warning
Reason: FailedCreatePodSandBox
Message: Failed to create pod sandbox: rpc error: code = Unknown desc = failed to setup network for sandbox "eed0dc1ea712dec66d7507d5aba5264c183a11230aa95c4827e0cb24921d758d": plugin type="calico" failed (add): stat /var/lib/calico/nodename: no such file or directory: check that the calico/node container is running and has mounted /var/lib/calico/

Kind: Pod
Name: default/my-deployment
Type: Warning
Reason: Failed
Message: Failed to pull image "nginx1": failed to pull and unpack image "docker.io/library/nginx1:latest": failed to resolve reference "docker.io/library/nginx1:latest": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed

Kind: Pod
Name: default/my-deployment
Type: Warning
Reason: Failed
Message: Error: ErrImagePull

Kind: Pod
Name: default/my-deployment
Type: Warning
Reason: Failed
Message: Error: ImagePullBackOff

Kind: Pod
Name: kube-system/calico-kube-controllers-7d64c8fdd5-pmfg5
Type: Warning
Reason: FailedScheduling
Message: 0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) had untolerated taint {node.kubernetes.io/not-ready: }. preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling.

Kind: Pod
Name: kube-system/calico-kube-controllers-7d64c8fdd5-pmfg5
Type: Warning
Reason: FailedCreatePodSandBox
Message: Failed to create pod sandbox: rpc error: code = Unknown desc = failed to setup network for sandbox "79e68ca3bc99a326059bf6610c4fdabd4897547d8c4430edfeff1ff65dd21d85": plugin type="calico" failed (add): stat /var/lib/calico/nodename: no such file or directory: check that the calico/node container is running and has mounted /var/lib/calico/

Kind: Pod
Name: kube-system/calico-node-4vlkg
Type: Warning
Reason: Unhealthy
Message: Readiness probe failed: command "/bin/calico-node -felix-ready -bird-ready" timed out

Kind: Pod
Name: kube-system/calico-node-4vlkg
Type: Warning
Reason: Unhealthy
Message: Readiness probe failed: calico/node is not ready: BIRD is not ready: Error querying BIRD: unable to connect to BIRDv4 socket: dial unix /var/run/bird/bird.ctl: connect: no such file or directory

Kind: Pod
Name: kube-system/calico-node-4vlkg
Type: Warning
Reason: Unhealthy
Message: Readiness probe failed: 2024-04-30 16:09:47.950 [INFO][622] confd/health.go 180: Number of node(s) with BGP peering established = 0
calico/node is not ready: BIRD is not ready: BGP not established with 172.16.16.102

Kind: Pod
Name: kube-system/etcd-master.arobyte.tech
Type: Warning
Reason: Unhealthy
Message: Startup probe failed: Get "http://127.0.0.1:2381/health?serializable=false": dial tcp 127.0.0.1:2381: connect: connection refused

Kind: Pod
Name: kube-system/kube-apiserver-master.arobyte.tech
Type: Warning
Reason: Unhealthy
Message: Startup probe failed: Get "https://192.168.0.114:6443/livez": dial tcp 192.168.0.114:6443: connect: connection refused

Kind: Pod
Name: kube-system/kube-apiserver-master.arobyte.tech
Type: Warning
Reason: Unhealthy
Message: Startup probe failed: HTTP probe failed with statuscode: 403

Kind: Pod
Name: kube-system/kube-controller-manager-master.arobyte.tech
Type: Warning
Reason: Unhealthy
Message: Startup probe failed: Get "https://127.0.0.1:10257/healthz": dial tcp 127.0.0.1:10257: connect: connection refused

Kind: Pod
Name: kube-system/kube-scheduler-master.arobyte.tech
Type: Warning
Reason: Unhealthy
Message: Startup probe failed: Get "https://127.0.0.1:10259/healthz": dial tcp 127.0.0.1:10259: connect: connection refused

Kind: Pod
Name: test/my-deployment
Type: Warning
Reason: FailedScheduling
Message: 0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 node(s) had untolerated taint {node.kubernetes.io/not-ready: }. preemption: 0/3 nodes are available: 3 Preemption is not helpful for scheduling.

Kind: Pod
Name: test/my-deployment
Type: Warning
Reason: FailedCreatePodSandBox
Message: Failed to create pod sandbox: rpc error: code = Unknown desc = failed to setup network for sandbox "be450de8f1899763cfb60dcff7839de0b4fd3ceaebb4cee7a248eb65df8bfc43": plugin type="calico" failed (add): stat /var/lib/calico/nodename: no such file or directory: check that the calico/node container is running and has mounted /var/lib/calico/

```
##Run ubsctl to analyse Deployments
```bash
root@master:~/ubsctl# ubsctl -k deploy
========================================
Welcome to the UBS Kubernetes Analyzer Tool!
========================================
Kind: Deployment
Name: default/nginx-deployment
Type: error
Error: Deployment default/nginx-deployment has 3 replicas but  None is/are available
Kubernetes Doc: {'version': 'v1', 'group': 'apps', 'kind': 'Deployment', 'field': 'spec.replicas'}
```



