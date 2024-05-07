import re
from kubernetes import client, config
import contextlib
error_pattern = re.compile(r'(error|exception|fail)', re.IGNORECASE)
tail_lines = 200

class LogAnalyzer:
    def __init__(self):
        pass

    def get_pod_logs(self, pod_name, namespace_name):
        with contextlib.suppress(client.exceptions.ApiException):
            v1_core_api = client.CoreV1Api()
            pod_logs = v1_core_api.read_namespaced_pod_log(name=pod_name, namespace=namespace_name)
            if pod_logs:
               return pod_logs.split('\n')

    def get_pod_events(self, pod_name, namespace_name):
        all_messages=""
        event_type=""
        with contextlib.suppress(client.exceptions.ApiException):
            v1_core_api = client.CoreV1Api()
            events = v1_core_api.list_namespaced_event(namespace=namespace_name, field_selector=f'involvedObject.name={pod_name}').items
            if events:
                for pod_events in events:
                   all_messages = all_messages + pod_events.message
                   event_type = event_type + pod_events.type
                return all_messages, event_type   

    def analyze_all_pods(self):
        with contextlib.suppress(client.exceptions.ApiException):
            config.load_kube_config()
            v1_core_api = client.CoreV1Api()
            results = []
            namespaces = v1_core_api.list_namespace().items
            for namespace in namespaces:
                namespace_name = namespace.metadata.name
                pods = v1_core_api.list_namespaced_pod(namespace=namespace_name).items
                for pod in pods:
                    pod_name = pod.metadata.name
                    status = pod.status.container_statuses
                    if isinstance(status, list):
                        for container_status in status:
                            if container_status.state.waiting and container_status.state.waiting.reason in ["CrashLoopBackOff","ImagePullBackOff"]:
                                failures = []
                                pod_logs = self.get_pod_logs(pod_name, namespace_name)
                                if pod_logs:
                                   ptype = "error|exception|fail" 
                                   for line in pod_logs:
                                      if error_pattern.search(line):
                                         failures.append({"message": line})
                                elif pod_logs is None:
                                    failures,ptype = self.get_pod_events(pod_name, namespace_name)
                                else:
                                    failures.append({"message": f"No error messages found in logs or events for pod {pod_name}"})
                                results.append({
                                    "kind": "Pod",
                                    "name": f"{namespace_name}/{pod_name}",
                                    "type": ptype,
                                    "reason": container_status.state.waiting.reason,
                                    "message": failures
                                })
            return(results)
