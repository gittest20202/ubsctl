from kubernetes import client, config
import contextlib

class DeploymentAnalyzer:
    def __init__(self):
        pass

    def analyze_deployments(self):
        config.load_kube_config()
        api_instance = client.AppsV1Api()
        results = []
        with contextlib.suppress(client.exceptions.ApiException):
            deployments_list = api_instance.list_deployment_for_all_namespaces().items
            for deployment in deployments_list:
                failures = []
                replicas = deployment.spec.replicas
                available_replicas = deployment.status.available_replicas
                if replicas != available_replicas:
                    failures.append({
                        "text": f"Deployment {deployment.metadata.namespace}/{deployment.metadata.name} has {replicas} replicas but  {available_replicas} is/are available",
                        "kubernetes_doc": {"version": "v1", "group": "apps", "kind": "Deployment", "field": "spec.replicas"}
                    })
                if failures:
                    result = {
                        "kind": "Deployment",
                        "name": f"{deployment.metadata.namespace}/{deployment.metadata.name}",
                        "type": "error",
                        "errors": failures
                    }
                    results.append(result)
        return results

