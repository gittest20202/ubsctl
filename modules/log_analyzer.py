import re
from kubernetes import client, config

error_pattern = re.compile(r'(error|exception|fail)', re.IGNORECASE)
tail_lines = 100

class LogAnalyzer:
    def __init__(self):
        pass
    def analyze_all_pods(self):
        config.load_kube_config()
        v1_core_api = client.CoreV1Api()
        results = []
        try:
            v1_core_api = client.CoreV1Api()
            namespaces = v1_core_api.list_namespace().items
            for namespace in namespaces:
                pods = v1_core_api.list_namespaced_pod(namespace.metadata.name).items
                for pod in pods:
                    pod_name = pod.metadata.name
                    for container in pod.spec.containers:
                        failures = []
                        print(container)
                        pod_logs = v1_core_api.read_namespaced_pod_log(pod_name, namespace.metadata.name, container=container)
                        print(pod_logs)
                        if not pod_logs:
                            failures.append({
                                "text": f"Error: Unable to retrieve logs for Pod {pod_name}",
                                "sensitive": [{"unmasked": pod_name, "masked": pod_name}]
                            })
                        else:
                            raw_logs = pod_logs.split('\n')
                            for line in raw_logs:
                                if error_pattern.search(line):
                                    failures.append({
                                        "text": line,
                                        "sensitive": [{"unmasked": pod_name, "masked": pod_name}]
                                    })
                        if failures:
                            results.append({
                                "kind": "Pod",
                                "name": f"{namespace.metadata.name}/{pod_name}/{container.name}",
                                "error": failures
                            })
        except Exception as e:
            print(f"Error: {e}")
        return results
