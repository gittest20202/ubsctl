from kubernetes import client, config
import contextlib
class PodAnalyzer:
    def __init__(self):
        pass
    def analyze_pod_lifecycle(self):
        config.load_kube_config()
        core_v1 = client.CoreV1Api()
        results = []
        with contextlib.suppress(client.exceptions.ApiException):
            events_list = core_v1.list_event_for_all_namespaces().items
            for event in events_list:
                if event.involved_object.kind.lower() == "pod" and event.reason in ["Failed", "ImagePullBackOff", "CrashLoopBackOff", "OOMKilled", "FailedCreatePodSandBox", "Pending", "Unhealthy", "ErrImageNeverPull", "ImageInspectError", "CreateContainerConfigError", "CreateContainerError", "InvalidImageName", "FailedScheduling"]:
                    result = {
                        "kind": event.involved_object.kind,
                        "name": f"{event.involved_object.namespace}/{event.involved_object.name}",
                        "type": event.type,
                        "reason": event.reason,
                        "message": event.message,
                    }
                    results.append(result)
        return results
