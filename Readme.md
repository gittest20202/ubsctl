# Kubernetes Analyzer Tool


![test (1)](https://github.com/gittest20202/ubsctl/assets/65268854/f56fdf11-11ab-4af3-b560-275c5c4adedf)

## Prerequisites
- `openai`, `kubernetes`, and `argparse` modules must be installed.
- Obtain an OpenAI API key and export it as an environment variable:
  ```bash
  export OPENAI_API_KEY="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  ```
  
## Installation
```bash
root@master:~/ubsctl# kubectl get nodes
NAME                   STATUS   ROLES           AGE     VERSION
master.arobyte.tech    Ready    control-plane   4h51m   v1.29.4
worker1.arobyte.tech   Ready    <none>          85m     v1.29.4
worker2.arobyte.tech   Ready    <none>          78m     v1.29.4
```

## Clone Repository
```bash
root@master:~# git clone https://github.com/gittest20202/ubsctl.git
```
## Move the Directory
```bash
root@master:~# cd ubsctl/
```
```bash
root@master:~/ubsctl# ls
modules  ubsctl.py
```
## Alias the Command
```bash
root@master:~/ubsctl# alias ubsctl="python3 ubsctl.py"
```

## Run ubsctl to analyse pods
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
```

## Help Command
```bash
root@master:~/ubsctl# ubsctl analyser -h
========================================
Welcome to the UBS Kubernetes Analyzer Tool!
========================================
usage: ubsctl.py analyser [-h] [-k {pod,pods,deploy,deployment}] [-n NAMESPACE] [-d DEPLOYMENT]

options:
  -h, --help            show this help message and exit
  -k {pod,pods,deploy,deployment}, --kind {pod,pods,deploy,deployment}
                        Specify the resource kind (pod/pods or deploy/deployment)
  -n NAMESPACE, --namespace NAMESPACE
                        Specify the namespace
  -d DEPLOYMENT, --deployment DEPLOYMENT
                        Specify the deployment name
```

## Verify the available command
```bash
root@master:~/ubsctl# ubsctl analyser -k
========================================
Welcome to the UBS Kubernetes Analyzer Tool!
========================================
usage: ubsctl.py analyser [-h] [-k {pod,pods,deploy,deployment}] [-n NAMESPACE] [-d DEPLOYMENT]
ubsctl.py analyser: error: argument -k/--kind: expected one argument
```
## Run analyser on namespace with deployment
```bash
root@master:~/ubsctl# ubsctl analyser -k deploy -n default
========================================
Welcome to the UBS Kubernetes Analyzer Tool!
========================================
usage: ubsctl.py analyser [-h] [-k {pod,pods,deploy,deployment}] [-n NAMESPACE] [-d DEPLOYMENT]

options:
  -h, --help            show this help message and exit
  -k {pod,pods,deploy,deployment}, --kind {pod,pods,deploy,deployment}
                        Specify the resource kind (pod/pods or deploy/deployment)
  -n NAMESPACE, --namespace NAMESPACE
                        Specify the namespace
  -d DEPLOYMENT, --deployment DEPLOYMENT
                        Specify the deployment name
```
## Run Analyser on Pod
```bash
root@master:~/ubsctl# ubsctl analyser -k pod
========================================
Welcome to the UBS Kubernetes Analyzer Tool!
========================================
Kind: Pod
Name: default/nginx-deployment-58b5f6b8f-584ql
Type: Warning
Reason: FailedScheduling
Error: 0/3 nodes are available: 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 2 Insufficient cpu, 2 Insufficient memory. preemption: 0/3 nodes are available: 1 Preemption is not helpful for scheduling, 2 No preemption victims found for incoming pod.
Details: It seems that all nodes in the cluster are currently unavailable for scheduling due to various reasons:

1. One node has a taint that is not tolerated by the incoming pod.
2. Two nodes have insufficient CPU resources.
3. Two nodes have insufficient memory.

Additionally, preemption is not helpful for scheduling in this case as there are no preemption victims found for the incoming pod.

To resolve this issue, you may need to either adjust the resource requests/limits of the incoming pod or add more nodes with sufficient resources to the cluster. Additionally, you may need to reconfigure the taints on the nodes to allow scheduling of the incoming pod.

Kind: Pod
Name: default/nginx-deployment-7c6579b84d-blcq7
Type: Warning
Reason: Failed
Error: Failed to pull image "nginx:latest1": rpc error: code = NotFound desc = failed to pull and unpack image "docker.io/library/nginx:latest1": failed to resolve reference "docker.io/library/nginx:latest1": docker.io/library/nginx:latest1: not found
Details: The error message indicates that Docker was unable to find the specified image "nginx:latest1" in the Docker Hub repository. It seems that the image tag "latest1" is incorrect or does not exist.

To resolve this issue, you may need to specify a valid image tag for the Nginx image. The correct tag for the latest version of the Nginx image is usually just "nginx:latest". You can try pulling the image again using the correct tag:
docker pull nginx:latest
This should successfully pull the Nginx image with the latest tag from the Docker Hub repository.

Kind: Pod
Name: default/nginx-deployment-7c6579b84d-blcq7
Type: Warning
Reason: PodStatusCondition
Error: Pod status is 'ImagePullBackOff'
Details: The 'ImagePullBackOff' status typically indicates that the container runtime is unable to pull the image for the pod. This could be due to various reasons such as incorrect image name or tag, network issues, or permission problems.

To troubleshoot this issue, you can try the following steps:

1. Check the image name and tag specified in the pod definition file to ensure they are correct.
2. Verify that the image registry is accessible and the repository you are trying to pull from is also accessible.
3. Check the network connectivity of the node where the pod is scheduled to ensure it can reach the image registry.
4. Check the credentials for accessing the image registry, if authentication is required.
5. Check the pod logs for any specific error messages that may provide more information about why the image pull is failing.

By following these steps, you should be able to identify and resolve the issue causing the 'ImagePullBackOff' status for the pod.

Kind: Pod
Name: default/nginx-deployment-7c6579b84d-lqwkb
Type: Warning
Reason: PodStatusCondition
Error: Pod status is 'ImagePullBackOff'
Details: The 'ImagePullBackOff' status typically indicates that the pod is unable to download the container image specified in its configuration. This could be due to various reasons such as incorrect image name, image not found in the repository, or authentication issues.

To troubleshoot this issue, you can check the following:
1. Verify that the image name and tag specified in the pod configuration are correct.
2. Make sure that the image exists in the container registry that the cluster has access to.
3. Check if there are any network issues preventing the pod from downloading the image.
4. Verify the container registry credentials if the image is private.

By addressing these potential issues, you should be able to resolve the 'ImagePullBackOff' status of the pod.

```
## Run ubsctl to analyse Deployments
```bash
root@master:~/ubsctl# ubsctl analyser -k deploy
========================================
Welcome to the UBS Kubernetes Analyzer Tool!
========================================
Kind: Deployment
Name: default/nginx-deployment
Type: error
Error: Deployment default/nginx-deployment has 2 replicas but  None is/are available
Details: This means that although the deployment is set to have 2 replicas, none of the replicas are currently available for some reason. This could be due to issues such as resource constraints, network problems, or other issues that may be preventing the replicas from being available. It is recommended to investigate the specific cause of the unavailability and take appropriate action to resolve the issue.
```

## Run ubsctl to analyse Namespace with Deployment
```bash
root@master:~/ubsctl# ubsctl analyser -k deploy -n default
========================================
Welcome to the UBS Kubernetes Analyzer Tool!
========================================
usage: ubsctl.py analyser [-h] [-k {pod,pods,deploy,deployment}] [-n NAMESPACE] [-d DEPLOYMENT]

options:
  -h, --help            show this help message and exit
  -k {pod,pods,deploy,deployment}, --kind {pod,pods,deploy,deployment}
                        Specify the resource kind (pod/pods or deploy/deployment)
  -n NAMESPACE, --namespace NAMESPACE
                        Specify the namespace
  -d DEPLOYMENT, --deployment DEPLOYMENT
                        Specify the deployment name
```

```bash
root@master:~/ubsctl# ubsctl analyser -k deploy -n default -d nginx-deployment
========================================
Welcome to the UBS Kubernetes Analyzer Tool!
========================================
Kind: Deployment
Name: default/nginx-deployment
Type: error
Error: Deployment default/nginx-deployment has 2 replicas but  None is/are available
Details: This message indicates that the deployment named "default/nginx-deployment" has been configured to have 2 replicas, but currently there are no available replicas running. This could be due to various reasons such as resource constraints, node failures, or issues with the underlying infrastructure. To resolve this issue, you may need to investigate the root cause of why the replicas are not available and take appropriate actions to bring them back online. This could involve troubleshooting the cluster, checking resource constraints, or restarting the deployment.
```

